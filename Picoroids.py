#    
#         ,@""""""²╗
#         ║` ╓φ▄   █`
#        ]╜  █░▒  ╟▌,,,    ,,,,    ,,.   ,.....,     ,,,    ,,,  .....,   ,,,,,,
#       ,▒  ▓▒▒  j█▒ .█`,*`   ▓▒,'   `@ ,▒      ▒∩ ¿`   ╠, ▒` ╠▌░      ╟@╜     ╟▌
#       ║` ]▌]░  █▌  ╟▒╨` ,@▀▀▀░` ▄w  ╟╖▒  █▀░ ]▓░┘ ,@  └▌╓░ ┌█▒  ▓▀░ ┌█▒  ╫▀▀▀▀
#      ]░   `   ╟█` ╓▌▒  @▀   ▒  █▀▒  █▓` ▐▌▒  █▒` ╥█▒r ╓█▒  ▓▒  ╟▌▒  █░╢  ╟░
#     .▒  ╓@KKK▀▒▒  █▒  ╟▀   ▒  ▓▒]░ ▐▌▒    ,φ▓▀╜ ┌▓ ▒  ▓▌  á▌░ ┌▓▒` ▐▌ ║  ╠▌
#     ╟   █`    ▒  ╟▌░ ╓▌   ]░ ]▌╓╜ ,█▒  ╓  ╟▌ ▒  ▓▒▒  ╟▓░  ▓Ñ  ▓▒▒ ┌█  ╙░  ▌
#    ╓░  ▓╝    ║░ ╓▌▒  █░   ║  └▓` ,▓▒░ ┌▓  ╟▌└▒  ╟▌  ▄█▒  ▓▌` ╟▌▒  █▒  ]▒  ▓
#    ▒  ]▌    j▒  █╫░     ▓▒╙H   ,@▀┌▒  █▒  ╟▌ ▒    ▄▓░║` ▐▓▒  ``  ╠█▒     ╟▌
#   ╠   █`    ╙▀%▀╜ ╙%KKKΦ▀  └╩%╝▀  ╙▀╩▀╜╙%╩▀╜  ╙%╩▀└  ▀Ñ╩▀▀╩╩╩╩╩╩▀▀╚Ñ╩╩╩%▀▀
#  ╓M  ╟▒
#  ╢,,g▌
#   `` 
# 
# Picoroids
# 
# by Andy Crook Feb 2021
#
# andy.crook@gmail.com
#
# https://github.com/andycrook
# 
# Picoroids is an asteroids clone written in python for the raspberry pi pico
# 
# The main target of the game is a small ssd1306 oled display, 128 x 64 pixels
# but refactoring it for other screns should be possible
#
# The game has an autoplay mode to show the features of the game without
# wiring up buttons, but 5 buttons are recommended to actually play the game
# 
# press fire to start
#
# main screen shows lives left, hyperspace available and the score
#   

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import machine
import framebuf
import random
import time
import math

WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height

i2c = I2C(0)                                            # Init I2C using I2C0 defaults, SCL=Pin(GP9), SDA=Pin(GP8), freq=400000

# report i2c address for information 
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config


oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display


# setup buttons on these physical pins


button_fire = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_left = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_right = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_thrust = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_hyperspace = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN)





# False by default. Setting this to true is for display mode without buttons

AUTOPLAY_MODE = False







# splash screen. Byte array for picoroids. Generated by my image to bytes python script
#
# https://github.com/andycrook/image-to-bytearray-for-OLED-python-programs
#


