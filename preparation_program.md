# 3-Month AI Preparation Program (built from dev.bg job ads, Oct 2026)

## 1. What the market asks for

Source: 372 unique ads scraped on 2026-10-04 from dev.bg back-end (288), front-end (122),
full-stack (79) and IT-management (22) categories. Some ads appear in several categories.
**150 ads (40%) mention AI**: back-end 113, front-end 63, full-stack 48, management 13.
Raw data: `data/jobs.jsonl`, `data/ai_topics_report.md`.

| # | Topic (what the ads actually say) | Ads | Typical wording |
|---|---|---:|---|
| 1 | **AI-assisted development**: Claude Code, Cursor, Copilot, Codex | 72 | "Daily hands-on use of AI coding agents… and the judgment to reject what they hand you"; "spec-driven development: writing specs that AI tools can execute against" |
| 2 | **Agents and agentic workflows**: orchestration, tool calling, state, multi-step flows | 53 | "conceptual understanding of AI agent orchestration (state machines, loop handling, tool-calling boundaries) rather than just basic prompt generation" |
| 3 | **LLM APIs and providers**: OpenAI, Anthropic, Bedrock, Vertex, Azure OpenAI | 35 | "LLM APIs, tool calling, streaming, structured output" |
| 4 | **GenAI/LLM fundamentals**: tokens, context windows, non-determinism, hallucination | 32 | "Good understanding of how LLMs behave to debug them" |
| 5 | **Prompt engineering and context engineering** | 28 | "set an agent up to succeed: prompt engineering, a clear spec, the right tools and tests wired in" |
| 6 | **RAG**: embeddings, chunking, re-ranking, vector DBs (pgvector, Pinecone, Weaviate, Qdrant) | 15 | "RAG in production: embeddings, vector search, chunking and re-ranking" |
| 7 | **AI strategy and adoption** (lead/manager roles) | 15 | "measure the impact of AI adoption… DORA, AI-assisted PR merge rates, agent output acceptance rates" |
| 8 | **MCP** (Model Context Protocol), A2A | 9 | "MCP server: tool design, descriptions, schemas… that an LLM can use correctly on the first try" |
| 9 | **Evals, guardrails and observability**: Langfuse, LangSmith, RAGAS | 9 | "automated suites that catch a regression when a prompt, a model or a retrieval step changes" |
| 10 | **LLM frameworks**: LangChain, LangGraph, LlamaIndex, CrewAI, PydanticAI | 7 | "stateful agentic workflows… using frameworks like LangGraph" |
| 11 | **AI security**: prompt injection, data leakage, OWASP LLM / Agentic Top 10 | ~6 | "least-privilege access, human-in-the-loop checkpoints, action logging" |
| 12 | **LLMOps and cost**: LLM gateway, routing, caching, token budgets, model selection | ~5 | "evaluating AI models based on capabilities, cost, and suitability" |
| 13 | ML basics: PyTorch, TF, Hugging Face, fine-tuning, NLP, document AI/VLMs, OCR | ~11 | Mostly "a plus" and Python-only roles |

**Takeaways**
- The most common requirement by far is **using AI coding agents well, while staying responsible for quality**:
  reviewing, testing and correcting their output. Ads name the specific tools (Claude Code 23 ads, Cursor 26, Copilot 26).
- Next comes **building LLM features into products**: agents, tool calling, RAG, structured output and MCP. This is
  the topic that makes a candidate stand out.
- **Production concerns** (evals, observability, guardrails, security, cost) appear in senior ads and are where
  most candidates are weak, so they are a good differentiator.
- Classic ML (training models, PyTorch) is rarely required for these developer roles. It gets a light touch here.

## 2. How the program is organized

- **About 8–10 h/week** for 12 weeks: roughly 1/3 reading and watching, 2/3 building.
- Each month ends with a **portfolio artifact**.
- Language: Python for the AI parts (most ads and tooling), plus one port to your main stack
  (Java → Spring AI / LangChain4j, .NET → Semantic Kernel / Microsoft Agent Framework, TS → Vercel AI SDK).
- Running capstone: **"Job Match Assistant"**, built on top of `data/jobs.jsonl` from this repo.
  You already own the dataset, and it touches every topic in the table above.

