#!/usr/bin/env python3
"""Extract AI-related topics from scraped dev.bg job ads.

Reads data/jobs.jsonl, matches each description against a taxonomy of AI
topics (regex patterns, English + Bulgarian), and writes:
  data/ai_topics.json        - per-topic counts, matching job URLs and snippets
  data/ai_topics_report.md   - human-readable summary

Usage: python3 analysis/extract_ai_topics.py
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOBS = ROOT / "data" / "jobs.jsonl"
OUT_JSON = ROOT / "data" / "ai_topics.json"
OUT_MD = ROOT / "data" / "ai_topics_report.md"

# topic -> list of case-insensitive regexes
TAXONOMY = {
    "AI / ML (general mention)": [r"\bAI\b", r"artificial intelligence", r"изкуствен\w* интелект", r"\bML\b", r"machine learning", r"машинно обучение"],
    "LLMs / Generative AI": [r"\bLLMs?\b", r"large language model", r"generative ai", r"\bgen ?ai\b", r"\bGPT[-\w]*", r"foundation model"],
    "LLM providers & APIs (OpenAI, Anthropic, Gemini, Bedrock, Azure OpenAI)": [r"openai", r"anthropic", r"\bclaude\b", r"gemini", r"bedrock", r"azure openai", r"vertex ai", r"mistral", r"llama", r"hugging ?face"],
    "Prompt engineering": [r"prompt engineering", r"\bprompts?\b", r"prompting"],
    "RAG / retrieval / embeddings": [r"\bRAG\b", r"retrieval[- ]augmented", r"embeddings?", r"semantic search", r"vector search"],
    "Vector databases": [r"vector (db|database|store)s?", r"pinecone", r"weaviate", r"qdrant", r"milvus", r"chroma(db)?\b", r"pgvector", r"faiss"],
    "AI agents & agentic workflows": [r"\bagents?\b(?! of)", r"agentic", r"multi[- ]agent", r"autonomous agent", r"tool[- ]calling", r"function calling"],
    "MCP (Model Context Protocol)": [r"\bMCP\b", r"model context protocol"],
    "LLM frameworks (LangChain, LlamaIndex, Semantic Kernel...)": [r"langchain", r"langgraph", r"llama ?index", r"semantic kernel", r"autogen", r"crew ?ai", r"dspy", r"haystack", r"spring ai"],
    "AI coding assistants / AI-assisted development": [r"copilot", r"cursor\b", r"claude code", r"ai[- ](assisted|powered) (development|coding|tools)", r"ai (coding|developer) tools", r"codeium", r"windsurf", r"tabnine", r"ai tools"],
    "ML frameworks (PyTorch, TensorFlow, scikit-learn)": [r"pytorch", r"tensorflow", r"keras", r"scikit[- ]learn", r"sklearn", r"xgboost", r"jax\b"],
    "Deep learning / neural networks": [r"deep learning", r"neural network", r"transformers?\b(?! (oil|power))", r"\bCNN\b", r"\bRNN\b"],
    "NLP": [r"\bNLP\b", r"natural language processing", r"\bNLU\b", r"text classification", r"named entity"],
    "Computer vision": [r"computer vision", r"image recognition", r"object detection", r"opencv", r"\bOCR\b"],
    "MLOps / LLMOps / model deployment": [r"mlops", r"llmops", r"mlflow", r"kubeflow", r"sagemaker", r"model (deployment|serving|monitoring)", r"model registry", r"feature store", r"vllm", r"triton", r"ollama"],
    "LLM evaluation, guardrails & observability": [r"\bevals?\b", r"evaluation (framework|pipeline)s?", r"guardrails", r"hallucinat", r"langsmith", r"langfuse", r"llm observability", r"red[- ]teaming"],
    "Fine-tuning & model training": [r"fine[- ]tun", r"\bLoRA\b", r"\bRLHF\b", r"model training", r"training (models|pipelines)"],
    "Data science / analytics / statistics": [r"data scien", r"statistic", r"predictive (model|analytics)", r"recommendation (engine|system)s?", r"forecasting"],
    "Data engineering for AI (pipelines, Spark, Databricks)": [r"databricks", r"\bspark\b", r"data pipelines?", r"\bETL\b", r"snowflake", r"airflow", r"data lake"],
    "Responsible AI / AI governance / EU AI Act": [r"responsible ai", r"ai governance", r"ai act", r"ai ethics", r"bias", r"explainab"],
    "AI product / AI strategy (management)": [r"ai strategy", r"ai roadmap", r"ai (adoption|transformation|initiatives?)", r"ai[- ](driven|first|native|enabled|powered) (products?|solutions?|features?|platform)"],
    "Speech / voice AI": [r"speech[- ]to[- ]text", r"text[- ]to[- ]speech", r"\bASR\b", r"\bTTS\b", r"voice ai", r"whisper"],
}

COMPILED = {t: [re.compile(p, re.IGNORECASE) for p in ps] for t, ps in TAXONOMY.items()}
# "AI" alone is case-sensitive to avoid matching e.g. "Aid", "Mail"
COMPILED["AI / ML (general mention)"][0] = re.compile(r"\bAI\b")
COMPILED["AI / ML (general mention)"][3] = re.compile(r"\bML\b")
COMPILED["NLP"][0] = re.compile(r"\bNLP\b")
COMPILED["MCP (Model Context Protocol)"][0] = re.compile(r"\bMCP\b")
COMPILED["RAG / retrieval / embeddings"][0] = re.compile(r"\bRAG\b")
COMPILED["Speech / voice AI"][2] = re.compile(r"\bASR\b")
COMPILED["Speech / voice AI"][3] = re.compile(r"\bTTS\b")

# These topics only count when the ad also mentions AI/ML somewhere, since the
# raw words (agents, prompts, bias, Spark, pipelines...) are ambiguous.
NEEDS_AI_CONTEXT = {
    "Prompt engineering", "AI agents & agentic workflows", "Responsible AI / AI governance / EU AI Act",
    "Data engineering for AI (pipelines, Spark, Databricks)", "LLM evaluation, guardrails & observability",
    "Fine-tuning & model training", "Data science / analytics / statistics", "MCP (Model Context Protocol)",
    "Deep learning / neural networks",
}


def snippet(text: str, m: re.Match, width: int = 110) -> str:
    s, e = max(0, m.start() - width), min(len(text), m.end() + width)
    return ("…" if s else "") + text[s:e].replace("\n", " ") + ("…" if e < len(text) else "")


def main() -> None:
    jobs = [json.loads(l) for l in JOBS.read_text(encoding="utf-8").splitlines() if l.strip()]
    jobs = [j for j in jobs if j.get("description")]
    general = COMPILED["AI / ML (general mention)"]

    topics = {t: {"count": 0, "by_category": Counter(), "jobs": []} for t in TAXONOMY}
    ai_jobs = 0
    ai_by_cat = Counter()
    for j in jobs:
        text = f"{j['title']}\n{' '.join(j.get('tech_stack', []))}\n{j['description']}"
        has_ai = any(p.search(text) for p in general) or any(
            p.search(text) for t in ("LLMs / Generative AI", "LLM providers & APIs (OpenAI, Anthropic, Gemini, Bedrock, Azure OpenAI)") for p in COMPILED[t]
        )
        if has_ai:
            ai_jobs += 1
            ai_by_cat.update(j.get("categories", []))
        for t, pats in COMPILED.items():
            if t in NEEDS_AI_CONTEXT and not has_ai:
                continue
            m = next((m for p in pats if (m := p.search(text))), None)
            if m:
                topics[t]["count"] += 1
                topics[t]["by_category"].update(j.get("categories", []))
                topics[t]["jobs"].append({"url": j["url"], "title": j["title"], "company": j["company"], "snippet": snippet(text, m)})

    cats = Counter(c for j in jobs for c in j.get("categories", []))
    result = {
        "total_jobs": len(jobs),
        "jobs_mentioning_ai": ai_jobs,
        "jobs_per_category": dict(cats),
        "ai_jobs_per_category": dict(ai_by_cat),
        "topics": {t: {**v, "by_category": dict(v["by_category"])} for t, v in sorted(topics.items(), key=lambda kv: -kv[1]["count"])},
    }
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = [
        "# AI topics in dev.bg job ads", "",
        f"- Job ads analysed: **{len(jobs)}**",
        f"- Ads mentioning AI/ML/LLMs: **{ai_jobs}** ({ai_jobs / max(len(jobs), 1):.0%})", "",
        "| Category | Ads | Ads mentioning AI |", "|---|---:|---:|",
        *[f"| {c} | {n} | {ai_by_cat.get(c, 0)} |" for c, n in cats.most_common()], "",
        "## Topics (number of ads)", "", "| Topic | Ads | % of AI ads |", "|---|---:|---:|",
        *[f"| {t} | {v['count']} | {v['count'] / max(ai_jobs, 1):.0%} |" for t, v in result["topics"].items() if v["count"]], "",
        "## Example mentions", "",
    ]
    for t, v in result["topics"].items():
        if not v["count"]:
            continue
        lines += [f"### {t} ({v['count']})", ""]
        lines += [f"- *{e['title']}* @ {e['company']}: {e['snippet']}" for e in v["jobs"][:5]]
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"{ai_jobs}/{len(jobs)} ads mention AI. Wrote {OUT_JSON.name} and {OUT_MD.name}")


if __name__ == "__main__":
    main()
