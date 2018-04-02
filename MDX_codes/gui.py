#!/usr/bin/python3
import sys
import os
from PyQt4 import QtCore, QtGui, uic
import time
import developer as dm
import Motorsteps as ms

qtCreatorFile = "/home/pi/MDX_codes/GUI/MDX.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Result(QtGui.QDialog):
    def __init__(self,n):
        QtGui.QDialog.__init__(self)
        d = QtGui.QDialog()
        b1 = QtGui.QPushButton("Close",d)
        b1.clicked.connect(d.close)
        d.setWindowTitle("Result")
        d.setWindowModality(QtCore.Qt.ApplicationModal)
        #temperary results
        layout = QtGui.QGridLayout()
        layout.addWidget(b1,2*n,5)
        for i in range(1,n+1):
            original = QtGui.QLabel(d)
            opixmap = QtGui.QPixmap(
                                   '/home/pi/MDX_codes/images/data/Current_result/{}.png'.format(i))
            opixmap = opixmap.scaled(150,150,QtCore.Qt.KeepAspectRatio)
            
            original.setPixmap(opixmap)
            ol = QtGui.QLabel(d)
            ol.setText('Orignial Image for {}'.format(i))

            subtracted = QtGui.QLabel(d)
            spixmap = QtGui.QPixmap(
                                   '/home/pi/MDX_codes/images/data/Current_result/{}Subtracted.png'.format(i))
            spixmap = spixmap.scaled(150,150,QtCore.Qt.KeepAspectRatio)
            subtracted.setPixmap(spixmap)
            sl = QtGui.QLabel(d)
            sl.setText('Subtracted Image for {}'.format(i))

            filtered = QtGui.QLabel(d)
            fpixmap = QtGui.QPixmap(
                                   '/home/pi/MDX_codes/images/data/Current_result/{}Filtered.png'.format(i))
            fpixmap = fpixmap.scaled(150,150,QtCore.Qt.KeepAspectRatio)
            filtered.setPixmap(fpixmap)
            fl = QtGui.QLabel(d)
            fl.setText('Filtered Image for {}'.format(i))


            circled = QtGui.QLabel(d)
            cpixmap = QtGui.QPixmap(
                                   '/home/pi/MDX_codes/images/data/Current_result/{}Findcircle.png'.format(i))
            cpixmap = cpixmap.scaled(150,150,QtCore.Qt.KeepAspectRatio)
            circled.setPixmap(cpixmap)
            cl = QtGui.QLabel(d)
            cl.setText('Found Spots for {}'.format(i))


            layout.addWidget(original,i,1)
            layout.addWidget(subtracted,i,2)
            layout.addWidget(filtered,i,3)
            layout.addWidget(circled,i,4)
            layout.addWidget(ol,i+1,1)
            layout.addWidget(sl,i+1,2)
            layout.addWidget(fl,i+1,3)
            layout.addWidget(cl,i+1,4)

        d.setLayout(layout)
        d.exec_()

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        

        #define buttons:
        self.Developermode.clicked.connect(self.on_Devbutton_clicked)
        self.developermode=dm.Developermode()
        #Number of channels!!!!!
        self.n=1
        self.Result.clicked.connect(self.on_Resbutton_clicked)
    @QtCore.pyqtSlot()
    def on_Devbutton_clicked(self):
##        self.developermode.show()
        self.developermode.showFullScreen()
    @QtCore.pyqtSlot()
    def on_Resbutton_clicked(self):
        self.result = Result(self.n)
    @QtCore.pyqtSlot()  
    def on_AST_clicked(self):
        pid = self.PatientID.toPlainText()
        temp_var = self.Testdate.date()
        date = temp_var.toPyDate()
        ms.AST(4,pid,date,27,26,18)
    @QtCore.pyqtSlot()
    def on_ID_clicked(self):
        pid = self.PatientID.toPlainText()
        temp_var = self.Testdate.date()
        date = temp_var.toPyDate()
        ms.ID(4,pid,date,27,26,18)
    @QtCore.pyqtSlot()
    def on_Close_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyApp')
    main = MyApp()
##    main.show()
    main.showFullScreen()
    sys.exit(app.exec_())
