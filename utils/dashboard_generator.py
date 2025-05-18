import json
import pandas as pd

def generate_dashboard(json_path="sitehunter_log.json", html_out="sitehunter_dashboard.html", excel_out="sitehunter_results.xlsx"):
    with open(json_path) as f:
        data = json.load(f)

    rows = []
    for item in data:
        row = {
            "URL": item["url"],
            "Obsoleto": item["is_obsolete"],
            "No SSL": item["flags"].get("no_ssl", False),
            "Usa <table>": item["flags"].get("uses_table", False),
            "Font tag": item["flags"].get("uses_font_tag", False),
            "Marquee": item["flags"].get("uses_marquee", False),
            "No Viewport": item["flags"].get("no_viewport", False),
            "Errore": item["flags"].get("error", False),
            "Categoria": item["flags"].get("category", "generico")
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_html(html_out, index=False)
    df.to_excel(excel_out, index=False)
    print(f"📊 Dashboard HTML → {html_out}")
    print(f"📊 Excel esportato → {excel_out}")
