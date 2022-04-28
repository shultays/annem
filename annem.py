import RPi.GPIO as GPIO
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd4in2b_V2
import time
from PIL import Image,ImageDraw,ImageFont
from clear import clearScreen

GPIO.setmode(GPIO.BCM)

led1 = 2
led2 = 3

button1 = 4

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.output(led1, 0)
GPIO.output(led2, 0)

files = []
for (dirpath, dirnames, filenames) in os.walk("/home/taytay/annem"):
    filenames.sort()
    for f in filenames:
        if f.endswith(".bmp"):
            z = os.path.join(dirpath, f)
            files.append(Image.open(z))
            

epd = epd4in2b_V2.EPD()
HRYimage = Image.new('1', (epd.width, epd.height), 255)  
im = 0
def display():
    global im
    global files
    global HRYimage
    
    print("next")
        
    epd = epd4in2b_V2.EPD()
    epd.init()
    epd.display(epd.getbuffer(files[im]), epd.getbuffer(HRYimage))
    
    epd.sleep()
    
    print("done")
    im = (im + 1) % len(files)
    time.sleep(2)

t = False
def onButton(pin):
    global t
    if t:
        return
    t = True
    
    display()
    
    t = False
    print("done2")
    
GPIO.setup(button1, GPIO.IN)
GPIO.add_event_detect(button1, GPIO.FALLING, callback=onButton, bouncetime=100)

try:
    while True:
        time.sleep(1.0)
except KeyboardInterrupt:
    clearScreen()
finally:
    clearScreen()