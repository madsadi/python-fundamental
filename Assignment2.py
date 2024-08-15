import RPi.GPIO as RPI
from Adafruit_LED_Backpack import SevenSegment
import time
import dht11 #--> lib for accessing sensor data (temp and humidity)
import thingspeak # -> import thingspeak
import json
import matplotlib.pyplot as plt
import numpy as np
from luma.led_matrix.device import max7219 # <-- MAX7219 device
from luma.core.interface.serial import spi, noop # <-- SPI interface
from luma.core.render import canvas # <-- Canvas for drawing

channel_id=343018
channel = thingspeak.Channel(id=channel_id)

my_channel_id=2624254
write_api_key = 'WDPU0U3DEW5GBPC2'
read_api_key = 'Q76IR3KHD2RV4Q2A'
my_channel = thingspeak.Channel(id=my_channel_id, api_key=write_api_key)

# Pin setup
left_button_pin = 25
right_button_pin = 19
button_pressed = 0

current_measurement_index = 0
measurement_list=[{'title':'PM1','field':'field5'}, {'title':'PM2.5','field':'field3'}, {'title':'PM10','field':'field1'},
                  {'title':'Temperature','field':'field6'}, {'title':'Humidity','field':'field7'}]
spi_connection = spi(port=0, device=1, gpio=noop())  # <- setup of SPI
led_driver = max7219(spi_connection, cascaded=1, block_orientation=90, rotate=0)  # <- Max7219
my_dht11 = dht11.DHT11(pin=4)  # --> creating an instance for DHT11 usage

def get_each_field():
    all_data = json.loads(channel.get())
    fields={}
    for j in range(1,8):
        field_data=[]
        for item in all_data['feeds']:
            field_data.append(int(item[f'field{j}']))

        fields[f'field{j}'] = field_data

    return fields

def plot(fields,title,color,linestyle='--'):
    mean = np.mean(fields)
    plt.plot(fields,color=color)
    plt.xlabel('sample')
    plt.ylabel('ATM')
    plt.axhline(y=mean, color=color, linestyle=linestyle)
    plt.title(title)
    plt.show()

field_data=get_each_field()
fields_name={
    'field1':{
        'title':'PM10',
        'color':'blue',
    },
    'field2':{
        'title':'PM10 avg60',
    },
    'field3':{
        'title':'PM2.5',
        'color':'black',
    },
    'field4':{
        'title':'PM2.5 avg60',
    },
    'field5':{
        'title':'PM1',
        'color':'red',
    },
    'field6':{
        'title':'PM1 avg60',
    },
    'field7':{
        'title':'Air Quality Index (AQI)',
    }
}

for i in [1,3,5]:
    title,color = fields_name[f'field{i}']['title'], fields_name[f'field{i}']['color']
    plot(field_data[f'field{i}'],title,color)

def fahrenheit_to_celcius(fahrenheit):
    celcius = (fahrenheit - 32) * 5 / 9
    return celcius

temp = []
for item in field_data['field6']:
    temp.append(fahrenheit_to_celcius(item))

humidity = field_data['field7']

print("Humidity:", humidity)
print("Temperature C:", temp)


def update_buffer(new_measurement):
    temp_value,humidity_value = new_measurement.temperature, new_measurement.humidity
    def buffer_control(buffer,value):
        if not len(buffer) == 100:
            buffer.insert(0,value)
        else:
            buffer.pop(99)
            buffer.insert(0,value)

    buffer_control(temp,temp_value)
    buffer_control(humidity,humidity_value)

def calculate_AQI(measurement,value):
    AQI = 0
    categories=[
            {
                'title':'GOOD',
                'min_PM2.5':0,
                'max_PM2.5':12,
                'min_PM10': 0,
                'max_PM10': 54,
                'min_index':0,
                'max_index':50,
            },
            {
                'title': 'MODERATE',
                'min_PM2.5': 12.1,
                'max_PM2.5': 35.4,
                'min_PM10': 55,
                'max_PM10': 154,
                'min_index': 51,
                'max_index': 100,
            },
            {
                'title': 'UNHEALTHY FOR SENSITIVE GROUPS',
                'min_PM2.5': 35.5,
                'max_PM2.5': 55.4,
                'min_PM10': 155,
                'max_PM10': 254,
                'min_index': 101,
                'max_index': 150,
            },
            {
                'title': 'UNHEALTHY',
                'min_PM2.5': 55.5,
                'max_PM2.5': 150.4,
                'min_PM10': 255,
                'max_PM10': 354,
                'min_index': 151,
                'max_index': 200,
            },
            {
                'title': 'VERY UNHEALTHY',
                'min_PM2.5': 150.5,
                'max_PM2.5': 250.4,
                'min_PM10': 355,
                'max_PM10': 424,
                'min_index': 201,
                'max_index': 300,
            },
            {
                'title': 'HAZARDOUS',
                'min_PM2.5': 250.5,
                'max_PM2.5': 350.4,
                'min_PM10': 425,
                'max_PM10': 504,
                'min_index': 301,
                'max_index': 400,
            },
            {
                'title': 'HAZARDOUS',
                'min_PM2.5': 350.5,
                'max_PM2.5': 500.4,
                'min_PM10': 505,
                'max_PM10': 604,
                'min_index': 401,
                'max_index': 500,
            },
        ]
    if measurement=='PM2.5':
        for category in categories:
            if value>=category['min_PM2.5'] and value<=category['max_PM2.5']:
                AQI=(((category['max_index']-category['min_index'])/(category['max_PM2.5']-category['min_PM2.5']))*(value-category['min_PM2.5'])) + category['min_index']
    elif measurement=='PM10':
        for category in categories:
            if value>=category['min_PM10'] and value<=category['max_PM10']:
                AQI=(((category['max_index']-category['min_index'])/(category['max_PM10']-category['min_PM10']))*(value-category['min_PM10'])) + category['min_index']
    return AQI

