import sys
import os
from PyQt4 import QtCore, QtGui, uic
import time
import picturemanipulation as pm
import GPIOcontrol as Gc
import Motorsteps as Ms


qtDevFile = "/home/pi/MDX_codes/GUI/Developer.ui"
Ui_DevWindow, QtDevClass = uic.loadUiType(qtDevFile)

class Developermode(QtGui.QMainWindow, Ui_DevWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_DevWindow.__init__(self)
        self.setupUi(self)
        self.datawd = None
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.led = 0
        self.laser = 0
        self.ledpin = 27
        self.laserpin = 26
        self.linearpin = 18
    @QtCore.pyqtSlot()
    def on_step0_dev_clicked(self):
        n = self.n_dev.text()
        x = self.x_dev.text()
        pid = self.pid_dev.text()
        temp_var = self.dateEdit.date()
        date = temp_var.toPyDate()
        exp = self.expo_dev.text()
        wd = '/images/data/{}/{}/AST'.format(date,pid)
        self.datawd = os.getcwd()+wd
##        a = int(self.led_dev.text())
##        b = int(self.laser_dev.text())
##        c = int(self.linear_dev.text())
        Ms.step0(n,x,pid,0,date,27,26,18)

    @QtCore.pyqtSlot()
    def on_step1_dev_clicked(self):
        rpm = self.rpm_dev.text()
        t = self.t_dev.text()
        Ms.spin(rpm,t)
        Ms.s.stop()

    @QtCore.pyqtSlot()
    def on_step2_dev_clicked(self):
        a0 = self.a0_dev.text()
        a1 = self.a1_dev.text()
        f = self.f_dev.text()
        t = self.t_dev.text()
        Ms.os(a0,a1,f,t)

    @QtCore.pyqtSlot()
    def on_step3_dev_clicked(self):
        rpm = self.rpm_dev.text()
        t = self.t_dev.text()
        Ms.spin(rpm,t)
        Ms.s.stop()

    @QtCore.pyqtSlot()
    def on_step4_dev_clicked(self):
        a0 = self.a0_dev.text()
        a1 = self.a1_dev.text()
        f = self.f_dev.text()
        t = self.t_dev.text()
        Ms.os(a0,a1,f,t)

    @QtCore.pyqtSlot()
    def on_step5_dev_clicked(self):
        a0 = self.a0_dev.text()
        a1 = self.a1_dev.text()
        f = self.f_dev.text()
        t = self.t_dev.text()
        Ms.os(a0,a1,f,t)

    @QtCore.pyqtSlot()
    def on_step6_dev_clicked(self):
        a0 = self.a0_dev.text()
        a1 = self.a1_dev.text()
        f = self.f_dev.text()
        t = self.t_dev.text()
        Ms.os(a0,a1,f,t)
        Ms.spin(500,20)
        Ms.s.stop()

    @QtCore.pyqtSlot()
    def on_step7_dev_clicked(self):
        
        n = self.n_dev.text()
        n = int(n)
        x = self.x_dev.text()
        x = int(x)
        pid = self.pid_dev.text()
        temp_var = self.dateEdit.date()
        date = temp_var.toPyDate()
        exp = self.expo_dev.text()
        exp = int(exp)
        wd = '/images/data/{}/{}/AST'.format(date,pid)
        tempwd = 'home/pi/MDX_codes/images/data/Current_result'
        self.datawd = os.getcwd()+wd
##        a = self.led_dev.text()
        Ms.camera(x,n,1,self.datawd,exp,27)
##        for i in range(1,n+1):
##            Ms.Imageprocess(i,tempwd,self.datawd)
            
    @QtCore.pyqtSlot()
    def on_step8_dev_clicked(self):
        pid = self.pid_dev.text()
        temp_var = self.dateEdit.date()
        date = temp_var.toPyDate()
        wd = '/images/data/{}/{}/AST'.format(date,pid)
        self.datawd = os.getcwd()+wd
        a=str(self.imgprocess_dev.currentText())
        
        if a == 'Subtract':
            img = pm.readimg(1,self.datawd,1)
            imgbck = pm.readimg(1,'/home/pi/MDX_codes/images/data/Current_result',0)
            pm.subtract(img,imgbck,1,self.datawd)
            print ('ok')
        elif a == 'Filter':
            img = pm.readimg(1,self.datawd,1)
            imgbck = pm.readimg(1,'/home/pi/MDX_codes/images/data/Current_result',0)
            pm.subtract(img,imgbck,1,self.datawd)
            pm.filter(1,self.datawd)
            print ('not finished')
        elif a == 'All':
            img = pm.readimg(1,self.datawd,1)
            imgbck = pm.readimg(1,'/home/pi/MDX_codes/images/data/Current_result',0)
            pm.subtract(img,imgbck,1,self.datawd)
            dude = pm.filter(1,self.datawd)
            pm.findcircle(dude,1,self.datawd)
            print ('sorry')



    @QtCore.pyqtSlot()
    def on_spspin_dev_clicked(self):
        rpm = self.rpm_dev.text()
        t = self.t_dev.text()
        Ms.spin(rpm,t)
        Ms.s.stop()


    @QtCore.pyqtSlot()
    def on_spled_dev_clicked(self):
##        a = self.led_dev.text()
        if (self.led%2) == 0:
            Gc.led(1,27)
            self.led = self.led+1
        else:
            Gc.led(0,27)
            self.led = self.led+1
            

    @QtCore.pyqtSlot()
    def on_spvalving_dev_clicked(self):
##        b = self.laser_dev.text()
##        c = self.linear_dev.text()
        t = self.t_dev.text()
        x = self.x_dev.text()
        n = self.n_dev.text()
        r = self.r_dev.text()
        Ms.valving(x,n,r,t,26,18)

    @QtCore.pyqtSlot()
    def on_sppositioning_dev_clicked(self):
        Gc.gpiosetup(27,26,18)
        r = self.r_dev.text()
##        c = self.linear_dev.text()
        Gc.lineargo(r,18)

    @QtCore.pyqtSlot()
    def on_motorstop_dev_clicked(self):
        Ms.s.stop()

    @QtCore.pyqtSlot()
    def on_exit_clicked(self):
        self.close()
