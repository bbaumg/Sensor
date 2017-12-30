#Output delay check test for TSL2561 Luminosity Sensor
#RaspberryConnect.com
import smbus
import time
TSLaddr = 0x39 #Default I2C address, alternate 0x29, 0x49 
TSLcmd = 0x80 #Command
chan0 = 0x0C #Read Channel0 sensor date
chan1 = 0x0E #Read channel1 sensor data
TSLon = 0x03 #Switch sensors on
TSLoff = 0x00 #Switch sensors off
#Exposure settings
LowShort = 0x00 #x1 Gain 13.7 miliseconds
LowMed = 0x01 #x1 Gain 101 miliseconds
LowLong = 0x02 #x1 Gain 402 miliseconds
LowManual = 0x03 #x1 Gain Manual
HighShort = 0x10 #LowLight x16 Gain 13.7 miliseconds
HighMed = 0x11	#LowLight x16 Gain 100 miliseconds
HighLong = 0x12 #LowLight x16 Gain 402 miliseconds
HighManual = 0x13 #LowLight x16 Gain Manual
# Get I2C bus
bus = smbus.SMBus(1)
writebyte = bus.write_byte_data
def lightcheck():
	#Read Ch0 Word
	data = bus.read_i2c_block_data(TSLaddr, chan0 | TSLcmd, 2)
	print("data = " + str(data))
	#Read CH1 Word
	data1 = bus.read_i2c_block_data(TSLaddr, chan1 | TSLcmd, 2)
	print("data1 = " + str(data1))
	# Convert the data to Integer
	ch0 = data[1] * 256 + data[0]
	print("ch0 = " + str(ch0))
	ch1 = data1[1] * 256 + data1[0]
	print("ch1 = " + str(ch1))
	vResults = ch0-ch1 #get visable light results
	print("Reading = ",vResults)
	if vResults > 200: #check against reading threshold 
		print("Light Level Detected")
		#do something else
		time.sleep(5)
	else:
		print("I will check again soon")
		writebyte(TSLaddr, 0x00 | TSLcmd, TSLoff) #switch off
		time.sleep(1) #delay before next check in seconds
		writebyte(TSLaddr, 0x00 | TSLcmd, TSLon) #switch on
		time.sleep(1) #time for sensor to settle
if __name__ == "__main__":
	writebyte(TSLaddr, 0x00 | TSLcmd, TSLon) #Power On
	#Gain x1 at 402ms is the default so this line not required 
	#but change for different sensitivity
	writebyte(TSLaddr, 0x01 | TSLcmd,LowLong) #Gain x1 402ms
	time.sleep(1) #give time sensor to settle
	print("check Starting")
	while 1:
		lightcheck()
	writebyte(TSLaddr, 0x00 | TSLcmd, TSLoff) #Power Off