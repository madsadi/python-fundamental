print('hello world')

import wiringpi as WiPi
from time import sleep

WiPi.wiringPiSetupGpio()

SwitchPins= [26,13,19,25]
WiPi.pinMode(17, 0)
for i in range(1,len(SwitchPins)):
    WiPi.pinMode(SwitchPins[i],0)
    WiPi.pullUpDnControl(SwitchPins[i],0)
    anybuttonpressed=0
    while not(anybuttonpressed):
        for i in range (1,len (SwitchPins)):
            if not WiPi.digitalRead(SwitchPins[i]):
                anybuttonpressed=1
                print("work done")



