## Importation des modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

## Importation des données

data = pd.read_csv("/home/onyxia/Projet_Python_2A/QPV_data/Départements/part_population_QPV_département.csv", sep=";", skiprows=2, dtype={"Code" : str})

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
départements = départements.to_crs(2154)

carte = départements.merge(data, left_on="INSEE_DEP", right_on="Code", how="left")

petite_couronne = carte[carte["INSEE_DEP"].isin(["75", "92", "93", "94"])]

variable = "QPV - Quartiers prioritaires de la politique de la ville 2024 : Part de la population municipale résidant en QPV"

fig = plt.figure(figsize=(16,10))

ax1 = fig.add_axes([0.03, 0.08, 0.58, 0.84])
ax2 = fig.add_axes([0.35, 0.65, 0.20, 0.25])

xmin, ymin, xmax, ymax = petite_couronne.total_bounds
ax2.set_xlim(xmin-50000, xmax+50000)
ax2.set_ylim(ymin-50000, ymax+50000)

vmin = carte[variable].min()
vmax = carte[variable].max()

graphe = carte.plot(column=variable, ax=ax1, cmap="YlOrRd", vmin=vmin, vmax=vmax, edgecolor="black", legend=True, legend_kwds={"label": "Part de la population vivant en QPV (en %)"})
petite_couronne.plot(column=variable, ax=ax2, cmap="YlOrRd", vmin=vmin, vmax=vmax, edgecolor="black")
graphe.set_axis_off()
graphe.set_title("Part de la population vivant en QPV dans chaque département en 2024")
ax2.set_axis_off()
plt.savefig("Carte_QPV_départements.png")
plt.show()
