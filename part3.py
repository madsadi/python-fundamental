from Adafruit_LED_Backpack import SevenSegment
import RPi.GPIO as GPIO
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas

# Pin setup
left_button = 25
right_button = 19
up_button = 26
down_button = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(left_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(up_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(down_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

spi_connection = spi(port=0, device=1, gpio=noop())  # <- setup of SPI
device = max7219(spi_connection, cascaded=1, block_orientation=90, rotate=0)  # <- Max7219

x, y = 0, 4
button_pressed = 0

# Function to display numbers on seven-segment display
def display_number(btn_number):
    my_7SD = SevenSegment.SevenSegment(address=0x70)
    my_7SD.begin()
    my_7SD.print_number_str(str(btn_number))
    my_7SD.write_display()


pixels = set()
pixels.add((x, y))


def update_display():
    with canvas(device) as draw:
        for pixel in pixels:
            draw.point(pixel, fill="white")


while True:
    if not GPIO.input(left_button):
        button_pressed = 1
        x -= 1
    elif not GPIO.input(right_button):
        button_pressed = 2
        x += 1
    elif not GPIO.input(up_button):
        button_pressed = 3
        y -= 1
    elif not GPIO.input(down_button):
        button_pressed = 4
        y += 1
    else:
        button_pressed = 0

    pixels.add((x, y))
    display_number(button_pressed)
    update_display()
    time.sleep(0.1)