splash = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x02\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x02\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x08\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x04\x3c\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x34\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x20\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x08\x60\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x08\x60\x30\x00\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x0b\xe8\
\x00\x00\x48\x30\xc0\x06\x00\x00\x00\x00\x02\x08\x60\x00\x20\x0c\
\x00\x10\x40\x70\xc0\x06\x00\x42\x00\x20\x01\x00\x60\x01\x00\x08\
\x00\x10\xc0\x60\x80\x06\x00\x00\x00\x30\x01\x00\x40\x01\x80\x08\
\x00\x00\x80\x61\x80\x04\x00\x20\x00\x20\x01\x10\xc0\x01\x80\x18\
\x00\x20\x80\xe1\x80\x7c\x00\x24\x38\x60\x00\x80\xc1\xc3\x87\xf0\
\x00\x21\x80\xc1\x20\xc0\x08\x24\x20\x60\x20\x80\x81\x43\x06\x00\
\x00\x21\xa0\xc1\x41\x80\x18\x20\x28\x40\x60\x81\x83\x03\x04\x00\
\x00\x01\xc1\xc3\x03\x00\x18\x30\x60\xc0\xe0\x81\x82\x06\x04\x00\
\x00\x40\x01\x83\x82\x00\x30\x38\x40\xc0\x80\xc1\x02\x06\x86\x00\
\x00\x40\x01\x82\x04\x00\x60\x30\x70\xc1\x81\xc1\x06\x84\x86\x00\
\x00\x00\x03\x86\x0c\x00\x60\x70\x00\x81\x21\xc3\x06\x04\x82\x00\
\x00\x80\x06\x07\x0c\x08\x48\x70\x01\x83\x01\x83\x04\x0c\x02\x00\
\x00\x83\xfc\x05\x08\x00\xc8\x60\x03\x03\x03\x82\x0d\x0c\x02\x00\
\x00\x86\x01\x0c\x18\x00\xc0\x60\x0e\x42\x43\x87\x0d\x08\x42\x00\
\x00\x06\x01\x0e\x18\x10\x90\xe0\x08\x06\x43\x07\x08\x18\x42\x00\
\x01\x04\x00\x0a\x10\x01\x90\xe0\x08\x06\x03\x04\x08\x18\x42\x00\
\x01\x04\x02\x08\x10\x01\x80\xc1\x08\x84\x87\x0e\x1a\x10\x02\x00\
\x00\x0c\x02\x1c\x30\x21\x81\xc1\x08\x04\x06\x0e\x10\x30\x03\x00\
\x02\x08\x02\x1c\x20\x20\xc1\xc3\x08\x06\x06\x0c\x10\x30\x43\x00\
\x02\x08\x00\x14\x20\x20\x83\x03\x08\x06\x0e\x0c\x34\x20\x43\x00\
\x00\x18\x04\x38\x60\x00\x02\x03\x08\x00\x18\x1c\x34\x20\x43\x00\
\x04\x18\x04\x38\x3f\x00\x06\x87\x08\x80\x30\x1c\x38\x6f\x82\x00\
\x04\x10\x00\x28\x01\x80\x0c\x87\x08\x00\x20\x18\x00\x60\x02\x00\
\x04\x30\x08\x68\x01\x10\x18\x05\x08\x00\x64\x38\x00\x60\x06\x00\
\x08\x30\x08\x68\x01\x00\x31\x0d\x08\x40\xc0\x38\x00\xc0\x04\x00\
\x08\x20\x08\x44\x03\x08\x61\x0d\x08\x23\x84\x78\x01\xa0\x0c\x00\
\x08\x20\x0f\xc3\xfe\x07\xc1\xf8\xf8\x3e\x07\xff\xff\x3f\xf8\x00\
\x00\x60\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x10\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x10\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x20\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x20\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x01\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x61\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x3f\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")


# gameover screen bytearray