### Core books (pick up once, used across months)
- **Chip Huyen – *AI Engineering* (O'Reilly, 2025)**: the main textbook for the whole program.
- **Jay Alammar & Maarten Grootendorst – *Hands-On Large Language Models* (O'Reilly, 2024)**: for intuition about how LLMs work.
- **John Berryman & Albert Ziegler – *Prompt Engineering for LLMs* (O'Reilly, 2024)**.
- Optional, for depth: **Sebastian Raschka – *Build a Large Language Model (From Scratch)* (Manning, 2024)**;
  **Paul Iusztin & Maxime Labonne – *LLM Engineer's Handbook* (Packt, 2024)**.

---

## Month 1: Foundations and AI-assisted development (topics 1, 4, 5)

### Week 1: How LLMs work (just enough to debug them)
- Topics: tokens and tokenization, context window, temperature and sampling, non-determinism, hallucination,
  training vs. inference, pre-training vs. instruction tuning vs. RLHF, model families and model tiers.
- Video: Andrej Karpathy, *Intro to Large Language Models* (1 h) and *Deep Dive into LLMs like ChatGPT*.
- Video: 3Blue1Brown, *Neural Networks* series (the chapters on transformers and attention).
- Read: *Hands-On LLMs* ch. 1–3; *AI Engineering* ch. 1–2.
- Do: call one LLM API from a script. Count tokens, then change the temperature and observe how the output varies.

### Week 2: Prompt and context engineering
- Topics: system prompts, few-shot examples, chain-of-thought, XML/markdown structuring, structured output
  (JSON schema), prompt templates, context engineering (what to put in the window and what to leave out).
- Read: *Prompt Engineering for LLMs* (main chapters); *AI Engineering* ch. 5.
- Course: Anthropic's *Prompt Engineering Interactive Tutorial* (GitHub `anthropics/prompt-eng-interactive-tutorial`);
  DeepLearning.AI *ChatGPT Prompt Engineering for Developers* (short course).
- Docs: the prompt-engineering guides from Anthropic and OpenAI.
- Do: extract structured fields from 50 job ads in `jobs.jsonl` (seniority, stack, AI requirements) into
  validated JSON (Pydantic).

### Week 3: AI coding agents in daily work (the #1 requirement)
- Topics: Claude Code / Cursor / Copilot agent mode, project memory files (CLAUDE.md, rules),
  custom commands and skills, plan-then-execute, running agents in parallel (git worktrees), hooks, giving the agent tests to verify against.
- Read: Claude Code documentation and Anthropic's *Claude Code best practices* post; Cursor docs (rules, agent);
  GitHub Copilot docs (agent mode, coding agent).
- Do: build a small feature in your main stack *only* through an agent. Keep a log of what it got wrong
  and how you caught it. Ads mention this skill repeatedly, so be ready to talk about it in interviews.

### Week 4: Spec-driven development and reviewing AI output
- Topics: writing specs that an agent can execute against, test-first with agents, reviewing AI-generated
  code (security, performance, hidden coupling), AI in code review and test generation, responsible use
  (secrets, IP, data protection).
- Read: Simon Willison's blog (AI-assisted programming tag); GitHub `spec-kit` docs (spec-driven development).
- Topic: DORA research on AI-assisted software development, i.e. how teams measure the impact.
- **Month 1 artifact**: a repo with a feature built through an agent: spec → plan → implementation → tests,
  plus a short write-up "What I delegate to AI and what I check myself".

---

## Month 2: Building LLM features (topics 2, 3, 6, 8, 10)

### Week 5: LLM APIs in production code
- Topics: messages API, streaming (SSE/WebSockets to a frontend), tool/function calling, structured outputs,
  retries, rate limits, timeouts, prompt caching, multi-provider abstraction.
- Docs: Anthropic API docs (tool use, streaming, prompt caching), OpenAI API docs; AWS Bedrock /
  Azure OpenAI / Vertex AI quick-starts (pick the cloud you use).
- Course: DeepLearning.AI *Building Systems with the ChatGPT API*.
- Do: a FastAPI (or your stack) endpoint that streams answers about a job ad to a small web UI.

### Week 6: RAG
- Topics: embeddings, chunking strategies, vector search (pgvector first, then Pinecone/Qdrant/Weaviate as an
  alternative), hybrid search (BM25 + vectors), re-ranking, metadata filtering, citations.
- Read: *AI Engineering* ch. 6; *Hands-On LLMs* ch. 8 (semantic search and RAG).
- Course: DeepLearning.AI *Building and Evaluating Advanced RAG*; Pinecone Learning Center articles.
- Do (capstone step 1): RAG over `jobs.jsonl` in Postgres + pgvector. Questions like
  "Which companies want LangGraph?" should get answers with links to the ads.

### Week 7: Agents
- Topics: the agent loop, tool design, planning, memory (short- and long-term), state machines, handling loops and
  stopping, multi-agent patterns, human-in-the-loop approval gates, workflows vs. agents.
- Read: Anthropic *Building Effective Agents* (essential); Lilian Weng *LLM Powered Autonomous Agents*;
  *AI Engineering* ch. 6 (agents section); Google/Kaggle *Agents* whitepaper.
- Course: Hugging Face *AI Agents Course* (free); DeepLearning.AI *AI Agents in LangGraph*;
  Microsoft *AI Agents for Beginners* (GitHub).
- Do: first write an agent loop by hand (no framework), then build the same thing in LangGraph. Compare the two.

### Week 8: MCP and frameworks
- Topics: MCP architecture (hosts, clients, servers; tools, resources, prompts), transports (stdio and streamable HTTP),
  auth, writing tool descriptions an LLM uses correctly, A2A protocol (awareness); framework landscape:
  LangChain/LangGraph, LlamaIndex, PydanticAI, CrewAI; per stack: Spring AI / LangChain4j, Semantic Kernel.
- Docs: modelcontextprotocol.io (spec and SDK quick-starts); FastMCP docs.
- Course: DeepLearning.AI *MCP: Build Rich-Context AI Apps with Anthropic*.
- Do (capstone step 2): an **MCP server over your jobs dataset** (`search_jobs`, `get_job`, `skills_gap`).
  Connect it to Claude Code or Cursor and watch where the model misreads your tools.
- **Month 2 artifact**: the Job Match Assistant. RAG + agent + MCP server; give it your CV and it returns matching
  ads plus a gap analysis.

---

## Month 3: Production quality, security and leadership (topics 7, 9, 11, 12)

### Week 9: Evals
- Topics: why "vibe checks" are not enough, building eval datasets, code-based checks vs. LLM-as-judge,
  RAG metrics (faithfulness, context precision/recall), regression evals in CI, error analysis.
- Read: *AI Engineering* ch. 3–4 (evaluation); Hamel Husain *Your AI Product Needs Evals*;
  *What We've Learned From A Year of Building with LLMs* (applied-llms.org); Eugene Yan *Patterns for
  Building LLM-based Systems & Products*.
- Tools: RAGAS, promptfoo, or a pytest-based suite you write yourself.
- Do: 30–50 test questions for the capstone, run in CI on every prompt or model change.

### Week 10: Observability, guardrails and LLMOps
- Topics: tracing (Langfuse / LangSmith / OpenTelemetry GenAI conventions), cost and latency monitoring,
  LLM gateway (multi-provider routing, fallbacks, rate limits, caching, token budgets), model selection by
  cost and capability, prompt versioning, canary/A-B rollouts, content moderation.
- Read: *AI Engineering* ch. 9–10; *LLM Engineer's Handbook* (LLMOps chapters, optional).
- Do: add Langfuse tracing and a cost dashboard to the capstone. Try routing simple queries to a cheaper model.

### Week 11: AI security and governance
- Topics: prompt injection (direct and indirect), data leakage, excessive agency, least privilege for tools,
  human approval gates, audit logging, securing MCP servers, AI supply chain; EU AI Act basics (risk
  categories, obligations for deployers).
- Read: **OWASP Top 10 for LLM Applications (2025)**; OWASP *Agentic AI – Threats and Mitigations*.
- Course: DeepLearning.AI *Red Teaming LLM Applications*.
- Do: attack your own capstone. Plant an injected instruction in a job ad, see whether the agent follows it,
  fix it, then add the attack to your evals.

### Week 12: Wrap-up and interview preparation
- Engineers: polish the capstone (README, architecture diagram, eval results, trade-offs). Prepare
  stories: "an agent wrote bad code, and here is how I caught it", "how I'd design RAG for X", "how I'd make an
  agent safe enough to move money".
- Leads/managers (topic 7, if relevant): AI adoption playbook, i.e. team guidelines for AI tools, quality gates
  for AI-generated code, metrics (DORA, PR cycle time, agent acceptance rate), cost governance.
  Topic: *Accelerate* (Forsgren, Humble, Kim) plus the DORA AI reports for the measurement side.
- Optional stretch (for Python AI roles): fine-tuning basics with LoRA (Hugging Face *LLM Course*),
  document AI / VLMs / OCR, classic ML with scikit-learn.

---

## Checklist: you are ready when you can…
- [ ] Explain tokens, context windows, sampling and hallucination, and debug a misbehaving prompt.
- [ ] Show a real feature built with an AI coding agent, and explain how you verified it.
- [ ] Build streaming, tool-calling, structured-output LLM features in your main stack.
- [ ] Build RAG end to end (chunking → embeddings → pgvector → re-rank → cited answer).
- [ ] Write an agent without a framework, and explain when to use LangGraph instead.
- [ ] Ship an MCP server whose tools a model uses correctly.
- [ ] Run an eval suite in CI and show a regression it caught.
- [ ] Name the OWASP LLM top risks and show the mitigations in your own project.
- [ ] Discuss the cost/latency/quality trade-offs of choosing a model.

*To refresh the analysis later: re-run the scraper and `analysis/extract_ai_topics.py`, then compare the topic table.*
