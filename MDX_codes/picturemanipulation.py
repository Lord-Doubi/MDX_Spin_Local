import cv2
import numpy as np
import os


def readimg(x,locations,flag):
    if flag == 1:
        return cv2.imread(os.path.join(locations,'%d.png'%(x)))
    else:
        return cv2.imread(os.path.join(locations,'%dBackground.png'%(x)))

def subtract(img,imgbck,x,loactions):
    imgs = imgbck-img
##    cv2.imwrite('home/pi/MDX_codes/testSubtracted.png'.format(loactions,x),imgs)
    cv2.imwrite(os.path.join(locations,'%dSubtract.png'%(x)),imgs)

def filter(x,locations):
    img = cv2.imread(os.path.join(locations,'%dSubtract.png'%(x)))
##    imgs = cv2.imread('testSubtracted.png',0)
    imgs = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(imgs,(17,17),0)
    ret,th = cv2.threshhold(blur,100,255,cv2.THRESH_TOZERO)
    cv2.imwrite(os.path.join(locations,'%dFiltered.png'%(x)),th)
    return th

def findcircle(img,x,locations):
    im2, contours, hierarchy = cv2.findContours(img,1,2)
    n = len(contours)
    i = 0
    r = 0
    approx = [None]*n
    perimeter = [None]*n
    epsilon = [None]*n
    thco = cv2.cvtColor(th,cv2.COLOR_Gray2BGR)
    while i < n :
        M = cv2.moments(contours[i])
        area = cv2.contourArea(contours[i])
        if area >1000:
            if area<100000:
                perimeter[i]= cv2.arcLength(contour[i],True)
                epsilon[i]=0.01*perimeter[i]
                approx[i]=cv2.approxPolyDP(contours[i],epsilon[i],True)
                cv2.drawContours(thco,[approx[i]],-1,(0,0,255),4)
                r = r+1
        i=i+1

    cv2.imwrite(os.path.join(locations,'%dFindcircle.png'%(x)),thco)
    return thco
    
