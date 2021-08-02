import cv2
import os
import numpy as np
from matplotlib import pyplot as plt 
import math

def TranslateW(img, x, y):
	h, w = img.shape[:2]
	A = np.identity(2)  
	B = [[x],[y]]
	M = np.concatenate((A, B), axis=1)
	img_out = cv2.warpAffine(img, M, (w, h))
	return img_out

def ScaleW(img, x, y):
	h, w = img.shape[:2]
	A = np.float32([[x,0],[0,y]])
	B = [[0],[0]]
	M = np.concatenate((A, B), axis=1)
	img_out = cv2.warpAffine(img, M, (w, h))
	return img_out

def RotationW(img, angle):
	h, w = img.shape[:2]
	img_c = (w / 2, h / 2)
	M = cv2.getRotationMatrix2D(img_c, angle, 1)
	rad = math.radians(angle)
	sin = math.sin(rad)
	cos = math.cos(rad)
	b_w = int((h * abs(sin)) + (w * abs(cos)))
	b_h = int((h * abs(cos)) + (w * abs(sin)))
	M[0, 2] += ((b_w / 2) - img_c[0])
	M[1, 2] += ((b_h / 2) - img_c[1])
	img_out = cv2.warpAffine(img, M, (b_w, b_h))
	return img_out

def shearW(img, x, y):
	h, w = img.shape[:2]
	ix = math.tan(x * math.pi / 180)
	iy = math.tan(y * math.pi / 180)
	M = np.float32([[1,ix,0],[iy,1,0]])
	img_out = cv2.warpAffine(img, M, (w+256, h+256))
	#final_frame = cv2.vconcat((img, img_out))
	#cv2.imshow('Antes - Despues',final_frame)
	#cv2.waitKey()
	return img_out

def runT(file1,x,y):
	img = cv2.imread(file1)
	out=TranslateW(img,x,y)
	if out is not None:
		final_frame = cv2.hconcat((img, out))
		cv2.imshow('Antes - Despues',final_frame)
		cv2.waitKey(0)
		cv2.imwrite('./Out/out_translate.png',out)
		cv2.destroyAllWindows()

def runS(file1,x,y):
	img = cv2.imread(file1)
	out=ScaleW(img,x,y)
	if out is not None:
		final_frame = cv2.hconcat((img, out))
		cv2.imshow('Antes - Despues',final_frame)
		cv2.waitKey(0)
		cv2.imwrite('./Out/out_scale.png',out)
		cv2.destroyAllWindows()

def runR(file1,angle):
	img = cv2.imread(file1)
	out=RotationW(img,angle)
	if out is not None:
		final_frame = cv2.hconcat((img, img_out))
		cv2.imshow('Antes - Despues',final_frame)
		cv2.waitKey(0)
		namefile='./Out/out_rotation_'+str(angle)+'.png'
		cv2.imwrite(namefile,out)
		cv2.destroyAllWindows()
		

def runShe(file1,x,y):
	img = cv2.imread(file1)
	out= shearW(img, x, y)
	if out is not None:
		cv2.imshow("Shear",img_out)
		cv2.waitKey(0)
		cv2.imwrite('./Out/out_shear.png',out)
		cv2.destroyAllWindows()

#runS('./Input/input1.png',0.4,0.9) 

"""for i in range(9):
	angle=45*i
	runR('./Input/input1.png',angle)"""
#runShe('./Input/input1.png',20,15)