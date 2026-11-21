## Importation des modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import json, s3fs

np.random.seed(123)

## Importation des données
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "https://minio.lab.sspcloud.fr"})
CACHE = "vgounot/diffusion"

with fs.open(f"{CACHE}/gcloud_emeutes_all.json", "r", encoding="utf-8") as f:
    body = json.load(f)

data = pd.DataFrame(body) #read_json ne fonctionne pas car le json est "imbriqué" donc je crée une dataframe qui garde les dictionnaires de second niveau

data["lat"] = data["geo"].apply(lambda x: x["latitude"])
data["long"] = data["geo"].apply(lambda x: x["longitude"]) 
#On utilise la fonction apply pour appliquer une fonction à chaque élément d'une colonne
#On a maintenant deux colonnes qui nous donnent la localisation exacte des émeutes

## Nettoyage préalable

#On retire les données manquantes si jamais il y en a (et seulement si c'est la latitude ou la longitude qui manque)
data = data.dropna(subset=["lat", "long"])
#On retire aussi les Outre-mer sinon on aura des points partout dans le monde et ce sera illisible
data = data[(data["lat"]>=41.3)&(data["lat"]<=51.2)&(data["long"]>=-5.2)&(data["long"]<=9.7)]

## Importation du fond de carte

url_fond_de_carte = ("https://minio.lab.sspcloud.fr/projet-cartiflette/production/"
       "provider=IGN/dataset_family=ADMINEXPRESS/"
       "source=EXPRESS-COG-CARTO-TERRITOIRE/year=2022/"
       "administrative_level=DEPARTEMENT/crs=4326/FRANCE_ENTIERE=France/"
       "vectorfile_format=geojson/territory=metropole/simplification=50/raw.geojson")

departements = gpd.read_file(url_fond_de_carte)
departements = departements[~departements["INSEE_DEP"].str.startswith("97")] 
#On retire les Outre-mer sinon la carte ne va ressembler à rien
departements = departements.to_crs(2154) #On passe en projection Lambert 93

## Création des points

points = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data["long"], data["lat"]), crs=4326)
points = points.to_crs(2154) #On passe en projection Lambert 93

## Projection des points sur la carte

#Ici, je ne vois pas comment faire la jointure. On va donc superposer le fond de carte et les points
fig, ax = plt.subplots(figsize=(12,12))
departements.plot(ax=ax, color="white", edgecolor="black")
ax.set_axis_off()
ax.set_title("Répartition des émeutes sur le territoire français en 2026")
points.plot(ax=ax, color="red", markersize=10, legend=True, legend_kwds={"label": "Emeutes"})
plt.savefig("Carte_émeutes_2026.png")
plt.show()


