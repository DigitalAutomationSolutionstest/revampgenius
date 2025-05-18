import re
import requests
from bs4 import BeautifulSoup

# Placeholder per scraping email
def find_emails(url: str) -> list:
    try:
        response = requests.get(url, timeout=10)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # Estrai tutto il testo visibile dalla pagina
        text = soup.get_text()
        
        # Cerca email con regex
        emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text))
        
        # Filtra email tipo info@facebook.com o roba da CDN
        emails = [email for email in emails if not is_blacklisted(email)]

        return emails
    except Exception as e:
        print(f"Errore nella ricerca email: {e}")
        return []

def is_blacklisted(email: str) -> bool:
    domain_blacklist = ["facebook.com", "instagram.com", "cloudflare.com"]
    return any(domain in email for domain in domain_blacklist)
