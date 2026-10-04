#!/usr/bin/env python3
"""Polite scraper for dev.bg job listings.

Walks every paginated listing page of the configured categories, visits each
job ad and appends its description to data/jobs.jsonl (one JSON object per
line). The run is resumable: ads already present in the output file are
skipped, so re-running only fetches new ads.

Usage:
    python3 scraper/scrape_devbg.py                # all categories
    python3 scraper/scrape_devbg.py --delay 5      # slower (seconds between requests)
    python3 scraper/scrape_devbg.py --max-pages 1  # quick test
"""
import argparse
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

CATEGORIES = {
    "back-end-development": "https://dev.bg/company/jobs/back-end-development/",
    "front-end-development": "https://dev.bg/company/jobs/front-end-development/",
    "full-stack-development": "https://dev.bg/company/jobs/full-stack-development/",
    "it-management": "https://dev.bg/company/jobs/it-management/",
}
JOB_PREFIX = "https://dev.bg/company/jobads/"
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "data" / "jobs.jsonl"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) jobpreparator/1.0 (personal research; slow crawl)",
    "Accept-Language": "bg,en;q=0.8",
}


class Fetcher:
    def __init__(self, delay: float):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self._last = 0.0

    def get(self, url: str) -> str | None:
        for attempt in range(4):
            # Throttle: base delay plus jitter between *every* request.
            wait = self.delay + random.uniform(0, self.delay / 2) - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
            try:
                r = self.session.get(url, timeout=30)
            except requests.RequestException as e:
                print(f"  ! {e}; retrying", file=sys.stderr)
                time.sleep(30 * (attempt + 1))
                continue
            if r.status_code == 200:
                return r.text
            if r.status_code == 404:
                return None
            if r.status_code in (429, 500, 502, 503, 504):
                backoff = int(r.headers.get("Retry-After", 0) or 0) or 60 * (attempt + 1)
                print(f"  ! HTTP {r.status_code}; backing off {backoff}s", file=sys.stderr)
                time.sleep(backoff)
                continue
            print(f"  ! HTTP {r.status_code} for {url}", file=sys.stderr)
            return None
        return None


def listing_url(base: str, page: int) -> str:
    return base if page == 1 else f"{base}?_paged={page}"


def job_links(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    seen, links = set(), []
    for a in soup.select(f'a[href^="{JOB_PREFIX}"]'):
        href = a["href"].split("?")[0].split("#")[0]
        if href not in seen:
            seen.add(href)
            links.append(href)
    return links


def parse_job(url: str, html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    text = lambda el: el.get_text(" ", strip=True) if el else None
    header = soup.select_one(".single-job")
    desc = soup.select_one(".job_description") or soup.select_one(".single_job_listing")
    stack = soup.select_one(".tech-stack")
    return {
        "url": url,
        "title": text(soup.select_one("h1")),
        "company": text(header.select_one(".company-name")) if header else None,
        "location": text(header.select_one(".tags-wrap")) if header else None,
        "posted": text(soup.select_one("time")),
        "tech_stack": [i.get("title") for i in stack.find_all("img") if i.get("title")] if stack else [],
        "description": desc.get_text("\n", strip=True) if desc else None,
    }


def load_existing(path: Path) -> dict[str, dict]:
    jobs = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                j = json.loads(line)
                jobs[j["url"]] = j
    return jobs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--delay", type=float, default=3.0, help="min seconds between requests (default 3)")
    ap.add_argument("--max-pages", type=int, default=100, help="max listing pages per category")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--categories", nargs="*", default=list(CATEGORIES), choices=list(CATEGORIES))
    args = ap.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    existing = load_existing(args.out)
    fetcher = Fetcher(args.delay)

    # Phase 1: collect job URLs per category from all listing pages.
    url_cats: dict[str, list[str]] = {}
    for cat in args.categories:
        seen_in_cat: set[str] = set()
        for page in range(1, args.max_pages + 1):
            url = listing_url(CATEGORIES[cat], page)
            print(f"[list] {cat} page {page}")
            html = fetcher.get(url)
            if not html:
                break
            new = [l for l in job_links(html) if l not in seen_in_cat]
            if not new:  # past the last page the site returns no new ads
                break
            seen_in_cat.update(new)
            for l in new:
                url_cats.setdefault(l, []).append(cat)
        print(f"[list] {cat}: {len(seen_in_cat)} ads")

    # Phase 2: fetch every ad not yet stored.
    todo = [u for u in url_cats if u not in existing]
    print(f"[jobs] {len(url_cats)} unique ads, {len(todo)} new to fetch")
    with args.out.open("a", encoding="utf-8") as f:
        for i, url in enumerate(todo, 1):
            html = fetcher.get(url)
            if not html:
                continue
            job = parse_job(url, html)
            job["categories"] = url_cats[url]
            job["scraped_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            f.write(json.dumps(job, ensure_ascii=False) + "\n")
            f.flush()
            print(f"[jobs] {i}/{len(todo)} {job['title']} @ {job['company']}")

    print(f"Done. Output: {args.out}")


if __name__ == "__main__":
    main()