gameover = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x02\x01\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\
\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\
\x00\x20\x7e\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\
\x00\x40\x80\x00\x00\x00\x00\x00\x00\x00\x20\x40\x00\x00\x00\x00\
\x00\x81\x00\x00\x00\x00\x00\x00\x00\x00\x60\x40\x00\x00\x00\x00\
\x00\x82\x00\x00\x00\x00\x01\xfd\x00\x20\xc0\xc0\x00\xfe\x80\x00\
\x00\x06\x00\x21\x08\xc0\x0e\x01\x80\x01\x80\xc2\x47\x00\xe0\x00\
\x01\x04\x00\x01\x00\xc1\x0c\x01\x00\x01\x00\xc2\x06\x00\x80\x04\
\x01\x08\x00\x41\x10\xc0\x0c\x01\x00\x43\x21\x82\x86\x00\x80\x04\
\x00\x08\x00\x03\x10\x82\x1c\x1f\x00\x42\x21\x83\x0e\x0f\x83\x04\
\x02\x08\x00\x83\x00\x80\x18\x30\x00\x02\x01\x03\x08\x18\x47\x8c\
\x02\x1f\xe0\x02\x00\x80\x18\x60\x00\x86\x41\x46\x18\x30\x04\x08\
\x00\x18\x11\x02\x20\x80\x38\x40\x00\x84\x43\x06\x14\x20\x85\x08\
\x04\x18\x10\x02\x00\x80\x38\x40\x00\x04\x02\x04\x34\x20\x85\x18\
\x04\x30\x32\x02\x00\x80\x30\xc0\x01\x04\x82\x04\x20\x60\x0c\x10\
\x04\x30\x20\x06\x40\x80\x30\x0c\x01\x0c\x86\x80\x68\x06\x0c\x10\
\x08\x38\x24\x06\x00\x80\x70\x0c\x00\x08\x84\x80\x48\x07\x00\x30\
\x08\x68\x64\x04\x00\x80\x60\x08\x00\x08\x04\x80\xc0\x04\x00\x60\
\x08\x48\x40\x04\x80\xc0\x60\x08\x02\x19\x0c\x00\x90\x04\x01\xc0\
\x00\x40\x48\x04\x80\x80\xe0\x18\x02\x11\x08\x01\x90\x0e\x01\x80\
\x10\xd0\xc0\x84\x08\x88\xc1\xf0\x00\x10\x08\x01\x00\xf8\x01\x80\
\x10\xd0\xd1\x8d\x18\x10\xc3\x00\x04\x12\x09\x01\x01\x80\x21\x80\
\x00\x80\x81\x8d\x18\x11\xc2\x00\x04\x14\x19\x03\x21\x04\x21\x80\
\x20\x80\xa1\x08\x18\x31\x82\x00\x04\x18\x11\x02\x21\x04\x21\x80\
\x21\xa1\x80\x0a\x10\x21\x86\x00\x04\x00\x31\x06\x03\x00\x21\x80\
\x00\xc1\x40\x0a\x38\x61\x86\x40\x04\x00\x60\x04\x43\x28\x61\x80\
\x00\x01\x00\x08\x38\xe3\x80\x60\x00\x00\xc0\x0c\x40\x38\x61\x80\
\x00\x03\x80\x0c\x38\xc3\x00\x40\x02\x01\x82\x08\x00\x30\x41\x80\
\x20\x03\x0f\x1c\x49\xc3\x00\x40\x00\x03\x02\x18\x80\x30\xc1\x80\
\x1c\x07\x99\x1c\x4b\x47\x00\xc0\x01\x0e\x02\x10\x80\x70\x91\x80\
\x07\x9e\xf1\xf3\xce\x3c\xff\x80\x00\xf8\x01\xf0\x7f\xcf\x9f\x00\
\x00\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")











# setup the two images in framebuffers for display

picoroids = framebuf.FrameBuffer(splash, 128, 64, framebuf.MONO_HLSB)
go = framebuf.FrameBuffer(gameover, 128, 64, framebuf.MONO_HLSB)



# function to input a name for the high score board. Max 8 characters.
#
# left / right controls the cursor. fire / thrust moves individual letter up or down
#
# when done, hyperspace chooses the name. Whitespace is removed.
#

def getname():

    player = "New     "    # default new name to choose
    
    cursor=0

    player2 = ""
    player2 = "       "[:cursor] + "_"  # cursor indicator at position cursor

    chosen=0
    while chosen==0:
        oled.fill(0)
        oled.text("New High Score!",0,0)

        oled.text(player2,30,15)
        oled.text(player,30,30)
        oled.text(player2,30,38)
        oled.show()

        if button_right.value()==1:
            cursor+=1
            time.sleep(.1)

        if button_left.value()==1:
            cursor-=1
            time.sleep(.1)

        if cursor<0:
            cursor=0
        if cursor>8:
            cursor =8
        player2 = "       "[:cursor] + "_"


        if button_fire.value()==1:
            oc = ord(player[cursor])
            oc += 1
            if oc<32:
                oc=32


            player = player[:cursor]+ chr(oc)+player[cursor+1:]

            time.sleep(.2)

        if button_thrust.value()==1:
            oc = ord(player[cursor])
            oc -= 1
            if oc>127:
                oc=127


            player = player[:cursor]+ chr(oc)+player[cursor+1:]

            time.sleep(.2)

        if button_hyperspace.value()==1:
            chosen=1

    
    player =player.strip()


    return player









# rotate an x coordinate around the axis by rot amount in radians. y needs to be provided

def rotate_x(x,y,rot):
    x2 = (x * math.cos(rot))-(y*math.sin(rot))
    return x2

