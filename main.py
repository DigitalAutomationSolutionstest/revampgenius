from agents.lead_hunter import lead_hunter_agent
from agents.outreach_bot import outreach_bot_agent
from agents.form_scraper_bot import form_scraper_bot

def run():
    print("🚀 RevampGenius: AI Email Outreach Engine\n")
    url = input("👉 Inserisci l'URL del sito da analizzare: ").strip()
    
    if not url.startswith("http"):
        url = "http://" + url  # fallback se l’utente non inserisce schema

    print(f"\n🔍 Analizzo il sito: {url}")
    lead_output = lead_hunter_agent(url)
    
    if "error" in lead_output:
        print(f"❌ Errore nell’analisi: {lead_output['error']}")
        return
    
    print("\n📄 Report tecnico generato.")
    print(lead_output["report"])

    print("\n✍️ Email ironica generata.")
    print(lead_output["email_text"])

    print("\n📬 Cerco email e invio proposta...")
    emails = outreach_bot_agent(lead_output)
    if not emails:
        form_scraper_bot(lead_output)

if __name__ == "__main__":
    run()
