import logging
from Drivers.THINGSPEAK import thingspeak

channel_id = 79569
write_key  = 'PNJNNXVDAEP5FC74'
THINGSPEAK_CHANNEL		= 79569
THINGSPEAK_KEY			= 'PNJNNXVDAEP5FC74'


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



channel = thingspeak(channel=THINGSPEAK_CHANNEL, apiKey=THINGSPEAK_KEY)
#~ print(channel.fields)
#~ fields = channel.field
#~ channel.field['field1'] = 90
#~ channel.field['field2'] = 91
#~ print(channel.field)
channel.field[channel.field_name(name='Temp')] = 80
channel.field[channel.field_name(name='Humidity')] = 81
channel.field[channel.field_name(name='PiCPU')] = 82
#~ print(channel.field)
channel.post_update()
#~ print(channel.field)

#~ print(channel.field_name(name='Temp'))
#~ for key, value in fields.items():
	#~ print(str(key) + " = " + str(value))

#~ channel.get_last_field(field = channel.field_name(name='Temp'))

print("---- End of the program ----")






#update = channel.post_update()












