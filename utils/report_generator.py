def generate_report(url: str, analysis_results: dict) -> tuple:
    negative_count = 0
    comments = []

    # Commenti predefiniti
    positive = {
        "design": "Moderno e accattivante.",
        "mobile": "Perfettamente responsive.",
        "ux": "Navigazione chiara e intuitiva.",
        "performance": "Caricamento rapido.",
        "seo": "Struttura SEO di base ben implementata.",
        "visual": "Look fresco e attuale."
    }

    ironic = {
        "design": "Sembra uscito da FrontPage 2003.",
        "mobile": "Mobile-friendly? Forse nel 2005.",
        "ux": "Dove cliccare? Boh.",
        "performance": "Più lento di una lumaca con la sciatica.",
        "seo": "SEO? Cos'è?",
        "visual": "Sembra che il CSS abbia preso una vacanza."
    }

    # Valutazione categorie
    for category in ["design", "mobile", "ux", "performance", "seo", "visual"]:
        status = analysis_results.get(category, False)
        if not status:
            negative_count += 1
            comment = ironic[category]
        else:
            comment = positive[category]
        comments.append(f"- **{category.capitalize()}:** {comment}")

    # Score e soglia obsolescenza
    score = max(0, 10 - (negative_count * 2))
    obsolete = negative_count >= 2

    # Genera report Markdown
    report = f"### Analisi sito: {url}\n\n" + "\n".join(comments)
    report += f"\n\n**Punteggio:** {score}/10"
    report += f"\n🧠 *{'Consigliamo un revamp AI con consegna in 72h. Fidati, gli utenti ringrazieranno.' if obsolete else 'Questo sito è già al top! Ottimo lavoro!'}*"

    return report, score, obsolete
