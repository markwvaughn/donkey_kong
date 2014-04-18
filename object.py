import pygame
import globals
import vector
import copy
import random

class Object(object):

	def __init__(self, pos, vel, acc, animation):
		self.pos = pos
		self.vel = vel
		self.acc = acc
		self.animation = animation

	def move(self):
		pass

	def update(self, dt):
		self.animation.update(dt)

	def draw(self, surface):
		self.animation.draw(surface, self.pos.x, self.pos.y)

class Platform(Object):

	def __init__(self, pos, vel, acc, animation):
		super(Platform, self).__init__(pos, vel, acc, animation)

	def move(self):
		super(Platform, self).move()

	def update(self, dt):
		super(Platform, self).update(dt)

	def draw(self, surface):
		super(Platform, self).draw(surface)


class OilDrum(Object):

	def __init__(self, pos, vel, acc, animation):
		super(OilDrum, self).__init__(pos, vel, acc, animation)

	def move(self):
		super(OilDrum, self).move()

	def update(self, dt):
		super(OilDrum, self).update(dt)

	def draw(self, surface):
		super(OilDrum, self).draw(surface)


class OilDrumFire(Object):

	def __init__(self, pos, vel, acc, animation):
		super(OilDrumFire, self).__init__(pos, vel, acc, animation)

	def move(self):
		super(OilDrumFire, self).move()

	def update(self, dt):
		super(OilDrumFire, self).update(dt)

	def draw(self, surface):
		super(OilDrumFire, self).draw(surface)


class RegularBarrel(Object):

	def __init__(self, pos, vel, acc, animation, a = 0):
		super(RegularBarrel, self).__init__(pos, vel, acc, animation)

		self.active = a

	def reset(self):
		self.active	= 0
		self.pos.x = 20
		self.pos.y = 200

	def wallCollision(self):
		w = self.animation._src.w 
		if self.pos.x + w > globals.WIDTH:
			self.pos.x = globals.WIDTH - w
			self.vel.x = -self.vel.x

		if self.pos.x < -15 and self.pos.y < globals.HEIGHT - 100:
			self.pos.x = -15
			self.vel.x = -self.vel.x

		if self.pos.y > globals.HEIGHT:
			self.reset()

	def applyGravity(self, dt):
		self.vel.y += (0.05 * dt)

	def move(self, dt):
		self.pos += self.vel * dt

	def objectCollision(self, objects):
	
		for obj in objects:

			for line in obj:

				v1 = vector.Vector(line[0])
				v2 = vector.Vector(line[1])
				v3 = copy.deepcopy(self.pos)
				v3.y = v3.y + self.animation._src.h
				v3.x = v3.x + self.animation._src.w / 2
				
				t1 = v2 - v1

				t2 = v3 - v1

				t = (vector.vecDot(t1,t2)) / (vector.vecDot(t1, t1))
				
				v = v1 + t1 * t
					
				distance = vector.vecDist(v3, v)
				
				left_obj = line[1][0]
				right_obj = line[0][0]

				if line[0][0] < line[1][0]:
					left_obj = line[0][0]
					right_obj = line[1][0]			

				if distance < 5 and v3.x >= left_obj and v3.x <= right_obj:
					self.pos.y = v.y - self.animation._src.h
					self.vel.y = 0
					self.acc.y = 0

	def applyForce(self, force, acc):
		self.vel = force
		self.acc = acc
		self.active = 1

	def update(self, dt):

		if self.active == 0:
			return

		self.move(dt)
		self.applyGravity(dt)
		self.wallCollision()
		self.animation.update(dt)

	def draw(self, surface):

		if self.active == 0:
			return

		super(RegularBarrel, self).draw(surface)


class BlueBarrel(RegularBarrel):
	def __init__(self, pos, vel, acc, animation, a = 0):
		super(BlueBarrel, self).__init__(pos, vel, acc, animation, a)

	def reset(self):
		super(BlueBarrel, self).reset()

	def wallCollision(self):
		super(BlueBarrel, self).wallCollision()

	def applyGravity(self, dt):
		super(BlueBarrel, self).applyGravity(dt)

	def move(self, dt):
		super(BlueBarrel, self).move(dt)

	def objectCollision(self, objects):
		super(BlueBarrel, self).objectCollision(objects)

	def applyForce(self, force, acc):
		super(BlueBarrel, self).applyForce(force, acc)

	def update(self, dt):
		super(BlueBarrel, self).update(dt)

	def draw(self, surface):
		super(BlueBarrel, self).draw(surface)


