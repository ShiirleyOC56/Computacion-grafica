import sys
import cv2
from ejercicio1 import TranslateW, ScaleW, RotationW, shearW
import numpy as np
import math
from matplotlib import pyplot as plt

def WarpAffine(img, M, widthI, heightI):
	h, w, c = img.shape
	img_out = np.zeros((heightI, widthI, c), np.uint8)
	A = np.array([[M[1][1],M[1][0]],[M[0][1],M[0][0]]])
	B = np.array([[M[1][2]],[M[0][2]]])
	for i in range(h):
		for j in range(w):
			X = np.array([[i],[j]])
			M1 = np.dot(A, X) + B
			M1 = M1.astype(int)
			if (M1[0,0] > 0 and M1[0,0] < heightI and M1[1,0] > 0 and M1[1,0] < widthI):
				for k in range(c):
					img_out[M1[0, 0], M1[1, 0]] =  img[i][j]
	return img_out

def Translate(img, x, y):
    h, w = img.shape[:2]
    A = np.identity(2)
    B = [[x],[y]]
    M = np.concatenate((A, B), axis=1)
    img_out = WarpAffine(img, M, w, h)
    return img_out

def Scale(img, x, y):
	h, w = img.shape[:2]
	A = np.float32([[x,0],[0,y]])
	B = [[0],[0]]
	M = np.concatenate((A, B), axis=1)
	img_out = WarpAffine(img, M, w, h)
	return img_out

def Rotation(img, angle):
    h, w = img.shape[:2]
    cX,cY  = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    #rad = math.radians(angle)
    sin = np.abs(M[0,0])
    cos = np.abs(M[0,1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    """b_w = int((h * abs(sin)) + (w * abs(cos)))
    b_h = int((h * abs(cos)) + (w * abs(sin)))

    mid_h = int((h+1)/2)
    mid_w = int((w+1)/2)

    A = np.float32([[cos,sin],[-sin,cos]])
    B = [[((1-cos)*img_c[0])-(sin*img_c[1])],[(sin*img_c[1])+((1-sin)*img_c[0])]]
    #B = [[((1-cos)*mid_w)-(sin*mid_h)],[(sin*mid_w)+(1-sin)*mid_h]]
    M = np.concatenate((A, B), axis=1)

    M[0, 2] += ((b_w / 2) - img_c[0])
    M[1, 2] += ((b_h / 2) - img_c[1])"""
    img_out = WarpAffine(img, M, nW, nH)
    return img_out

def Shear(img, x, y):
	h, w = img.shape[:2]
	ix = math.tan(x * math.pi / 180)
	iy = math.tan(y * math.pi / 180)
	A = np.float32([[1,ix,0],[iy,1,0]])
	B = [[0],[0]]
	M = np.concatenate((A, B), axis=1)
	img_out = WarpAffine(img, M, w+256, h+256)
	return img_out

def runTr(file1,x,y):
    img = cv2.imread(file1)
    out=Translate(img,x,y)
    out_w = TranslateW(img, x, y)
    if out is not None:
        final_frame = cv2.hconcat((out_w, out))
        cv2.imshow('Con OpenCV - Sin OpenCV',final_frame)
        cv2.imwrite('./Out/out_mi_translate.png',out)
        cv2.waitKey(0)

def runSc(file1,x,y):
    img = cv2.imread(file1)
    out=Scale(img, x, y)
    out_w = ScaleW(img, x, y)
    if out is not None:
        final_frame = cv2.hconcat((out_w, out))
        cv2.imshow('Con OpenCV - Sin OpenCV',final_frame)
        cv2.imwrite('./Out/out_mi_scale.png',out)
        cv2.waitKey(0)

def runRo(file1,angle):
    img = cv2.imread(file1)
    out=Rotation(img, angle)
    out_w = RotationW(img, angle)
    if out is not None:
        #final_frame = cv2.hconcat((out_w, out))
        cv2.imshow('Con OpenCV - Sin OpenCV',out)
        filename = './Out/out_mi_rotation_'+str(angle)+'.png'
        cv2.imwrite(filename,out)
        cv2.waitKey(0)

def runShe(file1,x,y):
    img = cv2.imread(file1)
    out=Shear(img,x,y)
    out_w = shearW(img, x, y)
    if out is not None:
        final_frame = cv2.hconcat((out_w, out))
        cv2.imshow('Con OpenCV - Sin OpenCV',final_frame)
        cv2.imwrite('./Out/out_mi_shear.png',out)
        cv2.waitKey(0)

#runTr('./Input/input1.png', 70, 70)
#runSc('./Input/input1.png', 0.4, 0.9)
for i in range(9):
	angle=45*i
	runRo('./Input/input1.png',angle)
#runShe('./Input/input1.png', 20,15)