import Spin as s
import GPIOcontrol as gp
import threading
import Cameracontrol as cc
import picturemanipulation as pm
import os as oss
import serial
import time

t =int(raw_input('time'))
x = int(raw_input('x'))
r = int(raw_input('r'))
a = 1
gp.gpiosetup(27,26,18)
while a == 1:
    s.serwrite('/1V10000N2Z1000000R\r\n')
    threading.Thread(target=time.sleep(5)).start()
    s.serwrite('/1x1R\r\n')
    time.sleep(0.5)
    s.serwrite('/1D{}R\r\n'.format(x))
    time.sleep(5)
    gp.shine(r,t)
    a = int(raw_input('continue? 1/0'))
    s.stop()

def valving(x,r,t):
    s.serwrite('/1V10000N2Z1000000R\r\n')
    threading.Thread(target=time.sleep(5)).start()
    s.serwrite('/1x1R\r\n')
    time.sleep(0.5)
    s.serwrite('/1D{}R\r\n'.format(x))
    time.sleep(5)
    ste = 5000/6
    steps = int(ste)
    step = str(steps)
    gp.shine(r,t)
    i = 1
    while i < 6:
        serialCode = '/1D{}R\r\n'.format(step)
        s.serwrite(serialCode)
        threading.Thread(target=time.sleep(2)).start()
        gp.shine(r,t)
        i=i+1
    s.stop()
