#from Adafruit_BME280 import *
from Adafruit_BME280.BME280 import *

sensor1 = BME280(
	t_mode=BME280_OSAMPLE_8, 
	p_mode=BME280_OSAMPLE_8, 
	h_mode=BME280_OSAMPLE_8,
	address=0x76
)
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
