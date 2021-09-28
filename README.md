# OC-DS-P3-Concevez_application_au_service_sante_publique
Formation OpenClassrooms - Parcours data scientist - Projet n°3 - Concevez une application au service de la santé publique

## Conception d’une application au service de la santé publique (phénylcétonurie) 

L'agence "Santé publique France" a lancé un appel à projets pour trouver des idées innovantes d’applications en lien avec l'alimentation. 

![P3_Presentation](https://user-images.githubusercontent.com/71518818/135096043-8d494e26-7c5f-4c6c-bf8c-13e9b5605376.png)

## Les données

Le jeu de données Open Food Fact est disponible sur le site officiel. Les variables sont définies à cette adresse: https://world.openfoodfacts.org/

## Objectifs

1) Traiter le jeu de données afin de repérer des variables pertinentes pour les traitements à venir. 
Automatiser ces traitements pour éviter de répéter ces opérations.
Le programme doit fonctionner si la base de données est légèrement modifiée (ajout d’entrées, par exemple).

2) Tout au long de l’analyse, produire des visualisations afin de mieux comprendre les données. Effectuer une analyse univariée pour chaque variable intéressante, afin de synthétiser son comportement.

L’appel à projets spécifie que l’analyse doit être simple à comprendre pour un public néophyte. Soyez donc attentif à la lisibilité : taille des textes, choix des couleurs, netteté suffisante, et variez les graphiques (boxplots, histogrammes, diagrammes circulaires, nuages de points…) pour illustrer au mieux votre propos.

3) Confirmer ou infirmer les hypothèses  à l’aide d’une analyse multivariée. Effectuer les tests statistiques appropriés pour vérifier la significativité des résultats.

4) Élaborer une idée d’application. Identifier des arguments justifiant la faisabilité (ou non) de l’application à partir des données Open Food Facts.

5) Rédiger un rapport d’exploration et pitcher votre idée durant la soutenance du projet.

## Idée d'application

L'idée d'application, avec test de faisabilité, portera sur une **aide** aux personnes **atteintes de phénylcétonurie**. 

En effet ces personnes doivent suivre un **régime hypoprotidique** très strict et quotidien tout en suivant une **alimentation saine et équilibrée** avec des produits peu transformés.

![P3_Phenylcetonurie](https://user-images.githubusercontent.com/71518818/135096547-49821dc0-5831-439f-82b5-969a5ff43838.png)

La pré-prototype de l'application sera dans un premier temps,  un **moteur de recommandation** : à partir de la recherche d'un produit, la liste des produits les plus sains classés par score (le nombre de g de protéines le plus faible possible, produit le plus sain donc nutri-score le plus bas et produit peu transformé donc groupe Nova le plus faible) sera proposée, après interrogation du jeu de données nettoyés et imputés à partir de la base de données d'*Open Food Facts*.

**Exemple de recherche**
![P3_application](https://user-images.githubusercontent.com/71518818/135097470-28a73d2f-74df-417e-abdb-c549f3d3553f.png)
