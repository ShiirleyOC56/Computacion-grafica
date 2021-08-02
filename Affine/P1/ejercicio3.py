import sys
import cv2 
import numpy as np 
from matplotlib import pyplot as plt

def interpolation(img):
    heigth, width, rgb = img.shape
    scaling = np.zeros((heigth*2-1, width*2-1, rgb), np.uint8)

    for row in range(heigth-1):
        for column in range(width-1):
            scaling[row*2][column*2] = img[row][column]
            scaling[row*2][column*2+1] = img[row][column] #(img[row][column] + img[row][column+1])*0.5
            scaling[row*2+1][column*2] = img[row][column] #(img[row][column] + img[row+1][column])*0.5

            if column:
                scaling[row*2+1][column*2-1] = (scaling[row*2+1][column*2] + scaling[row*2+1][column*2-2])*0.5

        scaling[row*2][(width-1)*2] = img[row][width-1]
        scaling[row*2+1][(width-1)*2] = (img[row][width-1]+img[row+1][width-1])*0.5
        scaling[row*2+1][(width-1)*2-1] = (scaling[row*2+1][(width-1)*2] + scaling[row*2+1][(width-1)*2-2])*0.5
        
    for column in range(width-1):    
        scaling[(heigth-1)*2][column*2] = img[heigth-1][column]    
        scaling[(heigth-1)*2][column*2+1] = (img[heigth-1][column+1]+img[heigth-1][column])*0.5

    scaling[(heigth-1)*2][(width-1)*2] = img[heigth-1][width-1]
    return scaling
    #cv2.imwrite('interpolacion.jpg', scaling)

def runI(file1):
    img = cv2.imread(file1)
    out=interpolation(img)
    if out is not None:
        #final_frame = cv2.vconcat((img, out))
        cv2.imshow('Interpolacion',out)
        cv2.imwrite('./Out/out_interpolacion.png',out)
        cv2.waitKey(0)

runI('./Input/input1.png')
