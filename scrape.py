# scraper.py
import csv
import time
from dataclasses import dataclass
from typing import List
import requests
from bs4 import BeautifulSoup

@dataclass
class ScrapeConfig:
    url: str
    user_agent: str = "Mozilla/5.0 (compatible; SimpleScraper/1.0; +https://example.com/bot)"
    timeout: int = 20
    retries: int = 3
    backoff: float = 1.5
    output_csv: str = "output.csv"

def fetch_html(cfg: ScrapeConfig) -> str:
    headers = {"User-Agent": cfg.user_agent, "Accept": "text/html,application/xhtml+xml"}
    last_err = None
    delay = 1.0
    for _ in range(cfg.retries):
        try:
            resp = requests.get(cfg.url, headers=headers, timeout=cfg.timeout)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            last_err = e
            time.sleep(delay)
            delay *= cfg.backoff
    raise SystemExit(f"Failed to fetch {cfg.url}: {last_err}")

def parse_paragraphs(html: str) -> List[str]:
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find_all("p")
    # Clean text: strip, collapse spaces, skip empties
    cleaned = []
    for p in paragraphs:
        text = " ".join(p.get_text(separator=" ").split()).strip()
        if text:
            cleaned.append(text)
    return cleaned

def save_csv(rows: List[str], path: str) -> None:
    # Save as a single column named "Content"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Content"])
        for item in rows:
            writer.writerow([item])

def main():
    cfg = ScrapeConfig(url="https://www.communityhealthpartners.org/find-a-provider?page=12")  # <- replace with your target
    html = fetch_html(cfg)
    data = parse_paragraphs(html)
    save_csv(data, cfg.output_csv)
    print(f"Saved {len(data)} rows to {cfg.output_csv}")

if __name__ == "__main__":
    main()
