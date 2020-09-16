from MOTION_ESTIMATION.LogarithmicSearch import *
from JPEG_COMPRESSION.utils import rgbTogray,make_video
from cv2 import cv2
import numpy as np
import os

#askhsh 18

#kai ta duo upoerwthmata
def remove_object(i_frame):
    results=[]
    for i in range(1,100):
        #pairnoume to frame
        path = 'images/bouncing-ball-frames/bouncing-ball'+str(i)+'.jpg'
        #metatroph se grayscale
        p_frame=rgbTogray(path)
        #afairoume to antikeimeno 
        prediction_frame=LogSearch(p_frame,i_frame,n=16,step=8).ReconstructImage(remove=True)
        #an thelete na allaxete to megethos tou block prepei na grapsete LogSearch(p_frame,i_frame,n=enas arithmos).Reconst...
        print(str(i),'%')
        #apothikeuoume to frame
        saving_img_path='images/Img-with-no-obj/'
        cv2.imwrite(os.path.join(saving_img_path , 'Error-img-'+str(i)+'.jpg'), prediction_frame)

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    i_framePath ='images/bouncing-ball-frames/bouncing-ball0.jpg'
    i_frame=rgbTogray(i_framePath)

    remove_object(i_frame) #afairoume to antikeimeno
    make_video('Img-with-no-obj','video-with-no-obj') #ftiaxnoume to video
        
if __name__ == '__main__':
    main()