import requests
from bs4 import BeautifulSoup
import psycopg2
import schedule
import time

# Script de scrapping des noms et coordonnées des ponts d'Italie situés à Gênes.
# Récupération depuis la page Wikipédia (https://fr.wikipedia.org/wiki/Liste_de_ponts_d%27Italie) à l'aide de BeautifulSoup.
# Insertion dans une base de données PostgreSQL hébergée sur Heroku.
# Affichage du contenu de cette base de données.

# [Julien Chignard - Mai 2022]


print('Récupération de la page...')
URL = "https://fr.wikipedia.org/wiki/Liste_de_ponts_d%27Italie" # URL de la page de la liste des ponts
r = requests.get(URL) # On récupère la page

soup = BeautifulSoup(r.content, 'html5lib') # On parse le contenu de la page

# Dictionnaire des ponts situés à Gênes
allPonts = {
pont.td.find_next_siblings()[1].text:# On récupère le nom du pont
pont.td.find_next_siblings()[7].text.replace(u'\xa0', u' ')[5:] # On récupère les coordonnées en formatant le texte pour le rendre lisible et en enlevant le "Gênes" au début

for catPonts in soup.find_all('table', class_='wikitable') # On récupère les tableaux de la page
for pont in catPonts.find_all('tr') # On récupère les lignes de chaque tableau
    if not pont.find("th") and "Gênes" in pont.td.find_next_siblings()[7].text # On vérifie que la ligne n'est pas un titre et que le pont est situé à Gênes
}

print('Liste de ponts récupérée.')

print('Connexion à la base de données...')

# On ouvre une connexion à la base de données
conn = psycopg2.connect(
host="ec2-54-76-43-89.eu-west-1.compute.amazonaws.com",
database="d5ians6u408hn2",
user="nooyxjbuglycdg",
password="0ce112f2940a7dddb5f7f2ea59978c349285742c405f108b4f850a11f3fe132f",
port="5432")

cur = conn.cursor() # On crée un curseur

values = "" # Initialisation de la variable contenant les informations à insérer dans la base de données
for key, value in allPonts.items(): # key = nom du pont, value = coordonnées
    values += "(\'" + key + "\', \'" + value + "\'),\n" # Rajout de chaque valeur dans la requête
values = values[:-2] # Suppression de la dernière virgule et de la nouvelle ligne

print("Mise à jour de la base de données...")

# Insertion des valeurs dans la base de données en vérifiant qu'il n'y a pas de doublon
cur.execute('INSERT INTO ponts_italie (nom, coordonnees) VALUES ' + values+ 'ON CONFLICT (nom) DO NOTHING;') 

# Insertion des valeurs dans la base de données en mettant à jour les coordonnées si besoin (je n'ai pas jugé cela utile car les ponts ne risquent pas de changer de coordonnées)
# cur.execute("INSERT INTO ponts_italie (nom, adresse) VALUES " + values+ " ON CONFLICT (nom) DO UPDATE SET coordonnees = excluded.coordonnees;") 

conn.commit() # Validation des changements

print("Mise à jour terminée.")

print("Contenu de la base de données:")

cur.execute('SELECT * FROM ponts_italie;') # On récupère les valeurs de la base de données

for row in cur.fetchall(): # On affiche les valeurs
    print(row)

print("Fin de l'exécution. Fermeture de la connexion.")

# Fermeture de la connexion
cur.close()
conn.close() 

