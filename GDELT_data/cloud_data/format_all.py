'''
ce script regroupe les resultats par fenetres du script req_all_bywindows dans un meme fichier json
'''

import json, s3fs
from datetime import date, timedelta


# parametres date
d, end_date = date(2026, 3, 1), date(2026, 11, 10)
MAX_DAYS = 30

# parametres stockage
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})
CACHE = "vgounot/diffusion"

events = {}
while d <= end_date:
    e = min(d + timedelta(days=MAX_DAYS - 1), end_date)
    path = f"{CACHE}/{d}_{e}.json"
    with fs.open(path, "r", encoding="utf-8") as f:
        rows = json.load(f)
    print(d, e, len(rows), "lignes")
    d = e + timedelta(days=1)
    for ev in rows:
        events[ev["id"]] = ev
    d = e + timedelta(days=1)

with fs.open(f"{CACHE}/gcloud_emeutes_all.json", "w", encoding="utf-8") as f:
    json.dump(list(events.values()), f, ensure_ascii=False)
