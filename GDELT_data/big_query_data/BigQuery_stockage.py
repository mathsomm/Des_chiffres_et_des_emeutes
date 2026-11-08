import s3fs
import json
import pandas as pd


fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})

MY_BUCKET = "vgounot"
FILE_PATH_S3 = f"{MY_BUCKET}/diffusion/20:10:26_gdelt_emeutes.json"

# Import
with fs.open(FILE_PATH_S3, 'r', encoding="utf-8") as file_in:
    r = json.load(file_in)

# tests affichage, ici la donnée 0 du fichier json
for k in r[0].keys():
    print(k, r[0][k])