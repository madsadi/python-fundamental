#------ Import Libraries ------

# Importing the GPIO library
import RPi.GPIO as RPI

# Import sleep method
from time import sleep

# -------- Pin Assignment ------#

# Input pins:
gpio_pin_input_btn_left = 25
gpio_pin_input_btn_right = 19
gpio_pin_input_btn_up = 26
gpio_pin_input_btn_down = 15

# Output Pins:
gpio_pin_output_buzzer = 18
gpio_pin_output_relay = 21
gpio_pin_output_vibration = 27

# ------ Setup of GPIO Pins --------- #

# Setting the numbering system for GPIOs
RPI.setmode(RPI.BCM) # <-- use the GPIO numbering system

# Defining Input Pins:
gpio_pins_input = [gpio_pin_input_btn_left,gpio_pin_input_btn_up,gpio_pin_input_btn_right]

# All input pins shall be defined as inputs with deactivated PUD
RPI.setup(gpio_pins_input, RPI.IN, pull_up_down=RPI.PUD_OFF)

# Defining Output Pins:
gpio_pins_output = [gpio_pin_output_vibration,gpio_pin_output_relay,gpio_pin_output_buzzer]

# All output pins shall be defined as outputs with deactivated PUD
RPI.setup(gpio_pins_output, RPI.OUT, pull_up_down=RPI.PUD_OFF)

# ---------- FOREVER - LOOP ----------- #
while 1:

    for pin in gpio_pins_input:
        if not RPI.input(pin):  # <--- There was a button pressed
            if pin == gpio_pin_input_btn_up: #<--- UP button was pressed
                RPI.output(gpio_pin_output_buzzer, RPI.HIGH) #<-- turn on buzzer
                sleep(1)
                RPI.output(gpio_pin_output_buzzer, RPI.LOW) #<-- turn on buzzer
            if pin == gpio_pin_input_btn_left:  # <--- UP button was pressed
                RPI.output(gpio_pin_output_relay, RPI.HIGH)  # <-- turn on buzzer
                sleep(1)
                RPI.output(gpio_pin_output_relay, RPI.LOW)  # <-- turn on buzzer
            if pin == gpio_pin_input_btn_right:  # <--- UP button was pressed
                RPI.output(gpio_pin_output_vibration, RPI.HIGH)  # <-- turn on buzzer
                sleep(1)
                RPI.output(gpio_pin_output_vibration, RPI.LOW)  # <-- turn on buzzer

        state = RPI.input(pin)
        print(pin)
        print(state)
        sleep(0.5)

