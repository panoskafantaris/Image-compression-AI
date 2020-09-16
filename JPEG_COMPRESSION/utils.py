import collections
import math
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import numpy as np
from scipy.fftpack import dct, idct
from skimage.color import rgb2gray
import skimage   
from cv2 import cv2
import glob

#metatroph apo rgb se gray scale
def rgbTogray(path):
    img = mpimg.imread(path).astype(float)     
    gray = rgb2gray(img) 
    return gray 

#ftiaxnoume to video ap ta frames pou exoume brei
#folder apo kei pou pairnoume ta frames
#name to onoma pou dinoume sto video 
def make_video(folder,name):
    img_array = []
    for filename in glob.glob('images/'+folder+'/*.jpg'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
 
    out = cv2.VideoWriter('videos/'+name+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

#diairoume ton pinaka se 8*8 
def block_slice(arr, nrows, ncols):
    h, _ = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1, 2)
               .reshape(-1, nrows, ncols))

#sunduazei mia list apo blocks (m * n) se pinaka(m,n)
def block_combine(arr, nrows, ncols):
    if arr.size != nrows * ncols:
        raise ValueError(f'The size of arr ({arr.size}) should be equal to '
                         f'nrows * ncols ({nrows} * {ncols})')

    _, block_nrows, block_ncols = arr.shape

    return (arr.reshape(nrows // block_nrows, -1, block_nrows, block_ncols)
            .swapaxes(1, 2)
            .reshape(nrows, ncols))

#DCT
def dct2d(arr):
    return dct(dct(arr, norm='ortho', axis=0), norm='ortho', axis=1)

#inverse DCT
def idct2d(arr):
    return idct(idct(arr, norm='ortho', axis=0), norm='ortho', axis=1)

#Quantization
def quantize(block):
    quantization_table = QUANTIZATION_TABLE
    return block / (quantization_table)

#deQuantization
def dequantize(block):
    quantization_table = QUANTIZATION_TABLE
    return block * (quantization_table)

#o jpeg quantization pinakas
QUANTIZATION_TABLE = np.array((
    (16, 11, 10, 16, 24, 40, 51, 61),
    (12, 12, 14, 19, 26, 58, 60, 55),
    (14, 13, 16, 24, 40, 57, 69, 56),
    (14, 17, 22, 29, 51, 87, 80, 62),
    (18, 22, 37, 56, 68, 109, 103, 77),
    (24, 36, 55, 64, 81, 104, 113, 92),
    (49, 64, 78, 87, 103, 121, 120, 101),
    (72, 92, 95, 98, 112, 100, 103, 99)
))
