from GT_data.Google_trends import Google_Trends
import s3fs
import json
import pandas as pd
from trendspy import Trends # ATTENTION !!!!
import matplotlib.pyplot as plt


 #------------ GOOGLE TRENDS ---------

 # -- Choix des mots -- 
G_trend = Google_Trends()
mots_contexte = ["Emeute", "violences urbaines"] #, "manifestation", "violence", 
mots_acteurs = ["casseurs"]
mots_actions = ["saccage", 'pillage']
mots_matériel = ["mortier", "LBD"]
mots_de_recherche = mots_contexte+mots_acteurs + mots_actions + mots_matériel

# -- Récuperer Data -- 
#df = G_trend.get_data(mots_de_recherche, "today 5-y")
#print(df.info())
#print(df.head(), "\n\n\n")
#G_trend.plot(df, ["mean"])


# --------- GDELT ---------------------

# -- Settings --
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})
MY_BUCKET = "vgounot"

# -- Import --
FILE_PATH_S3 = f"{MY_BUCKET}/diffusion/gcloud_emeutes_all.json"
with fs.open(FILE_PATH_S3, 'r', encoding="utf-8") as file_in:
    df_GDELT_small = pd.read_json(file_in)
    print("\n\n\n GDEL bigQuery small", df_GDELT_small.info())
    print(df_GDELT_small.head())


FILE_PATH_S3 = f"{MY_BUCKET}/diffusion/2023_gcloud_emeutes.parquet"

with fs.open(FILE_PATH_S3, 'rb', encoding="utf-8") as file_in:
    df_GDELT_large = pd.read_parquet(file_in)
print("\n\n\n GDEL bigQuery gros", df_GDELT_large.info())
print(df_GDELT_large.head())