# same for a y coordinate  
def rotate_y(x,y,rot):
    y2 = (y * math.cos(rot))+(x*math.sin(rot))
    return y2


# pixel collision test - not used

def collision_pixel(x,y):
    test=0
    for test_x in range(0,5):
        for test_y in range(0,5):
            tes = oled.pixel(x+test_x-2,y+test_y-2)
            if tes ==1:
                test =1
                
    return test




# break an asteroid - if it's a large asteroid, convert ito to one level smaller, and spawn another one
#
# if it's the smallest asteroid, remove it from the asteroid list
#
# asteroids are held in a list, 6 items per asteroid
#
# type , x, y, x movement, y movement, rotation

def break_asteroid(ass):
   
        if asteroids[int(ass*6)] < 3:  # asteroid isnt the smallest
            asteroids[int(ass*6)] += 1  # reduce asteroid size
            asteroids[int(ass*6)+3] = (random.randrange(1,6)-3)/10  # randomize movement
            asteroids[int(ass*6)+4] = (random.randrange(1,6)-3)/10
            asteroids[int(ass*6)+5] =(random.randrange(1,6)-3)/1000
            # add another asteroid to the list
            asteroids.append (asteroids[int(ass*6)])
            asteroids.append (asteroids[int(ass*6)+1])
            asteroids.append (asteroids[int(ass*6)+2])
            asteroids.append (((random.randrange(1,6)-3)/10)*asteroids[int(ass*6)]) # asteroid is smaller, so
            asteroids.append (((random.randrange(1,6)-3)/10)*asteroids[int(ass*6)]) # make faster
            asteroids.append ((random.randrange(1,6)-3)/1000)
          
        else:   # it's a 3 asteroid, so remove it!
            for f in range(6):
                asteroids.pop(int(ass*6))   # remove all 6 values for the asteroid
            


# check a single pixel at given coordinates. This is used by the ship collision system
#
# this is called before the ship is drawn. check each vertex for a pixel already there.
# if there is, it's a collision!

def check_ship(xxxx,yyyy):
    crash=0
    if oled.pixel(xxxx,yyyy)==1:
        crash =1
    return crash



# main collision system for ship

def collision():
    # collision check for ship
    collision =0
    for i in range(0,8,2):

        xx =  int(ship_x)+int(rotate_x(ship_1[i],ship_1[i+1],rotation))
        yy =  int(ship_y)+int(rotate_y(ship_1[i],ship_1[i+1],rotation))
      

        # check vertex

        if check_ship(xx,yy):
            collision =1
      
      # check for collisions on wraparound screen if needed
    
        if xx<0 :
            if check_ship(xx+128,yy):
                collision =1
          
        if yy<0 :
            if check_ship(xx,yy+64):
                collision =1
          
        if xx>127:
            if check_ship(xx-128,yy):
                collision =1
          
        if yy>63:
            if check_ship(xx,yy-64):
                collision =1


# let's be clever, we need to draw asteroids first, then the ship, then bullets, then the text so that collisions are
# checked only for asteroids

# end ship collision check
    return collision




# spawn a new bullet

def fire():
    AUTOPLAY_MODE=False    # firing, so not in demo mode anymore!
    bullets.append(ship_x)
    bullets.append(ship_y)
    bullets.append(20)   # bullet age
    bullets.append(rotate_x(0,bullet_speed,rotation))    # to be added onto x,y every frame.
    bullets.append(rotate_y(0,bullet_speed,rotation))


# add a new asteroid to the field
def new_asteroid():
    as_x = 0
    as_y = 0
    ok=0
    while ok==0:
       
        as_x = random.randrange(10,117)
        as_y = random.randrange(10,53)

        # don't spawn right in front of ship
        if as_x<40 or as_x>80:
            ok=1
        else:
            ok=0
        if as_y<20 or as_y>50:
            ok=1
        else:
            ok=0


    asteroids.append(1)
    asteroids.append(as_x)
    asteroids.append(as_y)
    asteroids.append((random.randrange(0,6)-3)/5)
    asteroids.append((random.randrange(0,6)-3)/5)
    asteroids.append(-.002)




# init blank bullet list

bullets=[]  

# High scores table

high_scores=["Andy","999","Crook","999","Pico","400","Pi","350","Rasp","200","Python","150"]


