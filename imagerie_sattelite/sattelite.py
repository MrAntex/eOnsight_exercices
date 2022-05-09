from skimage import io, data
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from osgeo import gdal

# Script de création d'image à partir de données Sentinel
# Rognage selon une zone de recherche
# Sauvegarde de l'image

# [Julien Chignard - Mai 2022]


coeffLum = 2.2 # Coefficient pour la luminosité
boundingBox = [[670, 170], [1065, 550]] # Zone à isoler du reste de l'image

# Localisation du fichier de sortie
savePath = 'data/sattelite_pont.png'


# Lecture des fichiers de données
imgB = io.imread('data/2022-04-16-00:00_2022-04-16-23:59_Sentinel-2_L2A_B02_(Raw).tiff') # Bande bleue
imgG = io.imread('data/2022-04-16-00:00_2022-04-16-23:59_Sentinel-2_L2A_B03_(Raw).tiff') # Bande verte
imgR = io.imread('data/2022-04-16-00:00_2022-04-16-23:59_Sentinel-2_L2A_B04_(Raw).tiff') # Bande rouge
imgN = io.imread('data/2022-04-16-00:00_2022-04-16-23:59_Sentinel-2_L2A_B08_(Raw).tiff') # Bande Infrarouge

# Isolation des pixels de couleur
arrayB = imgB[:,:,0]
arrayG = imgG[:,:,0]
arrayR = imgR[:,:,0]
arrayN = imgN[:,:,0]

# Création de la carte de la luminosité à partir de l'infrarouge
arrayN = (arrayN / arrayN.max()) + coeffLum

# Normalisation des valeurs en uint8
arrayB = arrayB * 255.0/arrayB.max()
arrayG = arrayG * 255.0/arrayG.max()
arrayR = arrayR * 255.0/arrayR.max()

# Ajustement de la luminosité de l'image 
arrayB = (arrayB * arrayN).clip(0,255)
arrayG = (arrayG * arrayN).clip(0,255)
arrayR = (arrayR * arrayN).clip(0,255)

# Création de l'image en RGB
rgb = np.dstack((arrayR, arrayG, arrayB))

# Conversion en uint8
rgb = rgb.astype(np.uint8)

# Rognage pour ne conserver que la zone du pont
rgb = rgb[boundingBox[0][1]:boundingBox[1][1], boundingBox[0][0]:boundingBox[1][0]]

#print(rgb.shape)

# Sauvegarde et affichage de l'image
im = Image.fromarray(rgb, 'RGB')
im.save(savePath)
im.show()


