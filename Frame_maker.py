from cv2 import cv2
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
#pairnoume to video pou theloume
cap = cv2.VideoCapture(dir_path+'/bouncing ball.mov')

try:#o fakelos pou tha apothikeusoume ta frames
    if not os.path.exists(dir_path+'/images/bouncing-ball-frames'):
        os.makedirs(dir_path+'/images/bouncing-ball-frames')
except OSError:
    print ('Error')

currentFrame = 0
while(True):
    #kanoume capture ta frames
    ret, frame = cap.read()
    print(ret)
    #apothikeuoume tis eikones
    name = dir_path+'/images/bouncing-ball-frames/bouncing-ball' + str(currentFrame) + '.jpg'
    print ('Creating...' + name)
    cv2.imwrite(name, frame)

    #proxwrame sthn epomenh
    currentFrame += 1
    
cap.release()
cv2.destroyAllWindows()