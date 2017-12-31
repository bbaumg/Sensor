import httplib, urllib
import time
import config


class thingspeak(object):
	key = config.thingspeak['key']
	temp = config.thingspeak['temp']
	humidity = config.thingspeak['humidity']
	pressure = config.thingspeak['pressure']
	picpu = config.thingspeak['picpu']

thingspeak = thingspeak()
print("Thingspeak Key = " + thingspeak.key)
print("Thingspeak Temp = " + thingspeak.temp)
print("Thingspeak Humidity = " + thingspeak.humidity)
print("Thingspeak PiCPU = " + thingspeak.picpu)
#Report Raspberry Pi internal temperature to Thingspeak Channel
def thermometer():
	while True:
		#Calculate CPU temperature of Raspberry Pi in Degrees C
		temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
		params = urllib.urlencode({
			thingspeak.temp:temp, 
			thingspeak.humidity:temp,
			thingspeak.picpu:temp,
			'key':thingspeak.key 
		}) 
		headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
		conn = httplib.HTTPConnection("api.thingspeak.com:80")
		try:
			conn.request("POST", "/update", params, headers)
			response = conn.getresponse()
			#data = response.read()
			print params, response.status, response.reason
			conn.close()
		except:
			print "connection failed"
		break


	


#sleep for desired amount of time
if __name__ == "__main__":
        while True:
                thermometer()
                time.sleep(15)
