#----- Import libraries -----#
import time
import RPi.GPIO as RPI
from Adafruit_LED_Backpack import SevenSegment

# ----- Define 7SD object -----
segment_display = SevenSegment.SevenSegment(address=0x70)

#----- initialise 7SD object -------#
segment_display.begin()


# ---- Definition and initialise of GPIO pins----#

gpio_output_trigger_us = 16
gpio_input_echo_us =12

RPI.setmode(RPI.BCM) # <- The GPIO numbering system
RPI.setup(gpio_input_echo_us, RPI.IN, pull_up_down=RPI.PUD_OFF)
RPI.setup(gpio_output_trigger_us, RPI.OUT, pull_up_down=RPI.PUD_OFF)

#---- Set GPIO pins to an initialised state ----#
RPI.output(gpio_output_trigger_us, False) # <- Setting trigger to False


#----Forever loop---#
while 1:
    RPI.output(gpio_output_trigger_us, True)  # <- Setting trigger to False
    time.sleep(0.001)  # <- wait
    RPI.output(gpio_output_trigger_us, False)  # <- Setting trigger to True
    print('Measurement started')

    #wait for rising edge of echo pin
    while not RPI.input(gpio_input_echo_us):
        t_rising = time.time()
    print(t_rising)
    #wait for falling edge of echo pin
    while RPI.input(gpio_input_echo_us):
        t_falling = time.time()
    print(t_falling)

    #Build time difference
    t_echo = t_falling - t_rising
    distance  = t_echo * 17241
    distance_string = str(int(round(distance, 0)))

    for index in range(0, len(distance_string)):
        segment_display.set_digit(index, distance_string[index])

    # ----- update of 7SD ---------
    segment_display.write_display()

    print(distance)

    print('Measurement stopped')
    time.sleep(2)