## Importation des modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

np.random.seed(123)

## Importation du jeu de données

data = pd.read_csv("/home/onyxia/Projet_Python_2A/inactivité_data/activité_régions.csv", sep=";", skiprows=2, dtype={"Code": str})
#skiprows sert à sauter les deux premières du document qui viendraient polluer notre data frame

## Nettoyage des données

#On va se débarrasser des données sur les Outre-Mer car on ne pourra pas les inclure dans la carte
data = data[~data["Code"].str.startswith("0")]
#Ensuite, on met les données de taux d'activité dans un format numérique pour pouvoir faire des calculs
data["Taux d'activité des 15-24 ans 2023"]=data["Taux d'activité des 15-24 ans 2023"].astype(float)

## Calcul du taux d'inactivité 
data["Taux d'inactivité chez les 15-24 ans 2023"] = 100-data["Taux d'activité des 15-24 ans 2023"]

## Création d'une carte
url_fond_de_carte =  ("https://minio.lab.sspcloud.fr/projet-cartiflette/production/"
                      "provider=IGN/dataset_family=ADMINEXPRESS/"
                      "source=EXPRESS-COG-CARTO-TERRITOIRE/year=2022/"
                      "administrative_level=REGION/crs=4326/FRANCE_ENTIERE=France/"
                      "vectorfile_format=geojson/territory=metropole/simplification=50/raw.geojson")

#Je n'arrive pas à utiliser cartiflette, donc je vais l'ouvrir avec geopandas
regions = gpd.read_file(url_fond_de_carte)
regions = regions[~(regions["INSEE_REG"]<10)]
regions.to_crs(2154) #On projette sur du Lambert 93, comme préconisé dans le cours

regions["INSEE_REG"] = regions["INSEE_REG"].astype(str) 
#On passe le code INSEE des régions en string. Pour la jointure, c'est mieux...

carte = regions.merge(data, left_on="INSEE_REG", right_on="Code", how="left")

variable = "Taux d'inactivité chez les 15-24 ans 2023"

#On peut maintenanat faire la carte
graphe = carte.plot(column=variable, cmap="YlOrRd", edgecolor="white", legend=True, legend_kwds={"label": "Taux d'inactivité chez les 15-24 ans en 2023 (en %)"})
graphe.set_axis_off()
graphe.set_title("Taux d'inactivité chez les 15-24 ans par région")
#plt.savefig("carte_inactivité_régions.png")
plt.show
