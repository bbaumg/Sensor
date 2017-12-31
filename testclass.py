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