def AQI():
    fields = get_each_field()
    ten_AQI = []
    for value in fields['field1']:
        ten_AQI.append(calculate_AQI('PM10', value))

    two_point_five_AQI = []
    for value in fields['field3']:
        two_point_five_AQI.append(calculate_AQI('PM2.5', value))

    max_AQI = np.amax(np.array([ten_AQI, two_point_five_AQI]), axis=0)
    for value in max_AQI:
        my_channel.update({'field3': value})
        time.sleep(15) # wait for 15 second because of thingspeak limitation of updating data
    for value in two_point_five_AQI:
        my_channel.update({'field1': value})
        time.sleep(15) # wait for 15 second because of thingspeak limitation of updating data
    for value in ten_AQI:
        my_channel.update({'field2': value})
        time.sleep(15) # wait for 15 second because of thingspeak limitation of updating data

def init():
    RPI.setmode(RPI.BCM) # --> setting numbering system for GPIOs
    RPI.setup(left_button_pin, RPI.IN, pull_up_down=RPI.PUD_UP)
    RPI.setup(right_button_pin, RPI.IN, pull_up_down=RPI.PUD_UP)
    with canvas(led_driver) as draw:
            draw.point([0, 0], fill="white")
    visualise_graphically()



def display_mean_value():
    data = get_each_field()
    mean_value = np.mean(data[measurement_list[current_measurement_index]['field']])
    my_7SD = SevenSegment.SevenSegment(address=0x70)
    my_7SD.begin()
    my_7SD.print_number_str(str(mean_value))
    my_7SD.write_display()

def visualise_graphically():
    data = get_each_field()
    list = data[measurement_list[current_measurement_index]['field']]
    chunk_size=13
    split_arr = [list[i:i + chunk_size] for i in range(0, len(list), chunk_size)]

    mean_list = []
    for chunk in split_arr:
        mean_value = np.mean(chunk)
        mean_list.append(mean_value)

    max_mean=max(mean_list)
    min_mean=min(mean_list)
    index=0

    with canvas(led_driver) as draw:
        for mean in mean_list:
            if mean>0:
                draw.point([index, (5-(mean-min_mean)/(max_mean-min_mean)*5)+2], fill="white")
            else:
                draw.point([index, 7], fill="white")
            index+=1
            draw.point([current_measurement_index, 0], fill="white")


def select_measurement(btn):
    global current_measurement_index
    if btn==1:
        with canvas(led_driver) as draw:
            if current_measurement_index > 0:
                current_measurement_index -= 1
                draw.point([current_measurement_index, 0], fill="white")
            else:
                current_measurement_index = len(measurement_list) - 1
                draw.point([len(measurement_list) - 1, 0], fill="white")
        display_mean_value()
        visualise_graphically()
    elif btn==2:
        with canvas(led_driver) as draw:
            if current_measurement_index + 1 < len(measurement_list):
                current_measurement_index += 1
                draw.point([current_measurement_index, 0], fill="white")
            else:
                current_measurement_index = 0
                draw.point([0, 0], fill="white")
        display_mean_value()
        visualise_graphically()

AQI()
init()

while True:
    temp_humidity_read = my_dht11.read()  # -> getting a single sensor measurement

    while not temp_humidity_read.is_valid():
        temp_humidity_read = my_dht11.read()  # -> getting a single sensor measurement

    if not RPI.input(left_button_pin):
        button_pressed = 1
    elif not RPI.input(right_button_pin):
        button_pressed = 2
    else:
        button_pressed = 0

    select_measurement(button_pressed)
    time.sleep(0.1)

    update_buffer(temp_humidity_read)
    plot(temp,'Temperature (C)','green','dotted')
    plot(humidity,'Humidity','navy','dotted')

