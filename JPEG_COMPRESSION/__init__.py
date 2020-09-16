import math
import os
import time
import imutils
from bitarray import bitarray, bits2bytes
import numpy as np
from MOTION_ESTIMATION.LogarithmicSearch import *
from .EntropyEncoding import Encoder, DC, AC
from .utils import (block_slice, block_combine, 
dct2d,idct2d, quantize,dequantize)

'''
Algorithmos sumpieshs jpeg:                                       
        exoume apo prin metatrepsei thn eikona se gray-scale                         
        epeidh mporei oi diastaseis na mhn einai pollaplasia tou 8
        kanoume padding wste na ginei 8n*8n                            
        diairoume thn eikona se 8*8                                    
        gia kathe block:                               
            DCT                                       
            kanoume Quantization 
        kwdikopoihsh entropias 
'''
#arxizoume th sumpiesh, to withExtract xrhsimeuei sthn askhsh tou meros B
def compress(image,withExtract=False):
    
    data=image.astype(float) #apothikeuoume to pinaka ths eikonas
    
    nrows, ncols = data.shape #pairnoume tis diastaseis wste na exetasoume an einai pollaplies tou 8
    
    #padding gia 8N * 8N
    data = np.pad(
        data,
            (
                (0, (nrows // 8 + 1) * 8 - nrows if nrows % 8 else 0),
                (0, (ncols // 8 + 1) * 8 - ncols if ncols % 8 else 0)
            ),
            mode='constant'
        )
    
    #diairoume thn eikona se tmhmata 8*8 
    data= block_slice(data, 8, 8)
    
    #exoume xwrisei thn eikona se block kai gia kathe block kanoyme ta parakatw
    for i, block in enumerate(data):
        #kanoume DCT
        data[i] = dct2d(block)

        #Quantization me bash ton pinaka JPEG gia grey scale
        data[i] = quantize(data[i])

    #tous kanoume apo float se int 
    data = np.rint(data).astype(int)
    if not withExtract: #gia askhseis 17,18
        #Kwdikopoihsh entropias: arxikopoihsh tha pame se -> endiamesh anaparastash
        encoded = Encoder(data).encode()

        #enonoume thn kwdikopoihsh pou pairnoume ap twn DC,AC mesw huffman 
        order = (encoded[DC], encoded[AC])

        #pairnoume ta bits
        bits = bitarray(''.join(order))

        #gurname ta bits, einai se morfh dictionary giati mporei na mas bohthisei se epomena erwthmata 
        #wste na gyrname parapanw dedomena 
        return {
            'data': bits,
        }
    else: #gia askhsh meros B
        size=[nrows, ncols]
        for i, block in enumerate(data):
            # Inverse Quantization
            data[i] = dequantize(block)

            # inverse DCT
            data[i] = idct2d(data[i])
        
        #epanafora ths eikonas se kanoniko size kathws prohgoumenws eixame dhmiourghsei 8*8 blocks
        #inverse padding
        inv_pad = ((s // 8 + 1) * 8 if s % 8 else s for s in size)
        
        #kanoume combine ta data mas me to inverse padding wste pleon o pinakas mas na exei tis arxikes tou diastasie
        data = block_combine(data, *inv_pad)
        # Clip Padded Image
        data = data[:size[0], :size[1]]
        # Combine layers into signle raw data.
        return data
    