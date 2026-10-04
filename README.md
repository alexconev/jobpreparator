# jobpreparator

Scrapes dev.bg job ads, extracts the AI skills employers ask for, and turns them into a study plan.

```
scraper/scrape_devbg.py        polite, resumable scraper (all listing pages → every job ad)
analysis/extract_ai_topics.py  AI-topic extraction over the scraped ads
data/jobs.jsonl                scraped ads, one JSON object per line (reusable dataset)
data/scrape.log                log of the last scrape
data/ai_topics.json            per-topic counts, matching ads and snippets
data/ai_topics_report.md       readable summary of the AI topics
preparation_program.md         3-month AI preparation program built from the findings
```

## Re-running

```bash
python3 scraper/scrape_devbg.py              # fetches only ads not already in data/jobs.jsonl
python3 scraper/scrape_devbg.py --delay 5    # even slower crawl
python3 analysis/extract_ai_topics.py        # regenerate the topic report
```

The scraper waits 3–4.5 s between requests (`--delay`), backs off on 429/5xx, and
appends to `data/jobs.jsonl`, so an interrupted run can simply be restarted.

Each record has these fields: `url, title, company, location, posted, tech_stack[], description, categories[], scraped_at`.