# some initial variables.
# waiting on splash screen
# countdown resets when a bullet fires. Set to 0 for lots of bullets :)
# level of play start on level 1 (2 astros). each level increses by 1 astro
# bullet speed. Can't remember what this does.....

waiting =1
countdown=0
level =1
bullet_speed = 4




# main game loop
while True:

    looped =0
    while waiting:

        # show splash screen
        oled.fill(0)
        oled.blit(picoroids, 0,0,2) 
        oled.show()

        looped+=1

        # if the splash screen / high scores has looped a lot, 
        if looped >1:
            AUTOPLAY_MODE= True 
            waiting=0


        # wait on splash screen for fire button to start
        for wait in range(0,200000):
            a = math.cos(2) # this is meaningless :) just give something to do....
            # sense for button press here and break
            if button_fire.value() == 1:
                AUTOPLAY_MODE= False  # pressed a button, so clearly playing!!
                waiting =0
                break

        # scroll through the high scores list
        if waiting ==1:
            for scroll in range((16 * len(high_scores))):
                oled.fill(0)
                for o in range(0,len(high_scores),2):
                    if o==0:
                        just = int((128-(len("HIGH SCORES")*8))/2)
                        oled.text("HIGH SCORES",just,10+(o*8)-scroll)
                    text = str(high_scores[o] +" - "+ high_scores[o+1])
                    just = int((128-(len(text)*8))/2)
                    oled.text(text,just,36+(o*8)-scroll)
                for o in range(0,len(high_scores),2):
                    if o==0:
                        just = int((128-(len("HIGH SCORES")*8))/2)
                        oled.text("HIGH SCORES",just,10+(o*8)-scroll+(8 * int(len(high_scores)/2))+24+64)
                    text = str(high_scores[o] +" - "+ high_scores[o+1]) 
                    just = int((128-(len(text)*8))/2)  
                    oled.text(text,just,36+(o*8)-scroll+(8 * int(len(high_scores)/2))+24+64)
                
                oled.show()
                time.sleep(0.1)
                # sense for button press here and break the for loop scroll
                if button_fire.value() == 1:
                    AUTOPLAY_MODE= False    # pressed a button, so clearly playing!!
                    waiting =0
                    break
                    
            #time.sleep(10)
        if AUTOPLAY_MODE == True:       # get beyond splash screen in auto mode after high scores
            waiting =0



    game_on =1   # not kidding! GAME ON!





