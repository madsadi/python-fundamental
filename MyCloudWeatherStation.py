import dht11 #--> lib for accessing sensor data (temp and humidity)
import RPi.GPIO as RPI
from Adafruit_LED_Backpack import SevenSegment
import time
import thingspeak # -> import thingspeak

channel_id=2587702
write_key='4SEHIF5HHLB6XA35'
read_key='Y7DAZDZRGJRGYZKR'

my_channel = thingspeak.Channel(id=channel_id, api_key=write_key)
#----- hardware up -----#
RPI.setmode(RPI.BCM) # --> setting numbering system for GPIos

my_dht11 = dht11.DHT11(pin=4)  # --> creating an instance for DHT11 usage

my_7SD = SevenSegment.SevenSegment(address=0x70)
my_7SD.begin()

while True:
    temp_humidity_read = my_dht11.read()  # -> getting a single sensor measurement

    while not temp_humidity_read.is_valid():
        temp_humidity_read = my_dht11.read()  # -> getting a single sensor measurement

    print("Temperature:")
    print(temp_humidity_read.temperature)

    print("Humidity:")
    print(temp_humidity_read.humidity)

    my_7SD.print_number_str(str(temp_humidity_read.temperature))
    my_7SD.write_display()

    # transfer data to thingspeak cloud
    my_channel.update({'field1': temp_humidity_read.temperature, 'field2': temp_humidity_read.humidity})
    time.sleep(5)