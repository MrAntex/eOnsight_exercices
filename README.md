# Exercices eOnsight
## Julien Chignard - 2022

Vous trouverez ici mon rendu pour les exercices demandés pour la candidature de stage à eOnsight.

J'ai trouvé ces deux exercices très intérréssants, et plus particulièrement celui d'imagerie sattelite. J'aurais voulu y passer plus de temps mais les cours ont occupé une bonne partie de ma journée. Je pense m'y repencher plus tard quoi qu'il arrive.

### Exercice Data Engineering :
Pour cet exercice j'ai utilisé Beautiful Soup 4 pour récupérer la liste des ponts situés à Gênes. Le script envoie ensuite ces données sur une base de données postgresql hébergée sur Heroku.

J'ai volontairement laissé les identifiants de la base de données dans le code afin que vous puissiez l'utiliser correctement. Bien sur, ce ne serait pas le cas en production.

#### Utilisation :
(Il vous faudra les librairies `requests, BeautifulSoup, psycopg2, schedule, et time` d'installées sur votre machine)

- `python scrapPonts.py`

J'ai aussi réalisé une version se mettant à jour périodiquement, profitant de l'hébergement sur Heroku. C'est le script `scrapPonts_scheduled.py`.

### Exercice Traitement d'image sattelite :
Pour cet exercice j'ai utilisé les images sattelite issues de Sentinel 2 fournies avec le projet, j'ai aussi tenté d'automatiser la récupération des images mais cela n'a pas fonctionné.

#### 1. Image couleur :
Le premier script sert à créer une image couleur à partir des images par bandes du sattelite.

Le script fonctionne de la manière suivante : il commence par récupérer les images sattelites correspondant aux différentes bandes de langueur d'onde, une image pour le bleu, une pour le rouge, une pour le vert et une infrarouge qui servira pour la luminosité.

Après avoir récupéré les images, elles sont normalisées sur \[0,255\]. Est ensuite appliquée la correction de luminosité en se basant sur l'image infrarouge.
Enfin, les images sont fusionnées sur 3 canaux pour créer une image RGB.

L'image est ensuite rognée pour ne sélectionner que la partie qui nous interresse, c'est à dire la partie où le pont se trouve.

J'ai choisi de rogner l'image après la fusion des canaux, car même si cela prend théoriquement plus de temps, cela permet de pouvoir garder une image large si besoin (Trouvable [ici](https://github.com/MrAntex/eOnsight_exercices/blob/master/imagerie_sattelite/data/sattelite_full.png)).

##### Utilisation :
(Il vous faudra les librairies `skimage, numpy, matplotlib, PIL et osgeo` d'installées sur votre machine)

- `python sattelite.py`

#### 2. Isolation des infrastructures :
Le second script permet d'isoler les zones ou se trouvent des infrastructures.
Pour cela on utilise toujours les mêmes images mais on se sert maintenant aussi d'autres bandes dans l'invisible.

Après un travail de recherche, j'ai appris qu'il était possible grâce à la combinaisons de plusieurs images de déduire à quelle "classe"  appartient un pixel, une classe étant par exemple de l'eau, de la végétation, de la route, etc.
([Source](https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-2-msi/level-2a/algorithm))

Il suffit ensuite de prendnre chaque pixel de l'image et de vérifier si il appartient à telle ou telle classe.

En jouant avec les coefficients de chaque bande, on arrive à une résultat satisfaisant (L'image entière est trouvable [ici](https://github.com/MrAntex/eOnsight_exercices/blob/master/imagerie_sattelite/data/infrasctructures_full.png)).

Il serait possible d'uutiliser cette méthode pour isoler aussi le relief ou encore la végétation, mais j'ai manqué de temps pour aller jusqu'ici.

##### Utilisation :
(Il vous faudra les librairies `skimage, numpy, matplotlib, PIL et osgeo` d'installées sur votre machine)

- `python infrastructures.py`

############################################################################

Les parties suivantes sont des ébauches de ce que j'ai tenté mais qui n'a pas abouti.

#### 3. Détection du pont :
J'ai tenté de détecter automatiquement le pont l'image zoomée, pour faire cela j'ai pensé pouvoir utiliser une détection de contours avec une fenêtre de convolution et/ou une transformée de Fourier, les ponts étants représentés prinncipalement par deux lignes parralèles assez facilement discernables.

Les résulats ne sont pas concluants, les lignes ne sont pas assez précises, et il y a un peu de bruit sur l'image.

Le script est néanmoins disponible si besoin : `bridgeDetect.py`.


#### 4. Téléchargement et rognage automatique des images :
Ayant découvert au cours de mes recherches l'[API Scihub](https://scihub.copernicus.eu/), j'ai tenté de télécharger automatiquement les images de la zone choisie. Cela aurait permis, en pouvant choisir précisemment les coordonnées GPS des points définissant la zone souhaitée, de ne pas avoir à rogner les images par la suite. En plus de pouvoir sélectionner la zone voulue beaucoup plus facilement, simplement avec des coordonnées GPS et une taille de zone.

J'ai donc réalisé une petit script me permettant de calculer les coordonnées GPS des deux points définissant une zone à partir de son point central et de sa longueur et hauteur.

Pour le lancer : `python coordonnes_box.py`

Ce script fonctionnant, je souhaitais le rediiriger vers le script `Sentinel_download.py`, qui permet de télécharger des images issues des sattelites Sentinel des zones souhaitées ([Source](https://github.com/olivierhagolle/Sentinel-download)).

Le problème est que ce script renvoyait des images bien trop grandes par rapport à mes besoins, de plusieurs centaines (milliers ?) de km de longueur et largeur (Par exemple `data/TooLarge.png`, ou on voit bien Gênes mais pas assez précisement).

Je n'ai donc pas pu utiliser ce script.

################################################################################

Merci d'avoir lu ces explications, n'hésitez pas à me contacter si besoin !
