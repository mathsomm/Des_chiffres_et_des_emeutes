'''
script avec des fonctions pour importer successivement plusieurs pages de 100 évènements d'une meme
fenetre temporelle de 30 jours, et les aggréger dans un même fichier JSON

config :
"GDELT_API_KEY" : clé API GDELT Cloud en var d'environnement

attention : end_date ne doit pas etre trop recent (5 jours par exemple, pour que les données aient
bien été traitées complètement dans la base gcloud)

dans l'idéal, pour minimiser le nombre de requêtes nécessaires, MAX_DAYS = 30
'''

import os, json, time, requests, s3fs
from datetime import date, timedelta

MAX_DAYS = 30

# parametres stockage
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

# parametres requetes
base_params = {
    "country": "France",
    "category": "Riots",
    "limit": 100,
    "sort": "recent"
}


def req_page(params):
    '''
    requete une page de 100 lignes selon les parametres définis par params
    
    entrée :
    params, les paramètres de la requête
    sortie :
    req.json(), le résultat de la requête au format JSON 
    '''
    # config
    key = os.environ.get("GDELT_API_KEY")  # clé en var d'environnement
    url = "https://gdeltcloud.com/api/v2/events"
    headers = {"Authorization": "Bearer "+key}

    req = requests.get(url, headers=headers, params=params)
    req.raise_for_status()
    time.sleep(6.5)  # 10 requêtes/minute maximum
    return req.json()


def req_window(start, end, base_params):
    '''
    requete itérativement une fenetre entre les dates start et end, page par page, selon les params
    définis dans base_params
    
    entrée :
    start, la date du début de la fenêtre
    end, la date de fin de la fenêtre
    base_params, la base de paramètres de la requête
    sortie :
    l'aggrégation des différentes pages requêtées, au format d'une liste d'évènements au format JSON
    prérequis :
    (start, end) forme une fenetre d'au plus 30 jours (inclus)
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


def requete_gcloud(
    base_params,
    start_date=date(2026, 3, 1),
    end_date=date(2026, 11, 10),
    cache="vgounot/diffusion"
):
    '''
    requête les fenêtres successivement en partant de start_date jusqu'à end_date puis les stocke,
    avec également le résultat agrégé

    entrée :
    base_params, la base de paramètres de la requête
    start_date=date(2026, 3, 1), la date de départ de la requête
    end_date=date(2026, 11, 10), la date d'arrivée de la requête
    cache="vgounot/diffusion", un chemin de dossiers de fs pour stocker les résultats
    intermédiaires et finaux des requêtes, à modifier pour reproduire l'extraction
    sortie :
    (aucune), stockage du résultat de la requête dans f"{cache}/gcloud_emeutes_all.json"
    '''
    d = start_date
    events = {}
    while d <= end_date:
        e = min(d + timedelta(days=MAX_DAYS - 1), end_date)
        path = f"{cache}/{d}_{e}.json"
        if fs.exists(path):
            with fs.open(path, "r", encoding="utf-8") as f:
                rows = json.load(f)
        else:
            rows = req_window(d, e, base_params)
            with fs.open(path, "w", encoding="utf-8") as f:
                json.dump(rows, f, ensure_ascii=False)
        print(f"entre les dates {d} et {e}, {len(rows)} évènements ont été requêtés")
        for ev in rows:
            events[ev["id"]] = ev
        d = e + timedelta(days=1)
    path = f"{cache}/gcloud_emeutes_all.json"
    with fs.open(path, "w", encoding="utf-8") as f:
        json.dump(list(events.values()), f, ensure_ascii=False)
        print(f"Le résultat est disponible au format JSON à l'adresse {path}.")

