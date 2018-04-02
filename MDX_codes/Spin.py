import serial
import time
import threading

ser = serial.Serial(
port='/dev/ttyUSB0',
baudrate=9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS
)


#threading.Thread(target=time.sleep(x)).start()
def serwrite(something):
    a = (something).encode()
    ser.write(a)
def initialize():
    serwrite('/1TR\r\n')
    time.sleep(.1)
    serwrite('/1N2w250x10y10000L2000R\r\n')
    time.sleep(.1)

def autoGoto(x,n):
    '''
    go to position x as locations in 4000;
    n is the number of channels;
    '''
    serwrite('/1V10000N2Z1000000R\r\n')
    threading.Thread(target=time.sleep(2)).start()
    serwrite('/1x1R\r\n')
    threading.Thread(target=time.sleep(2)).start()
    fl='/1D{position}R\r\n'.format(position=x)
    step = int(4000/n)
    individualPositions = [x+i*step for i in range (n)]
    serwrite(fl)
    threading.Thread(target=time.sleep(2)).start()
    if n > 1:
        for i in range (n-1):
            serialCode = '/1D{0}R\r\n'.format(step)
            serwrite(serialCode)
            threading.Thread(target=time.sleep(2)).start()
    else:
        return 'please use goto function next time for one channel'

def spin(rpm):
    serwrite('/1TR\r\n')
    time.sleep(.1)
    serwrite('/1N2w250x10y10000L2000R\r\n')
    time.sleep(.1)
    rpm = int(rpm)
    serialspeed = int(rpm*2184.53333333333)
    serialCode = '/1V{0}P0R\r\n'.format(serialspeed)
    serwrite(serialCode)


def oscillation(angle1,angle2,frequency):
    '''
    Oscillation between two angle1 and angle2 at certain frequency for certain time;
    Angles are in degree, frequency in Hz, time in second;
    '''
    angle1=int(angle1)
    angle2=int(angle2)
    a1=angle1*100/9
    a1=int(a1)
    a2=angle2*100/9
    a2=int(a2)
    serialAngle1 = str(a1)
    serialAngle2 = str(a2)
    frequency = int(frequency)
    v=frequency*(angle2-angle1)/3*2184.533
    v=int(v)
    serialVelocity = str(v)
    serwrite('/1gL50000V{0}A{1}A{2}G0R\r\n'.format(serialVelocity,serialAngle1,
                                                    serialAngle2))
    time.sleep(.1)

def stop():
    serwrite('/1TR\r\n')
    time.sleep(.1)
    serwrite('/1N2w250x10y10000L2000R\r\n')
    time.sleep(.3)
    
def terminalize():
    serwrite('/1TR\r\n')
    time.sleep(.1)
    serwrite('/1N2w250x10y10000L2000R\r\n')
    time.sleep(.3)
    print("Killing motor")

def close():
    ser.close()
