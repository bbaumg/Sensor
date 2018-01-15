settings = dict(
	SEVEN_ADDRESS			= 0x70,   					# 7 Stegment address
	SEVEN_BRIGHT			= 15,						# Default Brightness (0-15)
	BME280_ADDRESS			= 0x76,						# BME280 address
	THINGSPEAK_CHANNEL		= 79569,						# Channel ID #
	THINGSPEAK_KEY			= 'PNJNNXVDAEP5FC74',		# write API Key
	THINGSPEAD_FREQ			= 5,							# how often in "min"
	OLED_ADDRESS			= 0x3C,						# OLED disp address
	OLED_FONT				= 'VCR_OSD_MONO_1.001.ttf',
	OLED_FONT_SIZE			= 72
)

class functions(object):
	display_clock = True
	display_temp = True


thingspeak = dict(
    key = 'PNJNNXVDAEP5FC74',
    temp = 'field3',
    humidity = 'field4',
	pressure = 'field6',
    picpu = 'field5',
)

class someclass(object):
	x=1
	y=2
	z=3
	def __init__(self):
		self.current_idx = 0
		self.items = ["x","y","z"]
	def next(self):
		if self.current_idx < len(self.items):
			self.current_idx += 1
			k = self.items[self.current_idx-1]
			return (k,getattr(self,k))
		else:
			raise StopIteration
	def __iter__(self):
		return self

class thingspeakA(object):
	key = 'PNJNNXVDAEP5FC74'
	temp = 'field3'
	humidity = 'field4'
	pressure = 'field6'
	picpu = 'field5'
	
	def __init__(self):
		self.current_idx = 0
		self.items = ["key","temp","humidity","pressure","picpu"]
	def next(self):
		if self.current_idx < len(self.items):
			self.current_idx += 1
			k = self.items[self.current_idx-1]
			return (k,getattr(self,k))
		else:
			raise StopIteration
	def __iter__(self):
		return self
