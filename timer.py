#########################################################################################
# timer
#########################################################################################
class Timer():

	def __init__(self, t):
		self.time = t
		self.dt = 0
		self.dt2 = 0

	def update(self, time):
		self.dt2 = time - self.time
		self.dt = 0.75
		self.time = time

