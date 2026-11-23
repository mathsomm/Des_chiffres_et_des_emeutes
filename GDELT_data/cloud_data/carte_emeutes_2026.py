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
data["pays"] = data["geo"].apply(lambda x: x["country"])
data["loc"] = data["geo"].apply(lambda x: x["location"])
#On utilise la fonction apply pour appliquer une fonction à chaque élément d'une colonne
#On a maintenant deux colonnes qui nous donnent la localisation exacte des émeutes

## Nettoyage préalable

#On retire les données manquantes si jamais il y en a (et seulement si c'est la latitude ou la longitude qui manque)
data = data.dropna(subset=["lat", "long"])
#On retire aussi les Outre-mer sinon on aura des points partout dans le monde et ce sera illisible
data = data[(data["lat"]>=41.3)&(data["lat"]<=51.2)&(data["long"]>=-5.2)&(data["long"]<=9.7)]

data = data[data["pays"]=="France"] #On a remarqué un point un Espagne que l'on retire
data = data.dropna(subset=["loc"]) #On retire aussi les points non précis qui atterrissent tous au même endroit dans la Creuse

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

## Agrégation des émeutes par département

emeutes_département = gpd.sjoin(points, departements[["INSEE_DEP", "geometry"]], how="left", predicate="within")
# Cela permet d'attribuer un département à chaque de la carte
emeutes_département = emeutes_département.dropna(subset=["INSEE_DEP"])
# Il y a un point en dehors de la France sur la carte précédente, donc je préfère retirer la donnée pour la suite

émeutes_agrégé = emeutes_département["INSEE_DEP"].value_counts()
#On compte le nombre de fois où chaque département apparaît pour avoir le nombre d'événements récents par départements

carte2 = departements.merge(émeutes_agrégé, on="INSEE_DEP", how="left")
carte2["count"] = carte2["count"].fillna(0)
#Lorsque la valeur de count n'a pas été trouvée, c'est qu'il n'y a pas eu d'émeutes

petite_couronne = carte2[carte2["INSEE_DEP"].isin(["75", "92", "93", "94"])]

variable = "count"

vmin = carte2["count"].min()
vmax = carte2["count"].max()

fig = plt.figure(figsize=(16,10))

ax1 = fig.add_axes([0.03, 0.08, 0.58, 0.84])
ax2 = fig.add_axes([0.35, 0.65, 0.20, 0.25])

graphe2 = carte2.plot(column=variable, ax=ax1, cmap="YlOrRd", vmin=vmin, vmax=vmax, edgecolor="black", legend=True, legend_kwds={"label" : "Nombre d'émeutes dans le département en 2026"})
petite_couronne.plot(column=variable, ax=ax2, cmap="YlOrRd", vmin=vmin, vmax=vmax, edgecolor="black")
graphe2.set_axis_off()
graphe2.set_title("Nombre d'émeutes dans chaque département en 2026")
xmin, ymin, xmax, ymax = petite_couronne.total_bounds
ax2.set_xlim(xmin-50000, xmax+50000)
ax2.set_ylim(ymin-50000, ymax+50000)
ax2.set_axis_off()
plt.savefig("Carte_émeutes_2026_départements.png")
plt.show()

## Importation des données à propos des autres paramètres
data_inactivité = pd.read_csv("/home/onyxia/Projet_Python_2A/inactivité_data/Départements/inactivité_jeunes_departement.csv", sep=";", dtype={"Code":str})
data_QPV = pd.read_csv("/home/onyxia/Projet_Python_2A/QPV_data/Départements/part_population_QPV_département.csv", skiprows=2, sep=";", dtype={"Code":str})
data_inactivité = data_inactivité[~data_inactivité["Code"].str.startswith("97")]
data_inactivité["Taux d'activité des 15-24 ans 2023"] = data_inactivité["Taux d'activité des 15-24 ans 2023"].astype(float)
data_inactivité["inactivité"] = 100-data_inactivité["Taux d'activité des 15-24 ans 2023"]

## Jointure entre toutes les données et histogrammes
émeutes_agrégé = émeutes_agrégé.to_frame()
émeutes_agrégé = émeutes_agrégé.reindex(departements["INSEE_DEP"], fill_value="0") #On complète avec 0 émeutes pour les départements non concernés
émeutes_agrégé = émeutes_agrégé.reset_index() #On met au format DataFrame pour pouvoir faire les jointures

data1 = émeutes_agrégé.merge(data_inactivité, left_on="INSEE_DEP", right_on="Code", how="left")
data_tout = data1.merge(data_QPV, on="Code", how="left")

data_émeutes = data_tout[data_tout["count"].astype(float)>0]
data_non_émeutes = data_tout[data_tout["count"].astype(float)==0]

#On fait l'histogramme sur l'inactivité

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(32,14))

ax1.bar(data_émeutes["INSEE_DEP"], data_émeutes["inactivité"], color="firebrick", edgecolor="black")
ax1.set_title("Départements avec au moins une émeute")

ax2.bar(data_non_émeutes["INSEE_DEP"], data_non_émeutes["inactivité"], color="steelblue", edgecolor="black")
ax2.set_title("Départements sans émeute")

for ax in (ax1, ax2):
    ax.set_xlabel("Département")
    ax.set_ylabel("Taux d'inactivité des jeunes")
    ax.tick_params(axis="x", rotation=90, labelsize=9)   # On verticalise les étiquettes                                  
    ax.legend()

plt.savefig("Histogramme inactivité.png")

# On fait de même un histogramme avec les QPV
variable = "QPV - Quartiers prioritaires de la politique de la ville 2024 : Part de la population municipale résidant en QPV"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(32,14))

ax1.bar(data_émeutes["INSEE_DEP"], data_émeutes[variable], color="firebrick", edgecolor="black")
ax1.set_title("Départements avec au moins une émeute")

ax2.bar(data_non_émeutes["INSEE_DEP"], data_non_émeutes[variable], color="steelblue", edgecolor="black")
ax2.set_title("Départements sans émeute")

for ax in (ax1, ax2):
    ax.set_xlabel("Département")
    ax.set_ylabel("Part de la population vivant en QPV")
    ax.tick_params(axis="x", rotation=90, labelsize=9)   # On verticalise les étiquettes                                  
    ax.legend()

plt.savefig("Histogramme QPV.png")
