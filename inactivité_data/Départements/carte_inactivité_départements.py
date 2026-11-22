##  Importation des modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

np.random.seed(123)

## Importation du jeu de données

data=pd.read_csv("/home/onyxia/Projet_Python_2A/inactivité_data/Départements/inactivité_jeunes_departement.csv", sep=";", dtype={"Code":str})
#Le code est ici mis en string pour que l'on puisse retirer les Outre-mer dont le code commence par 97

##  Nettoyage

data = data[~data["Code"].str.startswith("97")] #On retire les Outre-mer pour éviter des problèmes avec la carte
data["Taux d'activité des 15-24 ans 2023"] = data["Taux d'activité des 15-24 ans 2023"].astype(float)
#On s'assure que le type des données est numérique pour que l'on puisse faire des calculs dessus

##  Calcul du taux d'inactivité

data["Taux d'inactivité chez les jeunes"] = 100-data["Taux d'activité des 15-24 ans 2023"]

##  Création d'une carte 

url = ("https://minio.lab.sspcloud.fr/projet-cartiflette/production/"
       "provider=IGN/dataset_family=ADMINEXPRESS/"
       "source=EXPRESS-COG-CARTO-TERRITOIRE/year=2022/"
       "administrative_level=DEPARTEMENT/crs=4326/FRANCE_ENTIERE=France/"
       "vectorfile_format=geojson/territory=metropole/simplification=50/raw.geojson")
#J'ai visiblement un problème avec cartiflette pour faire le fond de carte, je lis donc le fichier avec geopandas

departements=gpd.read_file(url)

departements = departements[~departements["INSEE_DEP"].str.startswith("97")] #On retire les Outre-Mer pour ne pas avoir de problème avec la projection
departements = departements.to_crs(2154) #On passe en projection Lambert 93

carte = departements.merge(data, left_on="INSEE_DEP", right_on="Code", how="left")

petite_couronne = carte[carte["INSEE_DEP"].isin(["75", "92", "93", "94"])]

var = "Taux d'inactivité chez les jeunes"

vmin = carte[var].min()
vmax = carte[var].max()

fig = plt.figure(figsize=(16,10))

ax1 = fig.add_axes([0.03, 0.08, 0.58, 0.84])
ax2 = fig.add_axes([0.35, 0.65, 0.20, 0.25])

xmin, ymin, xmax, ymax = petite_couronne.total_bounds
ax2.set_xlim(xmin-50000, xmax+50000)
ax2.set_ylim(ymin-50000, ymax+50000)

graphe = carte.plot(column=var, ax=ax1, cmap="YlOrRd", vmin=vmin, vmax=vmax, edgecolor="black", legend=True, legend_kwds={"label":"Taux d'inactivité chez les 15-24 ans en 2023 (en %)"})
graphe.set_axis_off()
graphe.set_title("Taux d'inactivité chez les 15-24 ans par département")
petite_couronne.plot(column=var, ax=ax2, cmap="YlOrRd", vmin=vmin, vmax=vmax, edgecolor="black" )
ax2.set_axis_off()
plt.savefig("carte_inactivite_départements.png")
plt.show()