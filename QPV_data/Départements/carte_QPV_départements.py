## Importation des modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

## Importation des données

data = pd.read_csv("/home/onyxia/Projet_Python_2A/QPV_data/Départements/Nb_QPV départements.csv", sep=";", skiprows=2, dtype={"Code" : str})

## Nettoyage des données

data = data[~data["Code"].str.startswith("97")] #On retire les Outre-mer

## Création d'une carte

url_fond_de_carte = ("https://minio.lab.sspcloud.fr/projet-cartiflette/production/"
       "provider=IGN/dataset_family=ADMINEXPRESS/"
       "source=EXPRESS-COG-CARTO-TERRITOIRE/year=2022/"
       "administrative_level=DEPARTEMENT/crs=4326/FRANCE_ENTIERE=France/"
       "vectorfile_format=geojson/territory=metropole/simplification=50/raw.geojson")

départements = gpd.read_file(url_fond_de_carte)

départements = départements[~départements["INSEE_DEP"].str.startswith("97")]
départements.to_crs(2154)

carte = départements.merge(data, left_on="INSEE_DEP", right_on="Code", how="left")

variable = "Quartiers prioritaires de la politique de la ville 2024 : Nombre de QPV sur le territoire"

graphe = carte.plot(column=variable, cmap="YlOrRd", edgecolor="white", legend=True, legend_kwds={"label": "Nombre de QPV"})
graphe.set_axis_off()
graphe.set_title("Nombre de QPV dans chaque département en 2024")
plt.savefig("Carte_QPV_départements.png")
plt.show()
