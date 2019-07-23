#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author: Furo Yang


import cv2 as cv
import numpy as np

def skyRegion(picname):
	iLow = np.array([100,43,46])
	iHigh = np.array([124,255,255])
	img = cv.imread(picname)
	imgOriginal = cv.imread(picname)
	img = cv.cvtColor(img,cv.COLOR_BGR2HSV)

	#hsv split
	h,s,v = cv.split(img)
	v = cv.equalizeHist(v)
	hsv = cv.merge((h,s,v))

	imgThresholded = cv.inRange(hsv,iLow,iHigh)
	imgThresholded = cv.medianBlur(imgThresholded,9)

	#open
	kernel = np.ones((5,5),np.uint8)
	imgThresholded = cv.morphologyEx(imgThresholded,cv.MORPH_OPEN,kernel,iterations = 10)
	imgThresholded = cv.medianBlur(imgThresholded,9)

	pic_name = picname.split('/')[-1].split('.')[0]
	tmp = 'D:/temp/py_img/' + pic_name + '-mask.jpg'
	print(tmp)
	cv.imwrite(tmp,imgThresholded)
	return tmp

def seamClone(skyname,picname,maskname):
	# read images
	src = cv.imread(skyname)
	dst = cv.imread(picname)

	src_mask = cv.imread(maskname,0)
	src_mask0 = cv.imread(maskname,)
	contours,hierarchy = cv.findContours(src_mask,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
	cnt = contours[0]

	x,y,w,h = cv.boundingRect(cnt)
	#print (x,y,w,h) 
	if w==0 or h == 0:
		return dst
	dst_x = len(dst[0])
	dst_y = len(dst[1])
	src_x = len(src[0])
	src_y = len(src[1]) 
	scale_x = w*1.0/src_x 
	src = cv.resize(src,(dst_x,dst_y),interpolation = cv.INTER_CUBIC)

	cv.imwrite('src_sky.jpg',src)
	center = (int((x+w)/2),int((y+h)/2))
	print (center)

	output = cv.seamlessClone(src,dst,src_mask0,center,cv.NORMAL_CLONE)

	return output

def test():
	src = cv.imread("C:/Users/hss/Desktop/20190114132436.png")
	cv.namedWindow("input image",cv.WINDOW_AUTOSIZE)
	cv.imshow('input image',src)
	cv.waitKey(0);
	cv.destroyAllWindows()

if __name__ == "__main__":
	#test()
	#picname = 'C:/Users/hss/Desktop/20190114132436.png'
	picname = 'C:/Users/hss/Desktop/20190723162440.jpg'
	skyname = 'C:/Users/hss/Desktop/20190723162643.jpg'
	maskname = skyRegion(picname)
	print(maskname)
	output = seamClone(skyname,picname,maskname)
	cv.imwrite('output.jpg',output)