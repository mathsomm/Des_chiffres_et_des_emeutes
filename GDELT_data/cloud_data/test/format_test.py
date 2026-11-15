import json

with open("resultat.txt", encoding="utf-8") as f:
    body = json.load(f)                    # le texte devient un dictionnaire Python

with open("resultat.json", "w", encoding="utf-8") as f:
    json.dump(body, f, ensure_ascii=False, indent=2)