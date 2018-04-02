import GPIOcontrol as gc
import sys
import time

def main():
    gc.gpiosetup(26,27,18)
    gc.lineargo(50,18)

def close():
    gc.led(0,27)

if __name__ == "__main__":
    try:
        main()
        time.sleep(5)
        a = input('close?')
        if a == 'y':
            sys.exit
        else:
            gc.lineargo(a,18)
    except KeyboardInterrupt:
        pass
