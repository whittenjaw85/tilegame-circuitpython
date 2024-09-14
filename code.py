import board
import digitalio
import displayio
import time
import random
import neopixel

from adafruit_display_text import label
import adafruit_imageload
import terminalio
from adafruit_display_shapes.rect import Rect

import keypad


#setup display
display = board.DISPLAY
group = displayio.Group(scale=1)


#create image mixer
sprite_sheet, palette = adafruit_imageload.load("numbers.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)

image_mover = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                width = 5,
                height = 4,
                tile_width = 32, 
                tile_height = 32)


#randomize image panels
# mixlist = list(range(20))
# for i in range(20):
#     r = random.randint(0, len(mixlist)-1)
#     #print(r)
#     image_mover[i] = mixlist[r]
#     #print(mixlist)
#     mixlist.pop(r)

mixlist = list(range(20))
for i in range(20):
    image_mover[i] = i
    

#highlight the moving position 
rectangle_m = Rect(0, 0, 32, 32, fill = 0x000000)
rectpos = int(0)


#groupstack so the game makes sense
imagegroup = displayio.Group(scale = 1)
imagegroup.append(image_mover)

highlightgroup = displayio.Group(scale = 1)
highlightgroup.append(rectangle_m)

group.append(imagegroup)
group.append(highlightgroup)

display.root_group = group

group.x = 0
group.y = 0

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

#setup keypad events
k = keypad.ShiftRegisterKeys(
    clock=board.BUTTON_CLOCK,
    data=board.BUTTON_OUT,
    latch=board.BUTTON_LATCH,
    key_count=8,
    value_when_pressed=True,
)

def swap_right():
    global rectpos
    global image_mover
    oldpos = rectpos
    oldval = image_mover[oldpos]
    
    rectpos = (rectpos+1)%20
    
    image_mover[oldpos] = image_mover[rectpos]
    image_mover[rectpos] = oldval
    
    calc_position_highlight(rectpos)

def swap_left():
    global rectpos
    oldpos = rectpos
    oldval = image_mover[oldpos]
    rectpos = (rectpos-1)
    if rectpos < 0:
        rectpos = rectpos+20
        
    image_mover[oldpos] = image_mover[rectpos]
    image_mover[rectpos] = oldval
    calc_position_highlight(rectpos)
    
def swap_down():
    global rectpos
    oldpos = rectpos
    oldval = image_mover[oldpos]
    rectpos = (rectpos+5)%20
    
    image_mover[oldpos] = image_mover[rectpos]
    image_mover[rectpos] = oldval
    calc_position_highlight(rectpos)
    

def swap_up():
    global rectpos
    oldpos = rectpos
    oldval = image_mover[oldpos]
    rectpos = (rectpos-5)
    if rectpos < 0:
        rectpos = rectpos+20
        
    image_mover[oldpos] = image_mover[rectpos]
    image_mover[rectpos] = oldval
    calc_position_highlight(rectpos)

    
def calc_position_highlight(rectpos):
    global highlightgroup
    highlightgroup.x = (rectpos%5)*32
    highlightgroup.y = int(rectpos/5)*32
    
def show_level_up():
    pm.show_level_up()
    
    

#setup neopixel strand for timer
GREEN = (0, 255, 0)
YELLOW = (255, 100, 0)
ORANGE = (200, 150, 0)
PINK = (100, 0, 100)
RED = (255, 0, 0)
LEVELUP = 1
PLAY = 0
class PixelManager(object):
    def __init__(self):
        self.level = 0
        
    def show_level_up(self):
        self.s
        
    def show_level(self, level):
        if level == 0:
            self.pixels[0] = RED
        if level == 1:
            self.pixels[0] = RED
            self.pixels[1] = PINK
        if level == 2:
            self.pixels[0] = RED
            self.pixels[1] = PINK
            self.pixels[2] = ORANGE
        if level == 3:
            self.pixels[0] = RED
            self.pixels[1] = PINK
            self.pixels[2] = ORANGE
            self.pixels[3] = YELLOW
        if level == 4:
            self.pixels[0] = RED
            self.pixels[1] = PINK
            self.pixels[2] = ORANGE
            self.pixels[3] = YELLOW
            self.pixels[4] = GREEN
            
        self.pixels.show()
        
        

pm = PixelManager()

def check_win():
    global image_mover
    global rectpos
    vals = list()
    for i in range(20):
        vals.append(image_mover[i])
        
    print(vals)
    for i in range(20):
        if rectpos == i:
            continue
        if image_mover[i] != i:
            print("%d not equal to %d" % (image_mover[i], i))
            return
    
    
    show_level_up()
    
timepiece = time.time()
        
while True:
    event = k.events.get()
    if event:
        if event.pressed == True:
            if event.key_number == 4:
                swap_left()
            if event.key_number == 5:
                swap_up()
            if event.key_number == 6:
                swap_down()
            if event.key_number == 7:
                swap_right()
          
    if time.time() - timepiece > 1:
        check_win()
        timepiece = time.time()
                
    
