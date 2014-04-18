import pygame

class Animation:

	def __init__(self, sprite, begin, end, step, dir, speed = 1):
		self._sprite = sprite
		self._begin = begin
		self._step = step
		self._end = end
		self._dir = dir

		self._time = pygame.time.get_ticks()
		self._speed = speed
	
		src_rect = sprite.get_rect()
		self._src = pygame.Rect(begin,0,step,src_rect.h)		

	def update(self, dt):

		if self._speed == 0: 
			self.reset()
			return

		self._time += self._speed * dt

		if self._time > 50.0:
	
			if self._src.x + self._step == self._end:
				self._src.x = self._begin - self._step

			self._src.x += self._step

			self._time = 0.0
		
	def reset(self):
		if self._dir == 1:
			self._src.x = self._begin
			self._src.top = 0
		
		else:
			self._src.x = self._end - self._step
			self._src.top = 0

		self._time = 0.0

	def draw(self, surface, x, y):
		dest = pygame.Rect(x, y, self._step, self._src.h)
		surface.blit(self._sprite, dest, self._src)