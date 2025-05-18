import os
from dotenv import load_dotenv
import resend

from utils.email_scraper import find_emails
from utils.supabase_logger import log_to_supabase
from utils.cost_tracker import log_cost_estimate

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")
SENDER_EMAIL = "revamp@miniaiapps.tech"

def outreach_bot_agent(data: dict):
    url = data["url"]
    email_data = data.get("email")
    report = data["report"]

    if not email_data:
        print(f"⛔ Sito non obsoleto → nessuna email inviata per {url}")
        return

    print(f"🔍 Cerco email da contattare su {url}...")
    emails = find_emails(url)

    if not emails:
        print(f"❌ Nessuna email trovata su {url}")
        return

    for email in emails:
        try:
            response = resend.Emails.send({
                "from": SENDER_EMAIL,
                "to": email,
                "subject": email_data["subject"],
                "html": email_data["body"]
            })
            print(f"✅ Email inviata a {email}")

            # Log su Supabase + costo stimato
            log_to_supabase(email, url, report)
            log_cost_estimate(email)

        except Exception as e:
            print(f"⚠️ Errore invio email a {email}: {e}")
