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

# authentification
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

with fs.open("vgounot/analyseemeutes-d76c10827b8e.json", "rb") as f:
    info = json.load(f)

creds = service_account.Credentials.from_service_account_info(info)
client = bigquery.Client(project=info["project_id"], credentials=creds)

# paramètres requete depuis 2023
sql = """
SELECT 
    GLOBALEVENTID, SOURCEURL, SQLDATE, 
    Actor1CountryCode, Actor1Name, Actor1Type1Code, Actor1Type2Code, Actor1Type3Code, 
    Actor2CountryCode, Actor2Name, Actor2Type1Code, Actor2Type2Code, Actor2Type3Code, 
    NumArticles, AvgTone, 
    Actor1Geo_FeatureID, Actor2Geo_FeatureID, ActionGeo_FeatureID,
    ActionGeo_Type, ActionGeo_CountryCode, ActionGeo_FullName, ActionGeo_ADM1Code, ActionGeo_ADM2Code, ActionGeo_Lat, ActionGeo_Long
FROM 
    `gdelt-bq.gdeltv2.events_partitioned`
WHERE _PARTITIONDATE >= @d0 
  AND EventBaseCode = '145'
  AND ActionGeo_CountryCode = 'FR'
"""

job_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("d0", "DATE", "2023-01-01"),
    ]
)

# estimation cout donnée scannée
cfg = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False,
                              query_parameters=job_config.query_parameters)
job = client.query(sql, job_config=cfg)
print(f"{job.total_bytes_processed / 1e9:.2f} Go lus")

# requete si coût acceptable 
if job.total_bytes_processed < 10**11 :
    # df = client.query(sql, job_config=job_config).to_dataframe() # à décommenter pour effectuer la requete
    print(df.head())
    PATH = "vgounot/diffusion/2023_gcloud_emeutes.parquet"
    with fs.open(PATH, "wb") as f:
        df.to_parquet(f, index=False)
