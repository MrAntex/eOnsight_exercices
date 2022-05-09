import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage.io import imread, imshow
from skimage.color import rgb2hsv, rgb2gray, rgb2yuv
from skimage import color, exposure, transform
from skimage.exposure import equalize_hist

# Script de détection de pont dans une image
# Passage de fenêtre de convolution + Transformée de Fourrier
# Malheureusement non fonctionnel

# [Julien Chignard - Mai 2022]


# Lecture de l'image
img = imread('data/infrastructures_pont.png')

# Conversion en NB
img_dark = rgb2gray(img)

# Kernel 3x3
kernel3 = np.array([[-1, -1, -1],
[-1,  8, -1],
[-1, -1, -1]])

# Kernel 5x5
kernel5 = np.array([[-1, -1, -1, -1, -1],
[-1,  1,  2,  1, -1],
[-1,  2,  4,  2, -1],
[-1,  1,  2,  1, -1],
[-1, -1, -1, -1, -1]])

# Filtre de convolution
convolution = ndimage.convolve(img_dark, kernel5)

plt.imshow(convolution, cmap='gray');

# Transformée de Fourrier pour isoler les lignes du pont
four_conv = np.fft.fftshift(np.fft.fft2(convolution))

plt.figure(num=None, figsize=(8, 6), dpi=80)

# Affichage de la magnitude
plt.imshow(np.log(abs(four_conv)), cmap='gray');

plt.show()

