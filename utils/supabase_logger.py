import os
import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_to_supabase(email: str, url: str, report: dict):
    try:
        payload = {
            "sent_to": email,
            "site_url": url,
            "report_data": report,
            "sent_at": datetime.datetime.utcnow().isoformat()
        }
        response = supabase.table("outreach_logs").insert(payload).execute()
        if response.status_code == 201:
            print(f"📦 Log salvato su Supabase per {email}")
        else:
            print(f"⚠️ Errore log Supabase: {response.status_code}")
    except Exception as e:
        print(f"❌ Eccezione durante il log su Supabase: {e}")
