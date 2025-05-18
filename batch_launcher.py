import csv
from agents.lead_hunter import lead_hunter_agent
from agents.outreach_bot import outreach_bot_agent
from agents.form_scraper_bot import form_scraper_bot
from utils.email_scraper import find_emails

def process_url(url: str):
    if not url.startswith("http"):
        url = "http://" + url
    print(f"\n🚀 Analisi sito: {url}")
    
    data = lead_hunter_agent(url)
    if "error" in data:
        print(f"❌ Errore analisi: {data['error']}")
        return
    
    outreach_bot_agent(data)
    # Se non trova email, prova con form
    if "email" in data and not find_emails(url):
        form_scraper_bot(data)

def run_batch(csv_path="target_sites.csv"):
    with open(csv_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                url = row[0].strip()
                if url:
                    process_url(url)

if __name__ == "__main__":
    run_batch()
