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
for k in r[1].keys():
    print(k, r[1][k])

# On GARDE
# GLOBALEVENTID
# SQLDATE
# Actor[1/2]Code
# Actor[1/2]Name ----(à voir)
# Actor[1/2]Type[1/2/3]Code
# EventBaseCode = 145 (145=emeutes) (filtre)
# NumArticles (difficilement exploitable)
# AvgTone ----(à voir)
# Actor[1, 2]Geo_FeatureID
# ActionGeo_FeatureID
# ActionGeo_[Lat, Long]
# ActionGeo_CountryCode (filtre)
# ActionGeo_FullName
# ActionGeo_ADM1Code (région)
# ActionGeo_ADM2Code (ville)
# ActionGeo_Type (Précision géographique de l'encodage)
# SOURCEURL