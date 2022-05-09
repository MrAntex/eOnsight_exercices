# 44°25''1'N, 8°52''46'E
import math

# Script de calcul des coordonnées GPS d'une zone à partir de son point central et de sa hauteur et longueur.
# Les distances sont en km.
# Renvoie les coordonnées GPS sous forme de points à écriture décimale et de tuples (latitude, longitude)

# [Julien Chignard - Mai 2022]

r_earth = 6378 # Rayon de la terre en km

# Coordonnées du centre de la zone en question
centerLong = [44, 25, 34, 'N']
centerLat = [8, 53, 19, 'E']

# Taille en km de la zone à isoler
width = 2
length = 2

# Conversion de km en degrés
KmToLatitudeDeg = 1/110.574
KmToLongitudeDeg = 1/(111.32 * math.cos(centerLat[0] * math.pi / 180))

# Conversion de coordonnées en nombre décimal
def getLatitude(latitude):
    return (latitude[0] + latitude[1]/60 + latitude[2]/3600) * (latitude[3] == 'N' and -1 or 1)

# Conversion de coordonnées en nombre décimal
def getLongitude(longitude):
    return (longitude[0] + longitude[1]/60 + longitude[2]/3600) * (longitude[3] == 'E' and -1 or 1)

# Conversion de nombre décimal en degrés
def floatToDeg(f):
    d = int(f)
    m = int((f - d) * 60)
    s = int(((f - d) * 60 - m) * 60)
    return (d, m, s)

# Coordonnées du point en haut à gauche de la zone à isoler
new_latitude1  = getLatitude(centerLat)  + ((length/2) / r_earth) * (180 / math.pi);
new_longitude1 = getLongitude(centerLong) + ((width/2) / r_earth) * (180 / math.pi) / math.cos(getLatitude(centerLat) * math.pi/180);
 # Coordonnées du point en bas à droite de la zone à isoler
new_latitude2  = getLatitude(centerLat)  - ((length/2) / r_earth) * (180 / math.pi);
new_longitude2 = getLongitude(centerLong) - ((width/2) / r_earth) * (180 / math.pi) / math.cos(getLatitude(centerLat) * math.pi/180);


# Affichage
print(new_longitude1, new_latitude1)
print(new_longitude2, new_latitude2)
print(floatToDeg(new_latitude1), floatToDeg(new_longitude1))
print(floatToDeg(new_latitude2), floatToDeg(new_longitude2))
