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

class thingspeak(object):
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
