import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Prezzi modello GPT-4o su OpenRouter
# Fonte: https://openrouter.ai/docs/pricing
PRICING = {
    "openai/gpt-4o": {
        "input_per_1k": 0.005,   # $ per 1000 token input
        "output_per_1k": 0.015   # $ per 1000 token output
    }
}

def estimate_cost(input_tokens=500, output_tokens=300, model="openai/gpt-4o"):
    price = PRICING.get(model)
    if not price:
        return 0.0

    cost = (input_tokens / 1000) * price["input_per_1k"] + (output_tokens / 1000) * price["output_per_1k"]
    return round(cost, 4)

def fetch_openrouter_balance():
    try:
        headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
        res = requests.get("https://openrouter.ai/api/v1/account/credits", headers=headers)

        if res.status_code == 200:
            data = res.json()
            return float(data.get("credits", 0))
        else:
            print(f"⚠️ Errore richiesta credito: {res.status_code}")
            return None
    except Exception as e:
        print(f"❌ Errore recupero crediti: {e}")
        return None

def log_cost_estimate(email_target, model="openai/gpt-4o"):
    cost = estimate_cost()
    credits = fetch_openrouter_balance()

    log_line = f"[{datetime.utcnow().isoformat()}] Email a {email_target} → Costo stimato: ${cost} – Crediti residui: ${credits if credits is not None else 'N/A'}"
    print(log_line)

    with open("outreach_cost_log.txt", "a") as f:
        f.write(log_line + "\n")
