'''
ce script regroupe de fonctions permettant une requete googlecloud bigquery en passant par un
compte de services
stockage : format parquet, via s3://vgounot/diffusion/

config :
    pip install google-cloud-bigquery db-dtypes
    "GDELT_BIGQUERY_KEY" : clé json associée à un compte de services en var d'environnement

warning :
    BigQuery Storage module not found, fetch data with the REST endpoint instead
'''
import os, json, s3fs
from google.cloud import bigquery
from google.oauth2 import service_account

fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})


def estimation_donnees_scannees(req, client):
    """
    estimation cout donnée scannée pour une requete sql donnée
    entrée :
    req, la requete à estimer
    client, le lien avec le compte de service
    sortie :
    le nombre d'octets scannés
    """
    cfg = bigquery.QueryJobConfig(
        dry_run=True,
        use_query_cache=False)
    job = client.query(req, job_config=cfg)
    estim = job.total_bytes_processed
    print(f"{estim / 1e9:.2f} Go lus")
    return estim


def requete_bigquery(req, limite=10**11, path="vgounot/diffusion/2023_gcloud_emeutes.parquet"):
    '''
    requete via Google BigQuery si le volume de données scannées est acceptable et si la requete
    n'a pas déjà été effectuée auparavant
    entrée :
    req, la requete
    limite=10**11, la limite de données scannées à ne pas dépasser pour faire la requete
    path=(...), la destination fs du fichier résultat, à modifier pour reproduire l'extraction
    '''
    if fs.exists(path):
        print(f"Cette requête a déjà été effectuée et son résultat a été stocké à des fins de reproductibilité.\nLe résultat est disponible au format parquet à l'adresse {path}.")
    else:
        # config BigQuery
        info = json.loads(os.environ.get("GDELT_BIGQUERY_KEY"))  # clé en var d'environnement
        creds = service_account.Credentials.from_service_account_info(info)
        client = bigquery.Client(project=info["project_id"], credentials=creds)

        scan = estimation_donnees_scannees(req, client)
        if scan < limite:
            df = client.query(req).to_dataframe()
            with fs.open(path, "wb") as f:
                df.to_parquet(f, index=False)
            print(f"L'estimation des données scannées est acceptable.\nLe résultat est disponible au format parquet à l'adresse {path}.")
        else:
            print(f"L'estimation des données scannées dépasse {limite} octets.")
