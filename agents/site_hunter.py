import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import csv
import json
from utils.dashboard_generator import generate_dashboard

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def google_search(query: str, max_results: int = 50) -> list:
    search_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    res = requests.get(search_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http") and not any(b in href for b in ["bing.com", "microsoft.com", "youtube.com"]):
            domain = urlparse(href).netloc
            if domain not in links:
                links.append(href)
        if len(links) >= max_results:
            break
    return links

def is_obsolete(url: str) -> tuple:
    try:
        res = requests.get(url, timeout=8, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        score = 0
        flags = {}

        if not url.startswith("https://"):
            score += 1
            flags["no_ssl"] = True

        if soup.find_all("table"):
            score += 1
            flags["uses_table"] = True

        if soup.find_all("font"):
            score += 1
            flags["uses_font_tag"] = True

        if soup.find("marquee"):
            score += 1
            flags["uses_marquee"] = True

        if not soup.find("meta", attrs={"name": "viewport"}):
            score += 1
            flags["no_viewport"] = True

        is_old = score >= 2
        return is_old, flags
    except Exception:
        return False, {"error": True}

def site_hunter_agent(query: str, category="generico", max_results: int = 30):
    print(f"🔍 Cerco siti per: {query}")
    urls = google_search(query, max_results)

    valid_targets = []
    details_log = []

    for url in urls:
        is_old, flags = is_obsolete(url)
        if is_old:
            valid_targets.append(url)
        flags["category"] = category
        details_log.append({
            "url": url,
            "is_obsolete": is_old,
            "flags": flags
        })

    with open("target_sites.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for url in valid_targets:
            writer.writerow([url])

    with open("sitehunter_log.json", "w") as f:
        json.dump(details_log, f, indent=2)

    generate_dashboard()
    print(f"\n✅ Trovati {len(valid_targets)} siti obsoleti su {len(urls)} analizzati.")
    print("📁 Salvati: CSV + JSON + HTML + Excel")
