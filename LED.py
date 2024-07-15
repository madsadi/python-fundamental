#from luma.led_matrix.device import ws2812

from luma.led_matrix.device import max7219 # <-- MAX7219 device
from luma.core.interface.serial import spi, noop # <-- SPI interface
from luma.core.render import canvas # <-- Canvas for drawing
from luma.core.legacy.font import CP437_FONT, TINY_FONT, LCD_FONT, SEG7_FONT, SINCLAIR_FONT #<-- import fonts
from luma.core.legacy import text #<-- show text
from luma.core.virtual import viewport #<-- virtual viewport
from time import sleep
import numpy as np

#-------- setup of our devices ------------------------------------------
spi_connection = spi(port=0, device=1, gpio=noop()) # <- setup of SPI
led_driver = max7219(spi_connection, cascaded=1, block_orientation=90, rotate=0) # <- Max7219

# ------------- setup a new virtual viewport ---------------------------
my_vp = viewport(led_driver, width=200, height=100)
# -----------------------------------------------------------------------

message1 = "Hello guys"

#-------- create a canvas to draw upon ----------------------------------------------------
while 1:

    with canvas(led_driver) as draw:
        # text(draw, (0,0), 'S', fill="white", font=CP437_FONT) #white means that led turned on , it is defined by turn on leds
        # draw.line([0, 0, 7, 7], fill="white")
        # draw.rectangle([0,0,7,7], fill="white", outline="white") #it means the whole screen will be turned on
        # draw.line([0, 0, 7, 7], fill="black")
        draw.rectangle([0, 7, 1, 8-0.5*8], fill="white", outline="white")
        # draw.line([2, 7, 2, 7], fill="white")
        # draw.rectangle([3, 7, 4, 0.7*7], fill="white", outline="white")
        # draw.line([5, 7, 5, 7], fill="white")
        # draw.rectangle([6, 7, 7, 0.1*7], fill="white", outline="white")
        # draw.line([0, 0, 7, 7], fill="white")
        # draw.line([0,7,1,7], fill="white")
        # draw.point([0,3], fill="white")


# -------------------------- writting a code that counts from 9 to 0 ---------------------
# while 1:
#     for x in range(0, 10):
#         y = str(9-x) # for counting downward
#         print(y)
#         with canvas(led_driver) as draw:
#             text(draw, (0, 0), y, fill="white", font=SEG7_FONT)
#             sleep(0.5)
#     sleep(2)

# ------------------------- a code to write the message1 -----------------
# while 1:
#     for char in message1:
#         with canvas(led_driver) as draw:
#             text(draw, (0, 0), char, fill="white", font=SEG7_FONT)
#             sleep(0.5)
#     sleep(2)

# ------------ virtual viewport code --------------------------------------
# message2 = "welcome to campus soest!"
# while 1:
#     with canvas(my_vp) as draw:
#         text(draw, (0, 0), message2, fill="white", font=SEG7_FONT)
#
#     for i in range(0, len(message2)*8):
#         my_vp.set_position((i,0))
#         sleep(0.05)

#------------------ Graph code ---------------------------------------------
# while 1:
#     #data = [50, 42, 23, 56, 89, 98 , 5, 67] #dateset
#     data = np.random.rand(8,1) #dataset
#     normalised_date = np.zeros(8)
#     print(data,'here',len(data))
#     for i in range(0, len(data)):
#         #normalised_date[i] = 8.0*(data[i]/100.0)
#         normalised_date[i] = 8.0 * ((data[i]*100.0) / 100.0)
#         print(normalised_date[i])
#     while 1:
#         with canvas(led_driver) as draw:
#             for i in range(0, len(normalised_date)):
#                 draw.line((i,7,i,8-normalised_date[i]), fill="white")
#
#     sleep(10)

#-------------------------------------------------------------------