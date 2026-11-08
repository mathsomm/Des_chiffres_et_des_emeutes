'''
ce script est un test de requete googlecloud bigquery en passant par un compte de services
requete : données émeutes, en France, 20 octobre 2026
stockage : format parquet, via s3://vgounot/diffusion/

config :
    pip install google-cloud-bigquery db-dtypes pandas
    nécessite une clé json associée à un compte de services : s3://vgounot/ (accès perso)

warning :
    BigQuery Storage module not found, fetch data with the REST endpoint instead
'''
import s3fs
import json
from google.cloud import bigquery
from google.oauth2 import service_account

# authentification
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

with fs.open("vgounot/analyseemeutes-d76c10827b8e.json", "rb") as f:
    info = json.load(f)

creds = service_account.Credentials.from_service_account_info(info)
client = bigquery.Client(project=info["project_id"], credentials=creds)

# paramètres requete
sql = """
SELECT *
FROM `gdelt-bq.gdeltv2.events_partitioned`
WHERE ActionGeo_CountryCode = 'FR'
AND EventBaseCode = '145'
AND _PARTITIONDATE BETWEEN @d0 AND @d1
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("d0", "DATE", "2026-10-20"),
        bigquery.ScalarQueryParameter("d1", "DATE", "2026-10-20"),
    ]
)

# estimation cout donnée scannée
cfg = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False,
                              query_parameters=job_config.query_parameters)
job = client.query(sql, job_config=cfg)
print(f"{job.total_bytes_processed / 1e9:.2f} Go lus")

# requete si coût acceptable
if job.total_bytes_processed < 10**8 :
    # df = client.query(sql, job_config=job_config).to_dataframe() # à décommenter pour effectuer la requete
    print(df.head())
    PATH = "vgounot/diffusion/2026-20-10_gcloud_emeutes.parquet"
    with fs.open(PATH, "wb") as f:
        df.to_parquet(f, index=False)
