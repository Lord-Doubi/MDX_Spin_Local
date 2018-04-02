import RPi.GPIO as GPIO
import time
import threading
import sys

def gpiosetup(laserpin,ledpin,linearactuatorpin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(linearactuatorpin,GPIO.OUT)
    GPIO.setup(laserpin,GPIO.OUT)
    GPIO.setup(ledpin,GPIO.OUT) #Laser pin initialize


def laser(x,laserpin):
    if x == 1:
        GPIO.output(laserpin,GPIO.HIGH)
    if x == 0:
        GPIO.output(laserpin,GPIO.LOW)

def lineargo(x,linearactuatorpin):
    c = float(x)
    a = c*2
    pwm=GPIO.PWM(linearactuatorpin, 1000)
    pwm.start(0)
    pwm.ChangeDutyCycle(a)
    time.sleep(1)


def led(x,ledpin):
    if x == 1:
        GPIO.output(ledpin, GPIO.HIGH)
    if x == 0:
        GPIO.output(ledpin, GPIO.LOW)

def shine(x,y):
    c = float(x)
    a = c*2
    b = a/10
    pwm=GPIO.PWM(18, 1000)
    pwm.start(0)
    pwm.ChangeDutyCycle(a)
    time.sleep(b)
    GPIO.output(26,GPIO.HIGH)
    time.sleep(y)
    GPIO.output(26,GPIO.LOW)
