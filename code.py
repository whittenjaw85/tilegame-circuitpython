import board
import digitalio
import displayio
import time
import random

from adafruit_display_text import label
import adafruit_imageload
import terminalio
from adafruit_display_shapes.rect import Rect

import keypad

display = board.DISPLAY
group = displayio.Group(scale=1)

sprite_sheet, palette = adafruit_imageload.load("/dogfire.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)

image_mover = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                width = 5,
                height = 4,
                tile_width = 32, 
                tile_height = 32)


mixlist = list(range(20))
for i in range(20):
    r = random.randint(0, len(mixlist)-1)
    print(r)
    image_mover[i] = mixlist[r]
    print(mixlist)
    mixlist.pop(r)

rectangle_m = Rect(0, 0, 32, 32, fill = 0x000000)
rectpos = int(0)

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
    
    rectpos = (rectpos+1)%20
    
    image_mover[oldpos] = image_mover[rectpos]
    
    calc_position_highlight(rectpos)

def swap_left():
    global rectpos
    oldpos = rectpos
    rectpos = (rectpos-1)
    if rectpos < 0:
        rectpos = rectpos+20
        
    image_mover[oldpos] = image_mover[rectpos]
    calc_position_highlight(rectpos)
    
def swap_down():
    global rectpos
    oldpos = rectpos
    rectpos = (rectpos+5)%20
    
    image_mover[oldpos] = image_mover[rectpos]
    calc_position_highlight(rectpos)

def swap_up():
    global rectpos
    oldpos = rectpos
    rectpos = (rectpos-5)
    if rectpos < 0:
        rectpos = rectpos+20
        
    image_mover[oldpos] = image_mover[rectpos]
    calc_position_highlight(rectpos)

    
def calc_position_highlight(rectpos):
    global highlightgroup
    highlightgroup.x = (rectpos%5)*32
    highlightgroup.y = int(rectpos/5)*32
    
    
while True:
    event = k.events.get()
    if event:

        if event.pressed == True:
            if event.key_number == 4:
                swap_right()
            if event.key_number == 5:
                swap_down()
            if event.key_number == 6:
                swap_up()
            if event.key_number == 7:
                swap_left()
