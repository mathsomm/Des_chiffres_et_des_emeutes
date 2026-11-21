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

var = "Taux d'inactivité chez les jeunes"

graphe = carte.plot(column=var, cmap="YlOrRd", edgecolor="white", legend=True, legend_kwds={"label":"Taux d'inactivité chez les 15-24 ans en 2023 (en %)"})
graphe.set_axis_off()
graphe.set_title("Taux d'inactivité chez les 15-24 ans par département")
plt.savefig("carte_inactivite_départements.png")
plt.show()