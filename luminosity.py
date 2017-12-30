#Output test for TSL2561 Luminosity Sensor
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
#Manual Settings
ManDelay = 2 #Manual Exposure in Seconds
StartMan = 0x1F #Start Manual Exposure
EndMan = 0x1E #End Manual Exposure
#Number of sensor readings
vRepeat = 20
try:
	#Enter in [] the Exposure Setting to use 
	sequence = [HighLong]*vRepeat #repeat reading vRepeat times for setting in []
except:
	print("Unknown Exposure Setting used, defaulting to LowLong (x1 402ms")
	sequence = [LowLong]*vRepeat
	
# Get I2C bus
bus = smbus.SMBus(1)
writebyte = bus.write_byte_data
#Power On
writebyte(TSLaddr, 0x00 | TSLcmd, TSLon)
def luxcalc(Result0, Result1):
	"""Basic Lux Calculation value"""
	#see data sheet for lux calculation details
	#and to calculate lux correctly for all modes
	ResDiv = int(Result1)/int(Result0)
	#if ResDiv  0.52 and ResDiv  0.65 and ResDiv  0.8 and ResDiv  1.3:
		#lux = 0
	return lux
def manual(delay,mode):
	"""manual exposure"""
	bus.write_byte_data(TSLaddr, 0x01 | TSLcmd, mode) #sensativity mode
	bus.write_byte_data(TSLaddr, 0x01 | TSLcmd, StartMan) #start detection
	time.sleep(delay) #exposure
	bus.write_byte_data(TSLaddr, 0x01 | TSLcmd, EndMan) #stop detection
	return
def CurTime():
	"""Returns the current date and time"""
	t1 = time.asctime(time.localtime(time.time()))	
	return t1
print("Part Number", bus.read_byte_data(TSLaddr, 0x8A))
for item in sequence:
	if item != 3 and item != 19: #Selected built in delay for exposure. If Manual  mode not set (0x03 or 0x13)
		writebyte(TSLaddr, 0x01 | TSLcmd, item)
		#Give sensor time to write results before collecting reading. 
		#13.7ms  write several readings before sleep complete, 402ms would write once at 0.5sec sleep.
		time.sleep(0.5)
	else: #use manual exposure
		manual(ManDelay,item)
	#Read Ch0 Word
	data = bus.read_i2c_block_data(TSLaddr, chan0 | TSLcmd, 2)
	#Read CH1 Word
	data1 = bus.read_i2c_block_data(TSLaddr, chan1 | TSLcmd, 2)
	# Convert the data to Integer
	ch0 = data[1] * 256 + data[0]
	ch1 = data1[1] * 256 + data1[0]
	# Output data to screen
	#vTime = CurTime()
	if ch0 > 0:
		vLux = round(luxcalc(ch0, ch1),5)
		print(vTime," V+IR",ch0, " IR",ch1, "Lux",vLux)
	else:
		#either no light or clipping value exceeded due to too much light
		print(vTime, " V+IR",ch0, " IR",ch1, "No Light")
#Power Off
writebyte(TSLaddr, 0x00 | TSLcmd, TSLoff)
