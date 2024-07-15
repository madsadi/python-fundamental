import time
import RPi.GPIO as RPI

# ----- Button setup ----- #
gpio_pin_input_touch = 17

RPI.setmode(RPI.BCM)

RPI.setup(gpio_pin_input_touch,RPI.IN)

CurrentTime = 0
while 1:
    StartTime = time.time()

    while RPI.input(gpio_pin_input_touch) == 0:
        CurrentTime = time.time()
    while RPI.input(gpio_pin_input_touch) == 1:
        a = 0
        
    TimeDifference = CurrentTime - StartTime
    print(TimeDifference)
