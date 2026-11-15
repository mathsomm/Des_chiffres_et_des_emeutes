'''
script pour importer successivement plusieurs pages de 100 lignes d'une meme fenetre temporelle de
30 jours

attention : end_date ne doit pas etre trop recent
'''

import os, json, time, requests, s3fs
from datetime import date, timedelta


# parametres date
d, end_date = date(2026, 3, 1), date(2026, 11, 10)
MAX_DAYS = 30

# parametres stockage
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})
CACHE = "vgounot/diffusion"

# parametres requetes
key = os.environ.get("GDELT_API_KEY")
url = "https://gdeltcloud.com/api/v2/events"
headers = {"Authorization": "Bearer "+key}
base_params = {
    "country": "France",
    "category": "Riots",
    "limit": 100,
    "sort": "recent"
}


def req_page(params):
    '''
    requete une page de 100 lignes selon les parametres définis par params
    '''
    print("req")
    req = requests.get(url, headers=headers, params=params)
    req.raise_for_status()
    time.sleep(6.5)                                  # 10 requêtes/minute maximum
    return req.json()


def req_window(start, end):
    '''
    requete itérativement une fenetre entre les dates start et end, page par page, selon les params
    définis dans base_params
    prérequis : (start, end) forme une fenetre d'au plus 30 jours
    '''
    params = {**base_params, "date_start": start.isoformat(), "date_end": end.isoformat()}
    rows = []
    while True:
        body = req_page(params)
        rows += body["data"]
        cursor = body["pagination"]["next_cursor"]
        if not cursor:
            return rows
        params["cursor"] = cursor


while d <= end_date:
    e = min(d + timedelta(days=MAX_DAYS - 1), end_date)
    path = f"{CACHE}/{d}_{e}.json"
    if fs.exists(path):
        with fs.open(path, "r", encoding="utf-8") as f:
            rows = json.load(f)
    else:
        rows = req_window(d, e)
        with fs.open(path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)
    print(d, e, len(rows), "lignes")
    d = e + timedelta(days=1)
