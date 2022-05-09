from skimage import io, data
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from osgeo import gdal

# Script d'isolation des infrastructures depuis une image Sentinel par classe pixels
# Rognage selon une zone de recherche
# Sauvegarde de l'image

# [Julien Chignard - Mai 2022]


coeffLum = 2.2 # Coefficient pour la luminosité

# Coefficients pour l'isolation des différentes classes de l'image (végétation, roches, eau, etc.)
coeffNDVI = 1.8
coeffSV = 1.8
coeffWat = 1.7
coeffRocks = 2

boundingBox = [[670, 170], [1065, 550]] # Zone à isoler du reste de l'image

savePath = 'data/infrasctructures_pont.png'


# Lecture des fichiers de données
imgB = io.imread('data/2022-04-16-00:00_2022-04-16-23:59_Sentinel-2_L2A_B02_(Raw).tiff') # Bande bleue
imgG = io.imread('data/2022-04-16-00:00_2022-04-16-23:59_Sentinel-2_L2A_B03_(Raw).tiff') # Bande verte
imgR = io.imread('data/2022-04-16-00:00_2022-04-16-23:59_Sentinel-2_L2A_B04_(Raw).tiff') # Bande rouge
imgN = io.imread('data/2022-04-16-00:00_2022-04-16-23:59_Sentinel-2_L2A_B08_(Raw).tiff') # Bande Infrarouge
imgSWIR = io.imread('data/2022-04-16-00:00_2022-04-16-23:59_Sentinel-2_L2A_B11_(Raw).tiff') # Bande SWIR-1

width, height = imgB.shape[0:2]

# Isolation des pixels de couleur
arrayB = imgB[:,:,0]
arrayG = imgG[:,:,0]
arrayR = imgR[:,:,0]
arrayN = imgN[:,:,0]
arraySWIR = imgSWIR[:,:,0]


# Création de la carte de la luminosité à partir de l'infrarouge
arrayLum = (arrayN / arrayN.max()) + coeffLum

# Normalisation des valeurs en uint8
arrayB = arrayB * 255.0/arrayB.max()
arrayG = arrayG * 255.0/arrayG.max()
arrayR = arrayR * 255.0/arrayR.max()
arraySWIR = arraySWIR * 255.0/arraySWIR.max()
arrayN = arrayN * 255.0/arrayN.max()

# Création des masques pour détecter les différentes classes de l'image
imgNDVI = (arrayN - arrayG) / (arrayN + arrayG) # Végétation
imgSV = arrayN / arrayG # Végétation "brillante"
imgWat = arrayB / arraySWIR # Eau
imgRocks = arrayN / arraySWIR # Pierres / Désert

# Ajustement de la luminosité de l'image 
arrayB = (arrayB * arrayLum).clip(0,255)
arrayG = (arrayG * arrayLum).clip(0,255)
arrayR = (arrayR * arrayLum).clip(0,255)

# Création de l'image en RGB
rgb = np.dstack((arrayR, arrayG, arrayB))

# Sélection des pixels  correspondants à des infrastructures
for i in range(width):
    for j in range(height):
        if imgNDVI[i,j] > coeffNDVI:
            rgb[i,j] = [0,0,0]
        elif imgSV[i,j] > coeffSV:
            rgb[i,j] = [0,0,0]
        elif imgWat[i,j] > coeffWat:
            rgb[i,j] = [0,0,0]
        elif imgRocks[i,j] > coeffRocks:
            rgb[i,j] = [0,0,0]


# Conversion en uint8
rgb = rgb.astype(np.uint8)

# Rognage pour ne conserver que la zone du pont
rgb = rgb[boundingBox[0][1]:boundingBox[1][1], boundingBox[0][0]:boundingBox[1][0]]

#print(rgb.shape)

# Sauvegarde et affichage de l'image
im = Image.fromarray(rgb, 'RGB')
im.save(savePath)
im.show()


