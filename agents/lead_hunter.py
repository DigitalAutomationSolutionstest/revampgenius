from utils.site_analyzer import analyze_website
from utils.report_generator import generate_report
from utils.email_generator import generate_email

def lead_hunter_agent(url: str) -> dict:
    analysis_results = analyze_website(url)
    if "error" in analysis_results:
        return {"error": analysis_results["error"]}

    report, score, is_obsolete = generate_report(url, analysis_results)

    result = {
        "url": url,
        "report": report,
        "score": score
    }

    if is_obsolete:
        email = generate_email(report)
        result["email"] = {
            "subject": "Un consiglio amichevole per il tuo sito 😉",
            "body": email
        }

    return result
