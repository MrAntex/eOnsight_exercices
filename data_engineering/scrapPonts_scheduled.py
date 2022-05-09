import requests
from bs4 import BeautifulSoup
import psycopg2
import schedule
import time

# Script de scrapping automatisé des noms et coordonnées des ponts d'Italie situés à Gênes, se mettant à jour tous les jours.
# Récupération depuis la page Wikipédia (https://fr.wikipedia.org/wiki/Liste_de_ponts_d%27Italie) à l'aide de BeautifulSoup.
# Insertion dans une base de données PostgreSQL hébergée sur Heroku.
# L'insertion est effectuée en vérifiant qu'il n'y a pas de doublon.

# [Julien Chignard - Mai 2022]


# Création du dictionnaire des ponts en global
global allPonts
allPonts = {}

# Fonction qui sera exécutée par le scheduler
def updatePonts():
    global allPonts # On rend allPonts accessible à la fonction
    
    URL = "https://fr.wikipedia.org/wiki/Liste_de_ponts_d%27Italie" # URL de la page de la liste des ponts
    r = requests.get(URL) # On récupère la page
    
    soup = BeautifulSoup(r.content, 'html5lib') # On parse le contenu de la page

    # Dictionnaire des ponts situés à Gênes
    updatedAllPonts = {
    pont.td.find_next_siblings()[1].text:# On récupère le nom du pont
    pont.td.find_next_siblings()[7].text.replace(u'\xa0', u' ')[5:] # On récupère les coordonnées en formatant le texte pour le rendre lisible et en enlevant le "Gênes" au début

    for catPonts in soup.find_all('table', class_='wikitable') # On récupère les tableaux de la page
    for pont in catPonts.find_all('tr') # On récupère les lignes de chaque tableau
        if not pont.find("th") and "Gênes" in pont.td.find_next_siblings()[7].text # On vérifie que la ligne n'est pas un titre et que le pont est situé à Gênes
    }

    if allPonts != updatedAllPonts: # Si la liste des ponts a changé
        print("Liste de ponts modifiée...") # On affiche un message
        allPonts = updatedAllPonts # On met à jour la liste des ponts

        # On ouvre une connexion à la base de données
        conn = psycopg2.connect(
        host="ec2-176-34-211-0.eu-west-1.compute.amazonaws.com",
        database="dtil67b4purji",
        user="idkgjqwojqkmhw",
        password="f266a4fa205c4a165a2d8196dc87218be253f73d7b4c16d3b0b97af910422814",
        port="5432")

        cur = conn.cursor() # On crée un curseur

        values = "" # Initialisation de la variable contenant les informations à insérer dans la base de données
        for key, value in allPonts.items(): # key = nom du pont, value = coordonnées
            values += "(\'" + key + "\', \'" + value + "\'),\n" # Rajout de chaque valeur dans la requête
        values = values[:-2] # Suppression de la dernière virgule et de la nouvelle ligne

        print("Mise à jour sur la base de données...") # On affiche un message

        # Insertion des valeurs dans la base de données en vérifiant qu'il n'y a pas de doublon
        cur.execute('INSERT INTO ponts_italie (nom, coordonnees) VALUES ' + values+ 'ON CONFLICT (nom) DO NOTHING;') 

        # Insertion des valeurs dans la base de données en mettant à jour les coordonnées si besoin (je n'ai pas jugé cela utile car les ponts ne risquent pas de changer de coordonnées)
        # cur.execute("INSERT INTO ponts_italie (nom, adresse) VALUES " + values+ " ON CONFLICT (nom) DO UPDATE SET coordonnees = excluded.coordonnees;") 

        conn.commit() # Validation des changements

        # Fermeture de la connexion
        cur.close()
        conn.close() 
        
        print(values)

        print("Mise à jour terminée.") # On affiche un message
        
    return

# On lance la fonction updatePonts() tous les jours à 00:00 pour rester à jour automatiquement sans surcharger le site
schedule.every().day.at("00:00").do(updatePonts,'Mise à jour...')

# On lance la fonction updatePonts() au démarrage du programme
updatePonts()

# Lancement de la boucle
while True:
    # On vérifie toutes les minutes si la fonction doit être lancée
    schedule.run_pending()
    time.sleep(60) 





