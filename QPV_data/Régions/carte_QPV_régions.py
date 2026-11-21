## Importation des modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd

np.random.seed(123)

## Importation des données

data = pd.read_csv("/home/onyxia/Projet_Python_2A/QPV_data/Régions/Nb_QPV_régions.csv", sep=";", skiprows=2, dtype = {"Code" : str})
#Mettre le code en string est utile car nous allons retirer les codes commençant par 0
#Si on laisse en float ou int, le 0 devant le code des Outre-Mer sera retiré

## Nettoyage des données

data = data[~data["Code"].str.startswith("0")] #On se sépare encore une fois des données des Outre-Mer

## Création d'une carte

url_fond_de_carte =  ("https://minio.lab.sspcloud.fr/projet-cartiflette/production/"
                      "provider=IGN/dataset_family=ADMINEXPRESS/"
                      "source=EXPRESS-COG-CARTO-TERRITOIRE/year=2022/"
                      "administrative_level=REGION/crs=4326/FRANCE_ENTIERE=France/"
                      "vectorfile_format=geojson/territory=metropole/simplification=50/raw.geojson")

#Je n'arrive pas à utiliser cartiflette donc je fais avec geopandas
regions=gpd.read_file(url_fond_de_carte)
regions.to_crs(2154) #On reprojette sur du Lambert 93, comme d'habitude
regions = regions[~(regions["INSEE_REG"]<10)] #On retire les Outre-Mer
regions["INSEE_REG"] = regions["INSEE_REG"].astype(str) #On passe les codes en str pour la jointure

carte = regions.merge(data, left_on="INSEE_REG", right_on="Code", how="left")

variable = "Quartiers prioritaires de la politique de la ville 2024 : Nombre de QPV sur le territoire" 

#Et on finit par la carte
graphe = carte.plot(column=variable, cmap="YlOrRd", edgecolor="white", legend=True, legend_kwds={"label" : "Nombre de QPV en 2024"})
graphe.set_axis_off()
graphe.set_title("Nombre de QPV en 2024 par région")
plt.savefig("carte_QPV_régions")
plt.show()


