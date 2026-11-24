# Projet_Python_2A

## Descrition
Ces dernières années, les émeutes en France ont vu leur fréquence augmenter, avec les Gilets Jaunes d'abord en 2017-2018, les émeutes liées à la mort de Nahel en 2023 ensuite, ou encore les émeutes en Nouvelle-Calédonie en 2024. Ces émeutes ont causé des pertes assurantielles importantes, notamment pour les acteurs assurant les collectivités, qui se répercutent aujourd'hui sur une hausse des prix des contrats avec une police émeute, ce qui rend difficile pour certaines communes de s'assurer face à ce risque émeute.

Une réforme législative entrant en vigueur en janvier 2027 impose donc aux assureurs de couvrir les émeutes dans les mêmes conditions que les contrats incendie, et pour compenser prévoit la mise en place d’un fonds de réassurance garanti par l’Etat. Du point de vue des réassureurs, pour aider les cédantes à composer avec cette réforme et statuer quant au maintien des contrats via la réassurance traditionnelle, il faut prédire le risque émeute pour les prochaines années.

## Données

### GDELT:
Descritption : 
- Le GDELT Project met à disposition une base de données ouverte qui scanne en continu les médias du monde entier (presse en ligne, agences, web) et transforme chaque article en événement structuré.
- GDELT Cloud propose une base nettoyée à partir de la base du GDELT Project, soumise à une licence. Nous avons eu l'autorisation de paratager les données extraites et les résultats dans le cadre de ce projet.

Objectif : La parution d'articles sur le sujet des émeutes est le média le plus précis afin de déterminer où et quand se sont déroulés ces évenements.

### Google Trends
Description : Google Trends permet de connaitre le nombre de requêtes sur internet pour un mot clef.

Objectif : avoir un aperçu temporel du ressenti d'émeutes en France. 
Dans un but de vérifier les informations récupérées avec GDELT, Google Trends sert à caractériser l'intérêt des francais pour les emeutes à travers des recherches comme "Mortier", "LBD", "casseurs", ... 

### Observatoire des territoires
Description : L'observatoire des territoires contient des données socio-démographiques utiles pour notre analyse. Nous nous sommes intéressés aux données suivante, à la maille départementale.
- taux d'activité chez les 15/24
- part de la population vivant en QPV

## Dépendances
Les dépendances (avec des numéros de version stricts pour la reproductibilité) sont présentes dans le fichier `requirements.text`. Elles peuvent être installées avec la commande suivante dans le terminal.

`pip install -r requirements.txt`

## Configuration
Le projet peut être exécuté sans varibles d'environnement additionnelles. Néanmoins, dans le cas où l'on voudrait reproduire l'extraction des bases intermédiaires, il est nécessaire de fixer dans les variables d'environnement deux clé d'API :
- `"GDELT_BIGQUERY_KEY"` : la clé JSON d'un compte de service associé à un projet [ici](https://console.cloud.google.com/bigquery)
- `"GDELT_API_KEY"` : la clé API pour GDELT Cloud (les requêtes à disposition via le "free plan" sont suffisantes)

## Execution
Pour lancer le projet, ouvrir le notebook `Projet_main.ipynb`, qui constitue le rapport du projet.

## Structure du dépot


## Auteurs
Victor GOUNOT, Mathias SOMMIER, Tristan MARCOUX
