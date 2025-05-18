import requests
from bs4 import BeautifulSoup
import tldextract

def analyze_website(url: str) -> dict:
    try:
        response = requests.get(url, timeout=10)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as e:
        return {"error": f"Errore durante l'accesso al sito: {e}"}

    title = soup.title.string.strip() if soup.title else "Nessun titolo"
    has_ssl = url.startswith("https://")
    outdated_design = detect_outdated_design(soup)
    meta_tags = bool(soup.find("meta"))
    mobile_friendly = detect_mobile_friendly(soup)
    favicon = bool(soup.find("link", rel="icon"))

    domain = tldextract.extract(url).domain

    return {
        "site": url,
        "domain": domain,
        "title": title,
        "uses_ssl": has_ssl,
        "has_meta_tags": meta_tags,
        "has_favicon": favicon,
        "mobile_friendly": mobile_friendly,
        "outdated_design": outdated_design
    }

def detect_outdated_design(soup):
    fonts = soup.find_all("font")
    tables = soup.find_all("table")
    marquee = soup.find_all("marquee")
    return bool(fonts or tables or marquee)

def detect_mobile_friendly(soup):
    viewport = soup.find("meta", attrs={"name": "viewport"})
    return viewport is not None
