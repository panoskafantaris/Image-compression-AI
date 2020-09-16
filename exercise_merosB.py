import numpy as np
import random as rn
from cv2 import cv2
from JPEG_COMPRESSION import compress
from JPEG_COMPRESSION.utils import block_combine
from JPEG_COMPRESSION.HuffmanTree import *

def main():
    AM=list('15054')
    A_img=np.zeros((104,200)) #eikona A
    B_img=None #eikona B
    results=[] #oi logoi sumpieshs
    for i in range(1,100):
        x=rn.randint(0,4) #epilegoume tuxaia mia thesh
        AM[x]='5' #thn antikathistoume me to 5
        row=[AM[0],AM[1],AM[2],AM[3],AM[4]] #ftiaxnoume th grammh
        
        #ftiaxnoume thn eikona
        j=0
        for r in range(0,104):
            for c in range(0,200):
                A_img[r][c]=int(row[j])
                j=j+1
                if(j==5):
                    j=0
        #sumpiezoume th B sumfwna me to sxhma 7.7
        B_img=compress(A_img,withExtract=True)

        #Huffman gia B
        #metrame poses fores emfanizetai enas arithmos dld ftiaxnoume ena histogram
        hist = np.bincount(B_img.ravel(),minlength=256)
        probabilities = hist/np.sum(hist) #diairontas me to plhthos twn arithmwn briskoume tis pithanothtes		
    
        root_node = tree(probabilities) #ftiaxnoumai to dentro me riza to root node
        
        #anatrexoume to dentro apo to root node
        huffman_traversal(root_node)

        B_bits=np.sum(huffman_traversal.output_bits)
        #Huffman gia A
        A_img=A_img.astype(int)
        hist = np.bincount(A_img.ravel(),minlength=256)
        probabilities = hist/np.sum(hist) 		
        root_node = tree(probabilities) 
        huffman_traversal(root_node)
        A_bits=np.sum(huffman_traversal.output_bits)

        compression_ratio = (A_bits/B_bits)
        print(A_bits)
        print(B_bits)
        print('Compression_ratio einai ',compression_ratio)
        results.append(compression_ratio)
    mean_compress_ration=np.sum(results)/100
    print('O mesos logos sumpieshs einai: ',mean_compress_ration)
    #grafoume ta apotelesmata
    with open("Results-mean-compression-ratio.txt", "w") as text_file:
        text_file.write("%s\n" % "O mesos logos sumpieshs einai:")
        text_file.write("%s\n" % mean_compress_ration)
        
if __name__ == '__main__':
    main()
