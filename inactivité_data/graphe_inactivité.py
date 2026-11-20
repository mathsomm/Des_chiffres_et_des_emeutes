##Installation et importation des modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

np.random.seed(123)

##Importation du jeu de données

data=pd.read_csv("/home/onyxia/work/Projet_Python_2A/inactivité_data/inactivité_jeunes_departement.csv", sep=";", na_values=["N/A - résultat non disponible"])
#na_values est un argument qui permet de considérer certaines inscriptions dans les données comme des valeurs manquantes

##Nettoyage
data = data.dropna() #On retire la donnée manquante sur Mayotte, qui est la seule à manquer, on peut s'en passer

##Calcul du taux d'inactivité
data["Taux d'inactivité chez les jeunes"] = 100-data["Taux d'activité des 15-24 ans 2023"]

##Création d'une carte 
url = ("https://minio.lab.sspcloud.fr/projet-cartiflette/production/"
       "provider=IGN/dataset_family=ADMINEXPRESS/"
       "source=EXPRESS-COG-CARTO-TERRITOIRE/year=2022/"
       "administrative_level=DEPARTEMENT/crs=4326/FRANCE_ENTIERE=France/"
       "vectorfile_format=geojson/territory=metropole/simplification=50/raw.geojson")
#J'ai visiblement un problème avec cartiflette pour faire le fond de carte, je lis donc le fichier avec geopandas

departements=gpd.read_file(url)
print(departements.columns)

departements = departements[~departements["INSEE_DEP"].str.startswith("97")] #On retire les Outre-Mer pour ne pas avoir de problème avec la projection
departements = departements.to_crs(2154) #On passe en projection Lambert 93

carte = departements.merge(data, left_on="INSEE_DEP", right_on="Code", how="left")

var = "Taux d'inactivité chez les jeunes"

graphe = carte.plot(column=var, cmap="YlOrRd", edgecolor="white", legend=True, legend_kwds={"label":"Taux d'inactivité chez les 15-24 ans en 2023 (en %)"})
graphe.set_axis_off()
graphe.set_title("Taux d'inactivité chez les 15-24 ans par département")
plt.savefig("carte_inactivite_jeunes.png")
plt.show()