#######################################################
# EVENT CLASS
#######################################################
class Event:
	def __init__(self):
		self._listeners = []

	def addListener(self, listener):
		if listener not in self._listeners:
			self._listeners.append(listener)

	def removeListener(self, listener):
		try:
			self._listeners.remove(listener)
		except ValueError:
			pass

	def notifyListener(self, modifier = None):
		for listener in self._listeners:
			if modifier != listener:
				listener.update(self)


#######################################################
# EVENT LISTENER CLASS
#######################################################
class EventListener:

	def __init__(self, state = None):
		self._state = state

	def update(self, event):
		print "State %s has been updated to %s" % (event._name, event._type)
		state = event._type

# class State(Event):

# 	def __init__(self, name = ""):
# 		Event.__init__(self)
# 		self._type = 0
# 		self._name = name


# 	def update(self, t):
# 		self._type = t
# 		self.notifyListener()
