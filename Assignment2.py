import RPi.GPIO as RPI
from Adafruit_LED_Backpack import SevenSegment
import time
import dht11 #--> lib for accessing sensor data (temp and humidity)
import thingspeak # -> import thingspeak
import json
import matplotlib.pyplot as plt
import numpy as np

channel_id=343018
channel = thingspeak.Channel(id=channel_id)

RPI.setmode(RPI.BCM) # --> setting numbering system for GPIOs
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

while True:
    temp_humidity_read = my_dht11.read()  # -> getting a single sensor measurement

    while not temp_humidity_read.is_valid():
        temp_humidity_read = my_dht11.read()  # -> getting a single sensor measurement

    update_buffer(temp_humidity_read)
    plot(temp,'Temperature (C)','green','dotted')
    plot(humidity,'Humidity','navy','dotted')

