from Adafruit_LED_Backpack import SevenSegment


#----- Define a 7SD object -----#
segment_display = SevenSegment.SevenSegment(address=0x70)

#----- initialise 7SD object -------#
segment_display.begin()

year = '2024'

distance = 42.232
distance_string = str(int(round(distance,0)))

# ----- write data to 7SD ------


# segment_display.set_digit(0,'1')
# segment_display.set_digit(1,'2')
# segment_display.set_digit(2,'4')
# segment_display.set_digit(3,'6')

# or

for index in range(0,4):
    segment_display.set_digit(index,year[index])

# ----- update of 7SD ---------
segment_display.write_display()
