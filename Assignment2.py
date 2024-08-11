import RPi.GPIO as RPI
from Adafruit_LED_Backpack import SevenSegment
import time
import thingspeak # -> import thingspeak
import json
import matplotlib.pyplot as plt
import numpy as np

channel_id=343018
channel = thingspeak.Channel(id=channel_id)

RPI.setmode(RPI.BCM) # --> setting numbering system for GPIOs

def get_each_field():
    all_data = json.loads(channel.get())
    fields={}
    for j in range(1,8):
        field_data=[]
        for item in all_data['feeds']:
            field_data.append(int(item[f'field{j}']))

        fields[f'field{j}'] = field_data

    return fields

def plot(fields,title,color):
    mean = np.mean(fields)
    plt.plot(fields,color=color)
    plt.xlabel('sample')
    plt.ylabel('ATM')
    plt.axhline(y=mean, color=color, linestyle='--')
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

# print(get_each_field())
