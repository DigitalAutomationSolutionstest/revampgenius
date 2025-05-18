#!/bin/bash

echo "🔥 RevampGenius Lead Machine"
echo "----------------------------"

read -p "📌 Inserisci la query (es: ristoranti Roma): " QUERY
read -p "📁 Inserisci la categoria (es: ristoranti): " CATEGORY

echo ""
echo "🎯 Lancio SiteHunter per: \"$QUERY\" (categoria: $CATEGORY)"
python3 -c "from agents.site_hunter import site_hunter_agent; site_hunter_agent(query='$QUERY', category='$CATEGORY')"

echo ""
echo "⚙️  Avvio batch AI su siti trovati..."
python3 batch_launcher.py

echo ""
echo "✅ Completato. Controlla:"
echo "- target_sites.csv"
echo "- sitehunter_log.json"
echo "- sitehunter_results.xlsx"
echo "- sitehunter_dashboard.html"
