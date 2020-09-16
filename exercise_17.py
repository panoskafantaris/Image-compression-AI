import numpy as np
from MOTION_ESTIMATION.LogarithmicSearch import *
from JPEG_COMPRESSION import compress
from JPEG_COMPRESSION.utils import rgbTogray,make_video
from cv2 import cv2
import os

#askhsh 17

#upoerwtima 1 
def Get_Results_ImgDifference(i_frame):
    results=[]
    for i in range(1,100):#se posa frames thelete na epanalhpthei h diadikasia
        path = 'images/bouncing-ball-frames/bouncing-ball'+str(i)+'.jpg'
        p_frame=rgbTogray(path) #metatrepoume se gray-scale
        frame_diff = cv2.absdiff(p_frame,i_frame) #pairnoume th diafora tous
        compressed = compress(frame_diff) #sumpiezoume
        
        #apothikeuoume to apotelesma ths eikonas
        saving_img_path='images/differencial-img/'
        cv2.imwrite(os.path.join(saving_img_path , 'Error-img-'+str(i)+'.jpg'), frame_diff)
        
        #apothikeuoume to mhkos ths entropias ths
        results.append(str(len(compressed['data'])))
        print(str(i)+'%')
    #to grafoume sto arxeio
    with open("Results-Diff.txt", "w") as text_file:
        text_file.write("%s\n" % "Entropy length for image difference(1-100):")
        for i in results:
            text_file.write("%s\n" % i)
        text_file.close()

#upoerwthma 2 ta idia me prin me kapoies diafores 
def Get_Results_MotionEst(i_frame):
    results=[]
    for i in range(1,100):
        path = 'images/bouncing-ball-frames/bouncing-ball'+str(i)+'.jpg'
        p_frame=rgbTogray(path)
        prediction_frame=LogSearch(p_frame,i_frame).ReconstructImage() #problepoume thn eikona
        
        #meta briskoume th diafora tous
        frame_diff = cv2.absdiff(prediction_frame,p_frame)
        compressed = compress(frame_diff) #meta sumpiezoume
        
        #apothikeuoume
        saving_img_path='images/MotionEst-img/'
        cv2.imwrite(os.path.join(saving_img_path , 'Error-img-'+str(i)+'.jpg'), frame_diff)
        results.append(str(len(compressed['data'])))
        print(str(i)+'%')
    #grafoume ta apotelesmata
    with open("Results-MotionEst.txt", "w") as text_file:
        text_file.write("%s\n" % "Entropy length for MotionEstimation(1-100):")
        for i in results:
            text_file.write("%s\n" % i)

def main():
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    i_framePath ='images/bouncing-ball-frames/bouncing-ball0.jpg'
    i_frame=rgbTogray(i_framePath)

    Get_Results_ImgDifference(i_frame)
    print('TELOS UPOERWTHMATOS 1')
    print('ARXIZEI TO DEUTERO')
    Get_Results_MotionEst(i_frame)
    print('TELOS DEUTEROU.. TELOS ASKHSHS')
    print('FTIAXNOUME TA VIDEOS..')
    
    #video gia prwto upoerwthma
    make_video('differencial-img','Image_difference')

    #video gia deutero
    make_video('MotionEst-img','Motion-Estimation')

if __name__ == '__main__':
    main()
