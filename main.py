# Author: Barrett Baumgartner
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import logging
import datetime
import time
import config
from Drivers.TSL2561 import TSL2561
from Adafruit_BME280.BME280 import *
from Adafruit_LED_Backpack import SevenSegment






thingspeak=config.thingspeak()
print thingspeak.key
thingspeak.key = ['234523452345',0]
print thingspeak.key
for k,v in thingspeak:
	print k,"=",v
	
s=config.someclass()
for k,v in s:
	print k,"=",v






class something(object):
	def __init__(self, somethingelse):
		self.somethingelse = somethingelse

if __name__ == "__main__":
	while True:
		#print config.thingspeak['key']
		sensor = BME280(address=0x76)
		degrees = sensor.read_temperature()
		pascals = sensor.read_pressure()
		hectopascals = pascals / 100
		humidity = sensor.read_humidity()
		dewpoint = sensor.read_dewpoint_f()
		print 'Temp      = {0:0.3f} deg C'.format(degrees)
		print 'Temp      = {0:0.3f} deg F'.format((degrees*9/5)+32)
		print 'Pressure  = {0:0.2f} hPa'.format(hectopascals)
		print 'Humidity  = {0:0.2f} %'.format(humidity)
		print 'Dewpoint  = {0:0.2f} deg F'.format(dewpoint)
		
		chip = TSL2561()
		print(chip.read_channel0())
		print(chip.read_channel1())
		print(chip.calculate_lux(chip.read_channel0()))
		print(chip.get_visible_lux())
		print(chip.get_full_lux())
		print(chip.get_ir_lux())
		time.sleep(1)




