import Spin as s
import GPIOcontrol as gp
import threading
import Cameracontrol as cc
import picturemanipulation as pm
import os as oss
import serial
import time

ser = serial.Serial(
port='/dev/ttyUSB0',
baudrate=9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS
)

def valving(x,n,r,t,b,c):
    r = int(r)
    x = int(x)
    b = int(b)
    c = int(c)
    n = int(n)
    t = int(t)
    s.serwrite('/1V10000N2Z1000000R\r\n')
    threading.Thread(target=time.sleep(5)).start()
    s.serwrite('/1x1R\r\n')
    time.sleep(0.5)
    s.serwrite('/1D{}R\r\n'.format(x))
    time.sleep(5)
    n = int (n)
    ste = 5000/n
    steps = int(ste)
    step = str(steps)
    gp.shine(r,t)
    i = 1
    while i < n:
        serialCode = '/1D{}R\r\n'.format(step)
        s.serwrite(serialCode)
        threading.Thread(target=time.sleep(2)).start()
        gp.shine(r,t)
        i=i+1
##    s.spin(500)
##    threading.Thread(target=time.sleep(15)).start()
    s.stop()

def camera(x,n,flag,location,exp,a):
    '''
    x stands for angular position
    n stands for number of channels
    flag is background identifer
    location is the saving location
    exp is exposure
    '''
    exp = int(exp)
    n = int (n)
    x = int(x)
    a = int(a)
    cameras=cc.cameramanipulation(exp)
    s.serwrite('/1V10000N2Z1000000R\r\n')
    threading.Thread(target=time.sleep(2)).start()
    s.serwrite('/1x1R\r\n')
    time.sleep(0.1)
    s.serwrite('/1D{position}R\r\n'.format(position=x))
    threading.Thread(target=time.sleep(2)).start()
    n = int (n)
    ste = 4000/n
    steps= int(ste)
    step = str(steps)
    gp.led(1,a)
    threading.Thread(target=time.sleep(1)).start()
    cameras.cameratakepicture(500000,1,flag,location)
    threading.Thread(target=time.sleep(1)).start()
    gp.led(0,a)
    print ('good')
    if n > 1:
        for i in range(2,n+1):
            serialCode = '/1D{0}R\r\n'.format(step)
            s.serwrite(serialCode)
            threading.Thread(target=time.sleep(2)).start()
            gp.led(1,a)
            threading.Thread(target=time.sleep(1)).start()
            cameras.cameratakepicture(500000,i,flag,location)
            threading.Thread(target=time.sleep(1)).start()
            gp.led(0,a)
            print (i)
    else:
        pass
##def Imageprocess(x,tempwd,datawd):
##    signal = pm.readimg(x,tempwd,1)
##    background = pm.readimg(x,tempwd,0)
##    imgs = pm.subtract(signal,background,x,tempwd)
####    cv2.imwrite('{}{}Subtracted.png'.format(datawd,x),imgs)
##    cv2.imwrite('testSubtracted.png'.format(datawd,x),imgs)


def step0(n,x,pid,f,date,a,b,c):
    f = int(f)
    a = int(a)
    b = int(b)
    c = int(c)
    x = int(x)
    n = int(n)
    gp.gpiosetup(a,b,c)
    s.initialize()
    
    wd = '/images/data/{}/{}/AST'.format(date,pid)
    datawd = oss.getcwd()+wd
    if not oss.path.exists(datawd):
        oss.makedirs(datawd)
    tempwd = oss.getcwd()+'/images/data/Current_result'
    camera(x,n,f,tempwd,500000,a)

def spin(rpm,t):
    s.spin(rpm)
    t = int(t)
    threading.Thread(target=time.sleep(t)).start()

def os(a1,a2,f,t):
    s.oscillation(a1,a2,f)
    t=int(t)
    threading.Thread(target=time.sleep(t)).start()
    s.stop()


def AST(n,pid,date,a,b,c):
    '''
    x stands for channels
    '''
    #step 0: setup and take background image
    a = int(a)
    b = int(b)
    c = int(c)
    gp.gpiosetup(a,b,c)
    s.initialize()
    wd = '/images/data/{}/{}/AST'.format(date,pid)
    datawd = oss.getcwd()+wd
    if not oss.path.exists(datawd):
        oss.makedirs(datawd)
    tempwd = oss.getcwd()+'/images/data/Current_result'
    camera(200,n,0,tempwd,60000,a)
    #step 1 : metering
    s.spin(500)
    threading.Thread(target=time.sleep(10)).start()
    #step 2: incubation
    s.oscillation(0,180,2)
    threading.Thread(target=time.sleep(5400)).start()
    s.stop()
    #laservalve opening:
    valving(100,4,20,3,b,c)
    #step 3: Lysis
    s.spin(200)
    threading.Thread(target=time.sleep(300)).start()
    #laservalve opening:
    valving(100,4,30,3,b,c)
    #step 4: Neutralization
    s.oscillation(0,180,2)
    threading.Thread(target=time.sleep(20)).start()
    #laservalve opening:
    valving(100,4,40,3,b,c)
    #step 5: Hybridization
    s.oscillation(0,180,2)
    threading.Thread(target=time.sleep(20)).start()
    s.stop()
    #valving
    valving(100,4,50,3,b,c)
    #step 6: washing
    s.oscillation(0,180,1)
    threading.Thread(target=time.sleep(20)).start()
    s.spin(500)
    threading.Thread(target=time.sleep(10)).start()
    #step 7: detection
    camera(200,n,1,tempwd,60000,a)
    for i in range(1,n+1):
        Imageprocess(i,tempwd,datawd)
