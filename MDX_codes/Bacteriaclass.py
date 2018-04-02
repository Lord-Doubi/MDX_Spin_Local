############################################################
## 01/22/2018 by Lord.Doubi. Revised from OpenCV tutorial ##
############################################################
import cv2
import os
import numpy as np
import Cameracontrol as cc

class Bug():
    def __init__(self,name):
        self.name = name
        self.background = name+"_Background"
        os.chdir('./data')
        files=os.listdir('.')
        identifier = 0
        if self.name in files:
            print "Already in database"
        else:
            os.system('mkdir {}'.format(self.name))
        os.chdir('..')
# creat bug name and folder and go back to main folder
    def getimage(self,i):
        """
        i = 0 get bacground image
        i = 1 get fluorescence image
        """
        os.chdir('./data/{}'.format(self.name))
        if i == 0:
            cc.Cameratakepicture(self.background)
        if i == 1:
            cc.Cameratakepicture(self.name)
        else:
            return 'Error'
        os.chdir('..')
        os.chdir('..')

    def realimage(self):
        os.chdir('./data/{}'.format(self.name))
        self.profile = cv2.imread(self.name,0)
        self.background = cv2.imread(self.background,0)
        self.realimage = self.profile-self.background
        cv2.imwrite("/{}/{}.png".format(self.name,self.realimage),self.realimage)
# store substracted image in /data/bug

    def findcountours(self):
        self.blur = cv2.GaussianBlur(self.realimage,(17,17),0)
        self.ret,self.th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        self.im2, self.contours,self.hierarchy = cv2.findContours(self.th, 1, 2)
        n=len(self.contours)
        i = 0
        r = 0
        approx=[None]*n
        perimeter=[None]*n
        epsilon=[None]*n
        self.thco = cv2.cvtColor(self.th, cv2.COLOR_GRAY2BGR)
        print 'Total Contours found{}'.format(n)
        while i<n:
          M = cv2.moments(self.contours[i])
          area = cv2.contourArea(self.contours[i])
          if area > 100:
            if area < 10000:
              perimeter[i] = cv2.arcLength(self.contours[i],True)
              epsilon[i] = 0.01*cv2.arcLength(self.contours[i],True)
              approx[i] = cv2.approxPolyDP(self.contours[i],epsilon[i],True)
              cv2.drawContours(self.thco,[approx[i]],-1,(0,0,255),4)
              r = r+1
              print 'Intensity for Filtered Contours {} is {}\n'.format(r,M)
          i=i+1
        print 'Filtered Contours found{}'.format(r)
        cv2.imwrite("{}{}.png".format(self.name,'_processed'),self.thco)
        os.chdir('..')
        os.chdir('..')
        #go back to main folder
