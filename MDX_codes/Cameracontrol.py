#!/usr/bin/python
from __future__ import absolute_import, print_function, division
from pymba import *
import time
import numpy as np
import cv2
import os

class cameramanipulation:
    def __init__(self,exp):
        with Vimba() as vimba:
            pass

            

    def cameratakepicture(self,exp,x,flag,locations):
        '''
        x is countnumber of image
        flag is background identifer
        locations is saving location
        '''
        with Vimba() as vimba:
            # get system object
            self.system = vimba.getSystem()
            # list available cameras (after enabling discovery for GigE cameras)
            if self.system.GeVTLIsPresent:
                self.system.runFeatureCommand("GeVDiscoveryAllOnce")
                time.sleep(0.2)

            self.cameraIds = vimba.getCameraIds()
            for cameraId in self.cameraIds:
                print('Camera ID:', cameraId)

            # get and open a camera
            self.camera0 = vimba.getCamera(self.cameraIds[0])
            self.camera0.openCamera()

            # list camera features
            self.cameraFeatureNames = self.camera0.getFeatureNames()
            #Camera feature setting
            self.camera0.PixelFormat="Mono8"
            self.camera0.ExposureTimeAbs= 500000
            self.camera0.AcquisitionMode = 'SingleFrame'
##            print(self.camera0.AcquisitionMode)
##            print('x')
            self.frame0= self.camera0.getFrame()  # creates a frame  # creates a second frame
            self.frame0.announceFrame()
##            print('y')
        # capture a camera image
            self.camera0.startCapture()
            self.frame0.queueFrameCapture()
            self.camera0.runFeatureCommand('AcquisitionStart')
            self.camera0.runFeatureCommand('AcquisitionStop')
            self.frame0.waitFrameCapture()
        # get image data...
            imgData = self.frame0.getBufferByteData()
        # ...or use NumPy for fast image display (for use with OpenCV, etc)
            moreUsefulImgData = np.ndarray(buffer=self.frame0.getBufferByteData(),
                                       dtype=np.uint8,
                                       shape=(self.frame0.height,
                                              self.frame0.width,
                                              1))
            if flag == 1:
                cv2.imwrite(os.path.join(locations,'%d.png'%(x)),moreUsefulImgData)
            else:
                cv2.imwrite(os.path.join(locations,'%dBackground.png'%(x)),moreUsefulImgData)
        # clean up after capture
            self.camera0.endCapture()
            self.camera0.revokeAllFrames()
        # close camera
            self.camera0.closeCamera()
            print('done')

if __name__ == '__main__':
    test_cameras()
