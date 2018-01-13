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
#from Drivers.TSL2561 import TSL2561
import Drivers.TSL2561 as TSL2561
#from Drivers.THINGSPEAK import thingspeak
import Drivers.THINGSPEAK as thingspeak
#from Adafruit_BME280.BME280 import BME280
import Adafruit_BME280.BME280 as BME280
#from Adafruit_LED_Backpack import SevenSegment
import Adafruit_LED_Backpack.SevenSegment as SevenSegment
import Adafruit_SSD1306.SSD1306 as SSD1306
#~ from PIL import Image
#~ from PIL import ImageDraw
#~ from PIL import ImageFont
import Image
import ImageDraw
import ImageFont

import config

# Setup logging
#logLevel = logging.CRITICAL
#logLevel = logging.ERROR
#logLevel = logging.WARNING
logLevel = logging.INFO
#logLevel = logging.DEBUG
#cstlogFile = '/var/controller/main.log'
logging.basicConfig(
  level=logLevel, 
  format='%(levelname)s:%(name)s:%(funcName)s - %(message)s', 
  datefmt = '%Y-%m-%d %H:%M:%S',
  #filename = cstlogFile)
  )
logger = logging.getLogger(__name__)

print(config.settings['SEVEN_ADDRESS'])

# Define all of the variables and device addresses
SEVEN_ADDRESS			= 0x70   					# 7 Stegment address
SEVEN_BRIGHT			= 15						# Default Brightness (0-15)
BME280_ADDRESS			= 0x76						# BME280 address
THINGSPEAK_CHANNEL		= 79569						# Channel ID #
THINGSPEAK_KEY			= 'PNJNNXVDAEP5FC74'		# write API Key
THINGSPEAD_FREQ			= 5							# how often in "min"
OLED_ADDRESS			= 0x3C						# OLED disp address
OLED_FONT				= 'VCR_OSD_MONO_1.001.ttf'
OLED_FONT_SIZE			= 72

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END SETUP - BEGIN FUNCTIONS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def update_clock(now):
	logger.info("Time: " + str(now))
	hour = now.hour
	minute = now.minute
	segment.clear()
	if hour > 12:
		hour = hour - 12
	if int(hour / 10) != 0:
		segment.set_digit(0, int(hour / 10)) 	# Tens
	segment.set_digit(1, hour % 10)          	# Ones
	segment.set_digit(2, int(minute / 10))   	# Tens
	segment.set_digit(3, minute % 10)        	# Ones
	segment.set_colon(1)
	try:
		segment.write_display()
	except Exception as e:
		logger.exception("Error writing to the segment display")

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END FUNCTIONS - BEGIN PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
logger.critical("**************************************************")
logger.critical("*")
logger.critical("* Starting Program")
logger.critical("*")
logger.critical("**************************************************")
logger.critical("Log Level = " + str(logLevel))
if config.functions.display_clock == True:
	logger.info("Setting up the 7 segment display")
	segment = SevenSegment.SevenSegment(address=SEVEN_ADDRESS)
	segment.begin()
	segment.set_brightness(SEVEN_BRIGHT)

	logger.info("Quick test to make sure the display works")
	testDispSetup = (
		0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
		0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20,
		0x3f, 0x00, 0x00, 0x3f, 0x00, 0x00, 0x3f, 0x00, 0x00, 0x3f)
	for y in range(len(testDispSetup)):
		try:
			for ii in range(0,4,1):
				segment.set_digit_raw(ii, testDispSetup[y])
			segment.write_display()
		except:
			logger.exception("An error happened to the display " + str(sys.exc_info()[0]))
		time.sleep(.04)

if config.functions.display_temp == True:
	logger.info("Setting up the OLED display")
	disp = SSD1306.SSD1306_128_64(rst=None, i2c_address=OLED_ADDRESS)
	disp.begin()
	disp.clear()
	disp.display()
	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))
	draw = ImageDraw.Draw(image)
	padding = 0
	top = padding
	bottom = height-padding
	x = 0
	font = ImageFont.truetype(OLED_FONT, OLED_FONT_SIZE)

logger.info("Setting up the BME sensor")
sensor = BME280.BME280(address=BME280_ADDRESS)

logger.info("Setting up the thingspeak channel")
channel = thingspeak.thingspeak(channel=THINGSPEAK_CHANNEL, apiKey=THINGSPEAK_KEY)

logger.info("**************************************************")
logger.info("Beginning the Loop")
while True:
	# Upate the clock display
	now = datetime.datetime.now()
	minute = now.minute
	second = now.second
	if config.functions.display_clock == True:
		update_clock(datetime.datetime.now())
	
	# Get the sensor Information
	degrees_c = sensor.read_temperature()
	degrees_f = int(round((degrees_c*9/5)+32, 0))
	pascals = sensor.read_pressure()
	hectopascals = int(round(pascals / 100, 0))
	humidity = int(round(sensor.read_humidity(), 0))
	
	# Update the temp display
	if config.functions.display_temp == True:
		draw.rectangle((0,0,width,height), outline=0, fill=0)
		draw.text((x, top), str(degrees_f),  font=font, fill=255)
		disp.image(image)
		disp.display()
	
	# Publish the data to Thingspeak
	if (minute % 5) == 0:
		channel.field[channel.field_name(name='Temp')] = degrees_f
		channel.field[channel.field_name(name='Humidity')] = humidity
		channel.field[channel.field_name(name='Pressure')] = hectopascals
		channel.post_update()
	# Sleep until the next minute
	now = datetime.datetime.now()
	if config.functions.display_clock == True or config.functions.display_temp == True:
		sleep = 60 - now.second
	else:
		sleep = 300 - now.second
	logger.info("Sleeping: " + str(sleep) + " seconds")
	time.sleep(sleep)