class BarrelList(object):

	def __init__(self):
		self.barrels = []
		self.insert_flag = 0
		self.clock_time = 0

	def activate(self):
		pass

	def update(self, timer, flag):

		self.clock_time += timer.dt2

		for barrel in self.barrels:
			barrel.update(timer.dt)
			
		self.remove()
		self.reset(flag)

	def checkCollisions(self, levelOne):
		for barrel in self.barrels:
			barrel.objectCollision(levelOne.lines)

	def remove(self):
		for barrel in self.barrels:
			if barrel.active == 0:
				del barrel	

	def reset(self, flag):
		if flag:
			del self.barrels[0:len(self.barrels)]
			self.clock_time = 0
			self.insert_flag = 0

	def draw(self, surface):
		for barrel in self.barrels:
			barrel.draw(surface)

class RegularBarrelList(BarrelList):

	def __init__(self):
		super(RegularBarrelList, self).__init__()

	def activate(self):
		
		if (self.clock_time / 1000) % 4 != 0:
			self.insert_flag = 0

		if (self.clock_time / 1000) % 4 == 0 and self.insert_flag == 0:
			self.insert_flag = 1
			self.barrels.append(RegularBarrel(vector.Vector((20,200)),vector.Vector((2.8,0)),vector.Vector((2.8,0)),globals.barrel_sideways_an, 1))
			
	def update(self, timer, flag):
		super(RegularBarrelList, self).update(timer, flag)

	def checkCollisions(self, levelOne):
		super(RegularBarrelList, self).checkCollisions(levelOne)

	def remove(self):
		super(RegularBarrelList, self).remove()

	def reset(self, flag):
		super(RegularBarrelList, self).reset(flag)

	def draw(self, surface):
		super(RegularBarrelList, self).draw(surface)

class BlueBarrelList(BarrelList):

	def __init__(self):
		super(BlueBarrelList, self).__init__()


	def activate(self):

		if (self.clock_time / 1000) % 4 != 0:
			self.insert_flag = 0

		if (self.clock_time / 1000) % 4 == 0 and self.insert_flag == 0:
			self.insert_flag = 1
			self.barrels.append(BlueBarrel(vector.Vector((20,200)),vector.Vector((2.8,0)),vector.Vector((2.8,0)),globals.bluebarrel_sideways_an, 1))
		
	def update(self, timer, flag):
		super(BlueBarrelList, self).update(timer, flag)

	def checkCollisions(self, levelOne):
		super(BlueBarrelList, self).checkCollisions(levelOne)

	def remove(self):
		super(BlueBarrelList, self).remove()

	def reset(self, flag):
		super(BlueBarrelList, self).reset(flag)

	def draw(self, surface):
		super(BlueBarrelList, self).draw(surface)


class FireBall(Object):

	def __init__(self, pos, vel, acc, animation):
		super(FireBall, self).__init__(pos, vel, acc, animation)

	def move(self):
		pass

	def update(self, dt):
		super(FireBall, self).update(dt)

	def draw(self, surface):
		super(FireBall, self).draw(surface)


class Hammer(Object):

	def __init__(self, pos, vel, acc, animation):
		super(Hammer, self).__init__(pos, vel, acc, animation)

		self.picked_up = False
		self.reset_pos = pos
		self.reset_vel = vel
		self.reset_acc = acc
		self.reset_animation = animation

	def reset(self):
		self.pos = self.reset_pos 
		self.vel = self.reset_vel
		self.acc = self.reset_acc
		self.animation = self.reset_animation 
		self.picked_up = False

	def update(self, dt):
		super(Hammer, self).update(dt)

	def draw(self, surface):
		if self.picked_up == False:
			super(Hammer, self).draw(surface)


class Pauline(Object):

	def __init__(self, pos, vel, acc, animation):
		super(Pauline, self).__init__(pos, vel, acc, animation)

	def move(self):
		pass

	def update(self, dt):
		super(Pauline, self).update(dt)

	def draw(self, surface):
		super(Pauline, self).draw(surface)


class DonkeyKong(Object):

	def __init__(self, pos, vel, acc, animation):
		super(DonkeyKong, self).__init__(pos, vel, acc, animation)

	def move(self):
		pass

	def update(self, dt):
		super(DonkeyKong, self).update(dt)

	def draw(self, surface):
		super(DonkeyKong, self).draw(surface)
