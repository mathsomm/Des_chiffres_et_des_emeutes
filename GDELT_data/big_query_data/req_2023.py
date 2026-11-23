'''
ce script est une requete googlecloud bigquery en passant par un compte de services
requete : données émeutes, en France, depuis janvier 2023
stockage : format parquet, via s3://vgounot/diffusion/

config :
    pip install google-cloud-bigquery db-dtypes
    nécessite une clé json associée à un compte de services : s3://vgounot/ (accès perso)

warning :
    BigQuery Storage module not found, fetch data with the REST endpoint instead
'''
import s3fs
import json
from google.cloud import bigquery
from google.oauth2 import service_account


# authentification (attention, à modifier, pour la reproductibilité info est innacessible au public)
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})
with fs.open("vgounot/analyseemeutes-d76c10827b8e.json", "rb") as f:
    info = json.load(f)
creds = service_account.Credentials.from_service_account_info(info)
client = bigquery.Client(project=info["project_id"], credentials=creds)


def estimation_donnees_scannees(req):
    """
    estimation cout donnée scannée pour une requete sql donnée
    entrée :
    req, la requete à estimer
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


def requete(req, limite=10**11):
    '''
    requete via Google BigQuery si le volume de données scannées est acceptable et si la requete
    n'a pas déjà été effectuée auparavant
    entrée :
    req, la requete
    limite=10**11, la limite de données scannées à ne pas dépasser pour faire la requete
    '''
    PATH = "vgounot/diffusion/2023_gcloud_emeutes.parquet"
    if fs.exists(PATH):
        print(f"Cette requête a déjà été effectuée et son résultat a été stocké à des fins de reproductibilité.\nLe résultat est disponible au format parquet à l'adresse {PATH}.")
    else:
        scan = estimation_donnees_scannees(req)
        if scan < limite:
            df = client.query(req).to_dataframe()
            with fs.open(PATH, "wb") as f:
                df.to_parquet(f, index=False)
            print(f"L'estimation des données scannées est acceptable.\nLe résultat est disponible au format parquet à l'adresse {PATH}.")
        else:
            print(f"L'estimation des données scannées dépasse {limite} octets.")
