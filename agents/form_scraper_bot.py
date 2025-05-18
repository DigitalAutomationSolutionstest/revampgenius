import requests
from utils.form_scraper import find_contact_forms
from utils.cost_tracker import log_cost_estimate

def form_scraper_bot(data: dict):
    url = data["url"]
    email_data = data.get("email")

    if not email_data:
        print(f"⛔ Sito non obsoleto → nessun form da usare su {url}")
        return

    forms = find_contact_forms(url)
    if not forms:
        print(f"❌ Nessun form contatto rilevato su {url}")
        return

    for form in forms:
        try:
            payload = {}
            for field_name, field_type in form["fields"].items():
                lname = field_name.lower()
                if "name" in lname:
                    payload[field_name] = "RevampGenius"
                elif "email" in lname:
                    payload[field_name] = "revamp@miniaiapps.tech"
                elif any(k in lname for k in ["message", "msg", "text", "body"]):
                    payload[field_name] = email_data["body"]
                else:
                    payload[field_name] = "N/A"

            response = requests.post(form["url"], data=payload, timeout=10)

            if response.status_code in [200, 202]:
                print(f"✅ Messaggio inviato tramite form su {form['url']}")
                log_cost_estimate(email_target=f"form:{form['url']}")
                return
            else:
                print(f"⚠️ Form trovato ma invio fallito: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Errore invio form {form['url']}: {e}")
