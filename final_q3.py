# coding=utf-8
#!/usr/bin/python
'''
Created on 2017��9��16��
 
@author: zhangjian
'''
import cv2
import imutils
import numpy as np 
from matplotlib import pyplot as plt
import time 
import math
def get_mode(arr):  
    mode = [];  
    arr_appear = dict((a, arr.count(a)) for a in arr);  
    if max(arr_appear.values()) == 1:  
        mode.append(sum(arr)/len(arr));    
    else:  
        for k, v in arr_appear.items():    
            if v == max(arr_appear.values()):  
                mode.append(k);  
    return mode  
def translate(image, x, y):
    M = np.float32([[1, 0, x], [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return shifted
def pingjie(img1,img2,x_max,y_max): 
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]
    out = np.zeros((rows1+2*abs(x_max),cols1+2*abs(y_max),3), dtype='uint8')
    out[abs(x_max)+x_max:abs(x_max)+rows2+x_max,abs(y_max)+y_max:abs(y_max)+cols2+y_max] = np.dstack([img2])
    out[abs(x_max):rows1+abs(x_max),abs(y_max):cols1+abs(y_max)] = np.dstack([img1])
    return out
def drawMatches(img1, kp1, img2, kp2, matches):
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1] 
    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8') 
    out[:rows1,:cols1] = np.dstack([img1]) 
    out[:rows2,cols1:] = np.dstack([img2])
    a=[]
    b=[]
    c=[]
    d=[]
    for mat in matches: 
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx 
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt
        a.append([x1,y1])
        b.append([x2,y2])
        c.append(x1-x2)
        d.append(y1-y2)
        cv2.circle(out, (int(x1),int(y1)), 4, (0, 0, 255), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (0, 0, 255), 1)

        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (0, 0, 255), 1)
    return out,a,b,c,d  
camera=cv2.VideoCapture("input.avi")
grabbed, pin = camera.read()
while camera.isOpened(): 
    grabbed, frame = camera.read() 
    img1=pin
    img2=frame
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)  
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img1_gray = cv2.GaussianBlur(img1_gray, (21, 21), 0) 
    img2_gray = cv2.GaussianBlur(img2_gray, (21, 21), 0) 
    sift=cv2.ORB()
    kp1, des1 = sift.detectAndCompute(img1,None)  
    kp2, des2 = sift.detectAndCompute(img2,None) 
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)  
    matches = bf.knnMatch(des1, trainDescriptors = des2, k = 2)  
    good = [m for (m,n) in matches if m.distance < 0.6*n.distance] 
    img3,a,b,c,d = drawMatches(img1,kp1,img2,kp2,good) 
    x_max=get_mode(c)[0]
    y_max=get_mode(d)[0]     
    pin = translate(img2, x_max, y_max)
    cv2.imshow("finally",pin)
    cv2.waitKey(20)  
	
camera.release()
cv2.destroyAllWindows()