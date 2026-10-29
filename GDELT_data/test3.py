import json


with open("resultat.json", encoding="utf-8") as f:
    body = json.load(f)

for e in body["data"]:
    print(e["event_date"], e["geo"].get("location"), "—", e["title"])