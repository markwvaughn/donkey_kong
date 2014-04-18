#########################################################################################
# vector 
#########################################################################################
class Vector():

	def __init__(self, tuple):
		self.x = tuple[0]
		self.y = tuple[1]

	def rot(self, t):
		t = (pi * t / 180.0)
		
		self.x, self.y = self.x * cos(t) - self.y * sin(t), \
						 self.x * sin(t) + self.y * cos(t)

	def __div__(self, i):
		return Vector((self.x / i, self.y / i))

	def __mul__(self, i):
		return Vector((self.x * i, self.y * i))

	def __add__(self, b):
		return Vector((self.x + b.x, self.y + b.y))

	def __sub__(self, b):
		return Vector((self.x - b.x, self.y - b.y))

	def len(self):
		return (self.x**2 + self.y**2)**0.5

	def unit(self):
		return self / (self.x**2 + self.y**2)**0.5

	def __repr__(self):
		return "(%s,%s)" % (self.x, self.y)
	
def vecDot(a, b):
	return a.x*b.x + a.y*b.y

def vecDist(a, b):
	return ((a.x-b.x)**2 + (a.y-b.y)**2)**0.5

