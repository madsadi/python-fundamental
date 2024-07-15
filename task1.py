import RPi.GPIO as RPI
import time
from Adafruit_LED_Backpack import SevenSegment
import numpy as np
import matplotlib.pyplot as plt

# Define pin numbers
gpio_pin_input_pin_trigger = 16
gpio_pin_input_pin_echo = 12
gpio_pin_input_btn_left=25
gpio_pin_input_btn_right=19
gpio_pin_input_btn_up = 26
gpio_pin_input_btn_down = 13
gpio_pin_output_buzzer = 18
alpha = 17241.0

gpio_pins_input = [gpio_pin_input_btn_left,gpio_pin_input_btn_up,gpio_pin_input_btn_right,gpio_pin_input_btn_down]
gpio_pins_output = [gpio_pin_output_buzzer,gpio_pin_input_pin_trigger]

archive = []
showing_digit_index=0
def init_ultrasonic(pin_trigger, pin_echo):
    RPI.setmode(RPI.BCM)
    RPI.setup(pin_echo, RPI.IN, pull_up_down=RPI.PUD_OFF)
    RPI.setup(gpio_pins_output, RPI.OUT, pull_up_down=RPI.PUD_OFF)

    RPI.output(pin_trigger, RPI.LOW)
    time.sleep(2)


def get_echo_time(pin_trigger, pin_echo):
    RPI.output(pin_trigger, RPI.HIGH)
    time.sleep(0.001)
    RPI.output(pin_trigger, RPI.LOW)

    while RPI.input(pin_echo) == 0:
        start_time = time.time()

    while RPI.input(pin_echo) == 1:
        end_time = time.time()

    t_echo = end_time - start_time
    return t_echo


def calibrate_ultrasonic(pin_trigger, pin_echo, threshold=0.1):
    measurements = []
    for _ in range(10):
        RPI.output(gpio_pin_output_buzzer, RPI.HIGH)
        measurements.append(get_echo_time(pin_trigger, pin_echo))
        RPI.output(gpio_pin_output_buzzer, RPI.LOW)
        time.sleep(0.5)


    mean_techo = np.mean(measurements)
    std_techo = np.std(measurements)

    if std_techo < threshold:
        alpha = 100 / mean_techo
        plt.plot(measurements, 'bo')
        plt.xlabel('Measurement number')
        plt.ylabel('Echo time')
        plt.title('Calibration Measurements')
        plt.show()
        return alpha
    else:
        print("Calibration failed: Standard deviation too high.")
        return -1

def up_button_pressed(channel):
    global alpha
    global showing_digit_index

    t_echo = get_echo_time(gpio_pin_input_pin_trigger, gpio_pin_input_pin_echo)
    distance = alpha * t_echo
    show_distance_7sd(t_echo,alpha,0x70)
    showing_digit_index = 0
    if not len(archive) == 100:
        archive.insert(0,t_echo)
    else:
        archive.pop(99)
        archive.insert(0,t_echo)

    print(archive,'archive')
    print(f"Distance: {distance:.2f} cm")

def show_distance_7sd(t_echo, alpha, address):
    my_7SD = SevenSegment.SevenSegment(address=address)
    my_7SD.begin()

    max_range = 400 # 4m - max range is mentioned in the slides of the lecture
    min_range = 2  # 2cm - min range is mentioned in the slides of the lecture

    current_distance = t_echo * alpha
    percentage = (current_distance / max_range)*100

    print(percentage)
    my_7SD.print_number_str(f"{percentage:.1f}")
    my_7SD.write_display()

def down_button_pressed(channel):
    global alpha
    alpha = calibrate_ultrasonic(gpio_pin_input_pin_trigger, gpio_pin_input_pin_echo)
    if alpha != -1:
        print(f"New calibration coefficient: {alpha:.2f}")

def right_button_pressed(channel):
    global showing_digit_index
    if showing_digit_index+1<len(archive):
        showing_digit_index += 1
        show_distance_7sd(archive[showing_digit_index],alpha,0x70)

def left_button_pressed(channel):
    global showing_digit_index
    if showing_digit_index-1>=0:
        showing_digit_index -= 1
        show_distance_7sd(archive[showing_digit_index],alpha,0x70)

init_ultrasonic(gpio_pin_input_pin_trigger, gpio_pin_input_pin_echo)
# Set up button event detection
RPI.setup(gpio_pins_input, RPI.IN, pull_up_down=RPI.PUD_OFF)

RPI.add_event_detect(gpio_pin_input_btn_up, RPI.FALLING, callback=up_button_pressed, bouncetime=200)
RPI.add_event_detect(gpio_pin_input_btn_down, RPI.FALLING, callback=down_button_pressed, bouncetime=200)
RPI.add_event_detect(gpio_pin_input_btn_right, RPI.FALLING, callback=right_button_pressed, bouncetime=200)
RPI.add_event_detect(gpio_pin_input_btn_left, RPI.FALLING, callback=left_button_pressed, bouncetime=200)


# forever loop
try:
    # Keep the program running to detect button presses
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Clean up GPIO settings before exiting
    RPI.cleanup()

