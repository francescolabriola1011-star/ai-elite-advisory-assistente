#!/usr/bin/env python3
"""Unisce conoscenza/*.md e faq.json in conoscenza.txt, il file al link unico.
Gira da solo su GitHub a ogni modifica (workflow conoscenza.yml)."""
import json, re, datetime
from pathlib import Path

root = Path(__file__).resolve().parent.parent
parti = []
for f in sorted((root / "conoscenza").glob("*.md")):
    t = re.sub(r"<!--.*?-->", "", f.read_text(encoding="utf-8"), flags=re.S).strip()
    if t:
        parti.append(t)
faq = json.loads((root / "faq.json").read_text(encoding="utf-8"))
righe = ["DOMANDE FREQUENTI DEI CONSULENTI E RISPOSTE UFFICIALI"]
for g in faq["gruppi"]:
    for v in g["voci"]:
        righe.append(f"D: {v['d']}\nR: {v['r']}")
parti.append("\n\n".join(righe))
oggi = datetime.date.today().strftime("%d/%m/%Y")
testo = f"CONOSCENZA DI BRACCIO DESTRO, AI ELITE ADVISORY. Versione del {oggi}.\n\n" + "\n\n".join(parti) + "\n"
(root / "conoscenza.txt").write_text(testo, encoding="utf-8")
# Stessa conoscenza in JSON: la legge l'azione del GPT su ChatGPT.
(root / "conoscenza.json").write_text(json.dumps({"versione": oggi, "conoscenza": testo}, ensure_ascii=False), encoding="utf-8")
print(f"conoscenza.txt: {len(testo)} caratteri, {len(parti)} parti")
