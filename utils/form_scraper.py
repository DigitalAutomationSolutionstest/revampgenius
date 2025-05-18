import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_contact_forms(url: str) -> list:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")
        contact_forms = []

        for form in forms:
            form_str = str(form).lower()
            if "contact" in form_str or "message" in form_str or "contattaci" in form_str:
                action = form.get("action") or url
                method = form.get("method", "post").lower()
                inputs = form.find_all("input") + form.find_all("textarea")
                form_fields = {
                    inp.get("name"): inp.get("type", "text")
                    for inp in inputs if inp.get("name")
                }
                full_action = urljoin(url, action)
                contact_forms.append({
                    "url": full_action,
                    "method": method,
                    "fields": form_fields
                })

        return contact_forms
    except Exception as e:
        print(f"❌ Errore parsing form su {url}: {e}")
        return []