#setup default ship

    # these are vertices of the ship to draw, x y location and rotation (up) for the default ship

    ship_1 = (0,5,3,-3,0,-1,-3,-3,0,5)
    ship_x = 64
    ship_y = 32
    rotation = 3.14

    # asteroids vector descriptions
    asteroid_1 = (-2,6,3,5,5,0,-1,-3,-3,-2,-2,6)
    asteroid_2 = (-2,4,2,3,4,0,-1,-2,-3,-2,-2,4)
    asteroid_3 = (-2,3,2,3,3,0,-1,-2,-2,-2,-1,2)

    asteroid_1_x =30
    asteroid_1_y = 30
    asteroid_1_rot =.2


    # ship thrust, rotation and values to help accelerate the ship in x y space
    thrust =0
    thrust_rotation =0
    accel_x =0
    accel_y=0

    # limits for acceleration and how much to slow the ship down
    topaccel=1
    botaccel=-1
    slowdown = 0.01

    # score for the game, number of lives and set immunity from collision to 10
    score = 0
    lives = 3
    immunity = 10

    # countdown for hyperspace function. 0 = available
    hyper_countdown=0

    # initialise 2 asteroids
    # asteroid   type  x    y  x_speed    y_speed  rotation
    #asteroids=[1,20,10,(random.randrange(0,6)-3)/5,(random.randrange(0,6)-3)/5,-.002,1,100,10,(random.randrange(0,6)-3)/5,(random.randrange(0,6)-3)/5,-.002]
    asteroids=[]
    new_asteroid()
    new_asteroid()
 


    




    while game_on:
        # Clear the oled display in case it has junk on it.
        oled.fill(0)


        if AUTOPLAY_MODE == True:

            if random.randrange(0,85)==2:   # fire bullet

                fire()
                score -= 1    # costs a point to fire
                if score < 0:
                    score =0

        if button_fire.value() == 1 and countdown ==0:
            countdown=5                                  # wait until firing again
            fire()
            score -= 1    # costs a point to fire
            if score < 0:
                score =0
        else:
            countdown -=1
            if countdown<0:
                countdown =0









    # draw asteroids


        asteroid_1_rot += 0.05
        asteroid_1_x += 0.6
        asteroid_1_y += 0.35

        if asteroid_1_y > 64:
            asteroid_1_y =asteroid_1_y-64
        if asteroid_1_y < 0:
            asteroid_1_y = asteroid_1_y+64
        if asteroid_1_x > 128:
            asteroid_1_x = asteroid_1_x-128
        if asteroid_1_x <0:
            asteroid_1_x = asteroid_1_x + 128

        if len(asteroids)>5:  # if there are asteroids to show....
            for i in range(0,len(asteroids)/6):
        # asteroid   type  x    y  x_speed    y_speed  rotation
                asteroid_1_x = asteroids[(i*6)+1]
                asteroid_1_y = asteroids[(i*6)+2]
                inc_x = asteroids[(i*6)+3]
                inc_y = asteroids[(i*6)+4]
                asteroid_1_rot = asteroids[(i*6)+5]
                if i % 2:
                    asteroids[(i*6)+5] += 0.05
                else:
                    asteroids[(i*6)+5] -= 0.05
           

                if  asteroids[(i*6)+5] > 6.28:
                    asteroids[(i*6)+5]-=6.28
                if  asteroids[(i*6)+5] <0:
                    asteroids[(i*6)+5]+=6.28


                asteroids[(i*6)+1] += inc_x
                asteroids[(i*6)+2] += inc_y

                if asteroids[(i*6)+2] > 64:
                    asteroids[(i*6)+2] =asteroids[(i*6)+2]-64
                if asteroids[(i*6)+2] < 0:
                    asteroids[(i*6)+2] = asteroids[(i*6)+2]+64
                if  asteroids[(i*6)+1] > 128:
                    asteroids[(i*6)+1] =  asteroids[(i*6)+1]-128
                if  asteroids[(i*6)+1] <0:
                    asteroids[(i*6)+1] =  asteroids[(i*6)+1] + 128



                for u in range(0,10,2):
                    if asteroids[(i*6)] ==1:
                        xx=int(asteroid_1_x)+int(rotate_x(asteroid_1[u],asteroid_1[u+1],asteroid_1_rot))
                        yy= int(asteroid_1_y)+int(rotate_y(asteroid_1[u],asteroid_1[u+1],asteroid_1_rot))
                        xxx=int(asteroid_1_x)+int(rotate_x(asteroid_1[u+2],asteroid_1[u+3],asteroid_1_rot))
                        yyy= int(asteroid_1_y)+int(rotate_y(asteroid_1[u+2],asteroid_1[u+3],asteroid_1_rot) )

                        oled.line(xx, yy,  xxx,yyy ,1)
                        if (xx<0) or (xxx<0):
                            oled.line(xx+128, yy,  xxx+128,yyy ,1)
                        if (yy<0) or (yyy<0):
                            oled.line(xx, yy+64,  xxx,yyy +64,1)
                        if (xx>127) or (xxx>127):
                            oled.line(xx-128, yy,  xxx-128,yyy ,1)
                        if (yy>63) or (yyy>63):
                            oled.line(xx, yy-64,  xxx,yyy-64 ,1)
                        
                   
                    if asteroids[(i*6)] ==2:
                        xx=int(asteroid_1_x)+int(rotate_x(asteroid_2[u],asteroid_2[u+1],asteroid_1_rot))
                        yy= int(asteroid_1_y)+int(rotate_y(asteroid_2[u],asteroid_2[u+1],asteroid_1_rot))
                        xxx=int(asteroid_1_x)+int(rotate_x(asteroid_2[u+2],asteroid_2[u+3],asteroid_1_rot))
                        yyy= int(asteroid_1_y)+int(rotate_y(asteroid_2[u+2],asteroid_2[u+3],asteroid_1_rot) )

                        oled.line(xx, yy,  xxx,yyy ,1)
                        if (xx<0) or (xxx<0):
                            oled.line(xx+128, yy,  xxx+128,yyy ,1)
                        if (yy<0) or (yyy<0):
                            oled.line(xx, yy+64,  xxx,yyy +64,1)
                        if (xx>127) or (xxx>127):
                            oled.line(xx-128, yy,  xxx-128,yyy ,1)
                        if (yy>63) or (yyy>63):
                            oled.line(xx, yy-64,  xxx,yyy-64 ,1)

                    if asteroids[(i*6)] ==3:
                        xx=int(asteroid_1_x)+int(rotate_x(asteroid_3[u],asteroid_3[u+1],asteroid_1_rot))
                        yy= int(asteroid_1_y)+int(rotate_y(asteroid_3[u],asteroid_3[u+1],asteroid_1_rot))
                        xxx=int(asteroid_1_x)+int(rotate_x(asteroid_3[u+2],asteroid_3[u+3],asteroid_1_rot))
                        yyy= int(asteroid_1_y)+int(rotate_y(asteroid_3[u+2],asteroid_3[u+3],asteroid_1_rot) )

                        oled.line(xx, yy,  xxx,yyy ,1)
                        if (xx<0) or (xxx<0):
                            oled.line(xx+128, yy,  xxx+128,yyy ,1)
                        if (yy<0) or (yyy<0):
                            oled.line(xx, yy+64,  xxx,yyy +64,1)
                        if (xx>127) or (xxx>127):
                            oled.line(xx-128, yy,  xxx-128,yyy ,1)
                        if (yy>63) or (yyy>63):
                            oled.line(xx, yy-64,  xxx,yyy-64 ,1)
                    
    # end asteroids



















    # ship movements


        if AUTOPLAY_MODE==True:
            if random.randrange(0,15)==2:

                rotation += 0.4
        
        if button_left.value() ==1:
            rotation -=.2
          #  thrust_rotation = rotation 
        if button_right.value() ==1:
            rotation +=.2
          #  thrust_rotation = rotation 






   



      




        if AUTOPLAY_MODE==True:
            if random.randrange(1,3) == 2:
                if thrust == 0:
                    thrust += random.randrange(1,4)
                    thrust_rotation = rotation     ## set thrust rotation to current vector

        if thrust >0:
            thrust -= 0.02
        if thrust <0:
            thrust = 0


        if button_thrust.value()==1:
            thrust +=.08
            if thrust>3:
                thrust =3

            thrust_rotation = rotation 

            accel_x += rotate_x(0,thrust,thrust_rotation)
            accel_y += rotate_y(0,thrust,thrust_rotation)

        ship_x+= accel_x
        ship_y+= accel_y

       
        if accel_x>topaccel:
            accel_x=topaccel
        if accel_y>topaccel:
            accel_y=topaccel
        if accel_x<botaccel:
            accel_x=botaccel
        if accel_y<botaccel:
            accel_y=botaccel




        if accel_x>0:
            accel_x-=slowdown
        else:
            accel_x+=slowdown
        
        if accel_y>0:
            accel_y-=slowdown
        else:
            accel_y+=slowdown

        if accel_x <= slowdown and accel_x>0:
            accel_x=0
        if accel_y <= slowdown and accel_y>0:
            accel_y=0

        if accel_x >= (slowdown*-1) and accel_x<0:
            accel_x=0
        if accel_y >= (slowdown*-1) and accel_y<0:
            accel_y=0

        


        # move ship across boundaries for infite play

        if ship_y > 64:
            ship_y = ship_y-64
        if ship_y < 0:
            ship_y = ship_y+64
        if ship_x > 128:
            ship_x = ship_x-128
        if ship_x <0:
            ship_x = ship_x + 128



        # if hyperspace is allowed
        if button_hyperspace.value() ==1 and hyper_countdown==0:
            ship_x = random.randrange(10,117)
            ship_y = random.randrange(10,53)
            immunity=30
            hyper_countdown=200
        hyper_countdown-=1
        if hyper_countdown<0:
            hyper_countdown=0



    # end ship movement










        if immunity==0:    # if ship is not immune, check for collision

            coll = collision()

            if coll ==1:
                # player is dead
                lives-=1
                ship_x=64
                ship_y=32
                rotation=3.14
                thrust=0
                time.sleep(1)
                immunity = 30      # set so that the ship isn't destroyed by same asteroid
                accel_x =0
                accel_y=0

                if lives <1:
                    game_on =0    # end of game, so escape the loop
                
                
                
                







        # do all bullets

        if len(bullets)>4:   # theres at least one bullet!
            for b in range(len(bullets)/5):
                bx = bullets[(b*5)]
                by = bullets[((b*5)+1)]
                age = bullets[((b*5)+2)]
                bxx = bullets[((b*5)+3)]
                byy = bullets[((b*5)+4)]
           
                bullets[((b*5)+2)] -= 1  # dec age by 1
                bullets[(b*5)] += bxx     # add vector to bullet
                bullets[((b*5)+1)] += byy
                # wraparound
                if bullets[(b*5)]<0:
                    bullets[(b*5)]+=128
                if bullets[(b*5)]>127:
                    bullets[(b*5)]-=128
                if bullets[((b*5)+1)]<0:
                    bullets[((b*5)+1)]+=64
                if bullets[((b*5)+1)]>63:
                    bullets[((b*5)+1)]-=64

                bullet_x=int(bullets[(b*5)])
                bullet_y=int(bullets[((b*5)+1)])



                oled.pixel(bullet_x,bullet_y,1)


                # check for collision with rocks - collsion is based on distance to origin
                if len(asteroids)>5:  # if there are asteroids to show....
                    break_a =-1
                    for i in range(0,len(asteroids)/6):
                        asteroid_1_x = asteroids[(i*6)+1]
                        asteroid_1_y = asteroids[(i*6)+2]
                        asteroid_type = asteroids[(i*6)]

                        x_dist = bullet_x-asteroid_1_x
                        y_dist = bullet_y-asteroid_1_y
                        
                        if x_dist <0:
                            x_dist = x_dist *-1
                        if y_dist <0:
                            y_dist = y_dist *-1

                        if x_dist<(9/asteroid_type) and y_dist <(9/asteroid_type):   # harder to hit smaller rocks
                      
                            bullets[(b*5)+2] = 0  # reduce age to 0
                            break_a =i
                    
                    if break_a>=0:
                        break_asteroid(break_a)
                        score += 25
        if len(bullets)>4:
            for b in range(int((len(bullets)/5))):

                age=1
                if ((b*5)+2)< len(bullets):
                    age = bullets[((b*5)+2)]   # problem!!!!
                if int(age)< 1:
               
                    for a in range(0,5):
                        bullets.pop(int((b*5)))   # remove 
                    b=100  # exit loop

    # bullets over
















        immunity -= 1

        if immunity <0:
            immunity =0


        # draw ship

        if immunity % 2 or immunity ==0:  # if immunity is decreasing, flash the ship so show immune status

            for i in range(0,8,2):

                xx =  int(ship_x)+int(rotate_x(ship_1[i],ship_1[i+1],rotation))
                yy =  int(ship_y)+int(rotate_y(ship_1[i],ship_1[i+1],rotation))
                xxx = int(ship_x)+int(rotate_x(ship_1[i+2],ship_1[i+3],rotation))
                yyy = int(ship_y)+int(rotate_y(ship_1[i+2],ship_1[i+3],rotation))
        
                oled.line(xx,yy,+xxx,yyy,1)
            
                if xx<0 or xxx<0:
                    oled.line(128+xx,yy,128+xxx,yyy,1)

                if yy<0 or yyy<0:
                    oled.line(xx,64+yy,xxx,64+yyy,1)

                if xx>127 or xxx>127:
                    oled.line(xx-128,yy,xxx-128,yyy,1)

                if yy>63 or yyy>63:
                    oled.line(xx,yy-64,xxx,yyy-64,1)





        if len(asteroids)<4:
        # no asteroids left!

            level+=1   # increase the level

            # add new asteroids for new level
            for ll in range(0,level):
                new_asteroid()
                immunity=10









    # draw extras on screen - lives, hyperspace and score

        if score>999:
            score = 999
            
        oled.text(("{:>3}".format(str(score)).replace(" ","0")),102,0)
        oled.text("^^^"[:lives],0,0)
        if hyper_countdown==0:
            oled.text("X",30,0)



    # finally, show it all
        oled.show()



    # loop escaped, so it's game over - show splash screen

    oled.fill(0)
    oled.blit(go, 0,0,2) 
    oled.show()
    time.sleep(5)


    # if playing the game, allow input of high score to the table

    if AUTOPLAY_MODE==False:
        # input high score
        for h in range(0,len(high_scores)/2,2):
            if score> int(high_scores[(h+1)]):
                name="NEW"
                name = getname()
                high_scores.insert(h,name)
                high_scores.insert(h+1,str(score))
                break



    game_on =0 # reset game to main loop and splash screen
    waiting =1


    
