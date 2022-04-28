#!/usr/bin/python

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd4in2b_V2
import time
from PIL import Image,ImageDraw,ImageFont

def clearScreen():
    try:
        epd = epd4in2b_V2.EPD()
        print("clearing")
        epd.init()
        epd.Clear()
        
        print("sleep")
        epd.sleep()
            
    except IOError as e:
        print(e)
        
    except KeyboardInterrupt:
        print("ctrl + c:")
        epd4in2b_V2.epdconfig.module_exit()
        exit()
    finally:
        print("end")
        time.sleep(2.0)

def main():
    clearScreen()
    
if __name__ == '__main__':
    main()

