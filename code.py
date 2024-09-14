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


'''
    Creates the image data for each image
'''
def create_data(image):
    global image_mover
    global group
    
    sprite_sheet = None
    palette = None
    image_mover = None
    sprite_sheet, palette = adafruit_imageload.load(image, bitmap=displayio.Bitmap, palette=displayio.Palette)

    image_mover = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                    width = 5,
                    height = 4,
                    tile_width = 32, 
                    tile_height = 32)
                    
    mixlist = list(range(20))
    for i in range(20):
        image_mover[i] = i
        
    
    
    #groupstack so the game makes sense
    imagegroup = displayio.Group(scale = 1)
    imagegroup.append(image_mover)

    group.append(imagegroup)
    mixup_image(gamelevel)

def draw_highlight():
    global rectpos
    global highlightgroup
    
    #highlight the moving position 
    rectangle_m = Rect(0, 0, 32, 32, fill = 0x000000)
    highlightgroup = displayio.Group(scale = 1)
    highlightgroup.append(rectangle_m)
    group.append(highlightgroup)
    
    highlightgroup.x = (rectpos%5)*32
    highlightgroup.y = int(rectpos/5)*32
    
    

    
def create_game_win():
    pm.show_win()

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

def swap_left():
    global rectpos
    oldpos = rectpos
    oldval = image_mover[oldpos]
    rectpos = (rectpos-1)
    if rectpos < 0:
        rectpos = rectpos+20
        
    image_mover[oldpos] = image_mover[rectpos]
    image_mover[rectpos] = oldval
    
def swap_down():
    global rectpos
    oldpos = rectpos
    oldval = image_mover[oldpos]
    rectpos = (rectpos+5)%20
    
    image_mover[oldpos] = image_mover[rectpos]
    image_mover[rectpos] = oldval
    

def swap_up():
    global rectpos
    oldpos = rectpos
    oldval = image_mover[oldpos]
    rectpos = (rectpos-5)
    if rectpos < 0:
        rectpos = rectpos+20
        
    image_mover[oldpos] = image_mover[rectpos]
    image_mover[rectpos] = oldval


def update_highlight():
    global highlightgroup
    global rectpos
    highlightgroup.x = (rectpos%5)*32
    highlightgroup.y = int(rectpos/5)*32

def mixup_image(level):
    global rectpos 
    rectpos = random.randint(0, 20)
    
    mixlist = (0,1,2,3)
    for i in range((level+2)*5):
        r = random.choice(mixlist)
        if r == 0:
            swap_right()
        elif r == 1:
            swap_left()
        elif r == 2:
            swap_up()
        elif r == 3:
            swap_down()
        
        time.sleep(0.05)
        
def show_level_up():
    global gamestate
    global group
    global imagelist
    global gamelevel
    
    hlg = group.pop()
    pm.show_level_up()
    group.pop()
    
    gamelevel += 1
    
    if gamelevel == 5:
        create_game_win()
    else:    
        create_data(imagelist[gamelevel])
    
    gamestate = PLAYING
    group.append(hlg)
    
   


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
        self.pixels = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness=0.02, auto_write=False)
        self.show_level(self.level)
        
    def clear(self):
        for i in range(5):
            self.pixels[i] = (0,0,0)
            
        self.pixels.show()
        
    def show_level_up(self):
        self.level = self.level + 1
        for i in range(5):
            self.show_level(i)
            time.sleep(0.5)
            
        self.show_level(self.level)
        time.sleep(1)
        
    def show_win(self):
        self.pixels.brightness = 0.2
        self.clear()
        while(True):
            for i in range(5):
                self.show_level(i)
                time.sleep(0.1)
        
    def show_level(self, level):
        self.clear()
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



def check_win():
    global image_mover
    global rectpos
    global gamestate
    
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
    
    
    gamestate = LEVELUP
    show_level_up()
    

    
#setup game variables
PLAYING = 0
LEVELUP = 1
gamestate = PLAYING
gamelevel = 0

#setup display
display = board.DISPLAY
group = displayio.Group(scale=1)

#create image mixer
imagelist = ["numbers.bmp", "dogfire.bmp", "camelkiss.bmp", "turtlefris.bmp", "cowview.bmp"]

sprite_sheet = None
image_mover = None
highlightgroup = None
imagegroup = None
rectpos = int(0)

timepiece = time.time()

display.root_group = group

group.x = 0
group.y = 0
create_data(imagelist[0]) 
draw_highlight()

pm = PixelManager()
        
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
                
            update_highlight()
          
    if time.time() - timepiece > 1:
        if gamestate == PLAYING:
            check_win()
            timepiece = time.time()
                
    

