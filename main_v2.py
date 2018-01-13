#!/usr/bin/python

import sys
import time
import datetime
import logging
import httplib
import urllib
from Adafruit_LED_Backpack import SevenSegment

# Setup logging
#logLevel = logging.CRITICAL
#logLevel = logging.ERROR
#logLevel = logging.WARNING
logLevel = logging.INFO
#logLevel = logging.DEBUG
cstlogFile = '/var/log/main.log'

logging.basicConfig(
  level=logLevel, 
  #format='%(asctime)s - %(levelno)s - %(funcName)s - %(message)s', 
  format='%(funcName)s - %(message)s', 
  datefmt = '%Y-%m-%d %H:%M:%S',
  #filename = cstlogFile)
  )
logger = logging.getLogger(__name__)

# Define all of the variables & dictionary arrays
varAddress = 0x70   # Display address
thingKey = 'MR9C3L1EU7JAT6FB'

# Initialize the display
segment = SevenSegment.SevenSegment(address=varAddress)
segment.begin()
segment.set_brightness(8)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END SETUP - BEGIN FUNCTIONS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def outDispSetup():
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
        logger.exception("An unknown error happened" + str(sys.exc_info()[0]))
    time.sleep(.04)

def getSensor():
  #Calculate CPU temperature of Raspberry Pi in Degrees C
  tempC = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
  logger.info("Temp C = " + str(tempC))
  temp = (tempC * 1.8) + 32
  logger.info("Temp F = " + str(temp))
  params = urllib.urlencode({'PiCPU': temp, 'Temp':temp, 'key':thingKey }) 
  logger.info("POST Paramaters: " + str(params.replace("&"," ")))
  headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
  conn = httplib.HTTPConnection("api.thingspeak.com:80")
  try:
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    logger.info("Response: " + str(response.status) + " " + str(response.reason))
    #print temp
    #print response.status, response.reason
    data = response.read()
    conn.close()
  except:
    logger.exception("An unknown error happened" + str(sys.exc_info()[0]))


def outTime():
  now = datetime.datetime.now()
  logger.info("Time: " + str(now))
  hour = now.hour
  minute = now.minute
  segment.clear()
  # Set hours
  if hour > 12:
    hour = hour - 12
  if int(hour / 10) <> 0:
    segment.set_digit(0, int(hour / 10))   # Tens
  segment.set_digit(1, hour % 10)          # Ones
  # Set minutes
  segment.set_digit(2, int(minute / 10))   # Tens
  segment.set_digit(3, minute % 10)        # Ones
  # Set colon on
  segment.set_colon(1)

  # Write display and sleep
  try:
    segment.write_display()
  except:
    logger.exception("An unknown error happened" + str(sys.exc_info()[0]))



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END FUNCTIONS - BEGIN PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

logger.critical("**************************************************")
logger.critical("*")
logger.critical("* Starting Program")
logger.critical("*")
logger.critical("**************************************************")
logger.critical("Log Level = " + str(logLevel))
outDispSetup()
print "Press CTRL+Z to exit"

while(True):
	now = datetime.datetime.now()
	minute = now.minute
	second = now.second
	outTime()
	if (minute % 5) == 0:
		getSensor()
	sleep = 60 - second
	logger.info("Sleeping: " + str(sleep) + " seconds")
	time.sleep(sleep)


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

