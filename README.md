# Projet_Python_2A

## Pitch
On analyse souvent les émeutes comme une explosion soudaine et imprévisible. Est ce vraiment le cas ? Il est possible que les territoires avec un taux d'inactivité plus élevé subissent plus frequemment ces désagréments. L'objectif de ce projet Python est ainsi d'explorer les dynamiques des émeutes et d'identifier les principaux drivers qui accompagnent ces évenements.

À travers un schema de collecte, de nettoyage et d'analyse de données, nous étudirons les corrélations entre présence de quartiers prioritaires (QPV), le taux d'inactivité et les émeutes. 

La difficulté première du projet étant d'obtenir des renseignements fiables sur la présence d'emeutes en France, nous avons choisi de croiser deux sources de données complémentaires: GDELT, qui capture l'activité médiatique et événementielle mondiale en temps réel, et Google Trends, qui reflète l'attention directe des citoyens à travers leurs requêtes de recherche.

### Problématique


## Description
Projet réalisé en plusieurs parties. Nous avons à cœur de garder un approche claire et transparente:
- Récupération
- Données problématiques (valeurs manquantes, outliers, réalisation des join)
- Modélisation
- Conclusion

### Contexte 


### Données
- Modeliser les emeutes
Deux bases de données sont utilisées pour caractériser au mieux ce phénomène:

-> GDELT:
Descritption: GDELT est une base de données ouverte qui scanne en continu les médias du monde entier (presse en ligne, agences, web) et transforme chaque article en événement structuré. 
Objectif: La parution d'articles sur le sujet des émeutes est le média le plus précis afin de déterminer où et quand se sont déroulés ces évenements.


-> Google Trends
Description: Google Trends permet de connaitre le nombre de requêtes pour un mot clef.
Objectif: avoir un aperçu temporel du ressenti d'émeutes en France. 
Dans un but de vérifier les informations récupérées avec GDELT, Google Trends sert à caractériser l'intérêt des francais pour les emeutes à travers des recherches comme "Mortier", "LBD", "casseurs", ... 


