import pygame
import globals
from vector import *
import copy

class Mario():

	def __init__(self, pos, vel, state, anim):
		self.pos = pos
		self.vel = vel
		self.acc = Vector((0, 0))
		self.animationstate = state
		self.animation = anim
		self.jumptime = 0
		self.actionstate = "on_ground"
		
		self.hammer_time = 0

		self.ground = globals.HEIGHT - 20
		self.current_ground = None


	def move(self, dt):
		self.pos += (self.vel * dt)
		
	def jump(self, time):
		if self.actionstate == "on_ground":
			self.actionstate = "jumping"
			self.jumptime = 0

	def applyJump(self,dt):
		
		if self.actionstate != "jumping":
			return

		# FREE FALL BASICALLY
		self.ground = globals.HEIGHT - 20

		self.jumptime += dt
		
		if self.jumptime < 10:
			
			self.acc.x += self.vel.x * dt * 0.005
			
			self.acc.y -= dt * 2.5 * 0.1
			
			self.vel = self.acc * 2.5 * dt

		if self.jumptime > 10:
			self.actionstate = "falling"
	
	def climb(self, objects, arrow_pressed):

		if self.actionstate == "jumping":
			return

		if self.actionstate == "falling":
			return

		if self.animation == globals.mario_with_hammer_left_an or \
		   self.animation == globals.mario_with_hammer_right_an:
		   return

		for obj in objects:

			obj_x = obj[0][0]
			
			top_objy = obj[1][1]
			bot_objy = obj[0][1]

			if obj[0][1] < obj[1][1]:
				top_objy = obj[0][1]
				bot_objy = obj[1][1]	

			y = self.pos.y
			yh = self.pos.y + self.animation._src.h

			x = self.pos.x + self.animation._src.w / 4
			xw = self.pos.x + 3 * self.animation._src.w / 4

			# bottom of ladder
			if x < obj_x and xw > obj_x and y < bot_objy and yh > bot_objy:
				if arrow_pressed == "up":
					self.actionstate = "on_ladder"
					self.animationstate = "climb_up"
				elif arrow_pressed == "down":
					self.actionstate = "off_ladder"
					self.animationstate = "face_back"

			# top of ladder
			if x < obj_x and xw > obj_x and y < top_objy and yh > top_objy:
				if arrow_pressed == "down":
					self.actionstate = "on_ladder"
					self.animationstate = "climb_down"
				elif arrow_pressed == "up":
					self.actionstate = "off_ladder"
					self.animationstate = "face_back"

			if self.actionstate == "on_ladder" and arrow_pressed == "down":
				self.animationstate = "climb_down"

			if self.actionstate == "on_ladder" and arrow_pressed == "up":
				self.animationstate = "climb_up"

	def reachPaulineWin(self, pauline):
		x = self.pos.x
		y = self.pos.y
		w = self.animation._src.w
		h = self.animation._src.h
		
		hx = pauline.pos.x
		hy = pauline.pos.y
		hw = pauline.animation._src.w
		hh = pauline.animation._src.h

		if x + w > hx and x < hx + hw and y + h > hy and y < hy + hh and (y + h <= globals.HEIGHT-450):
			return True

		return False

	def hammerCollision(self, hammer):
		x = self.pos.x
		y = self.pos.y
		w = self.animation._src.w
		h = self.animation._src.h
		
		hx = hammer.pos.x
		hy = hammer.pos.y
		hw = hammer.animation._src.w
		hh = hammer.animation._src.h

		if x + w > hx and x < hx + hw and y + h > hy and y < hy + hh and hammer.picked_up == False:
			hammer.picked_up = True
			if self.animationstate == "walk_left" or self.animationstate == "face_left" or self.animationstate == "face_back":
				self.animation = globals.mario_with_hammer_left_an
			elif self.animationstate == "walk_right" or self.animationstate == "face_right":
				self.animation = globals.mario_with_hammer_right_an


	def barrelCollision(self, barrels):
		
		x = self.pos.x
		y = self.pos.y
		w = self.animation._src.w
		h = self.animation._src.h
		
		cx = x + w / 2.0
		cy = y + h / 2.0

		did_die = 0

		for barrel in barrels:
			
			if barrel.active == 1:

				bx = barrel.pos.x
				by = barrel.pos.y
				bw = barrel.animation._src.w
				bh = barrel.animation._src.h

				bcx = bx + bw / 2.0
				bcy = by + bh / 2.0
				 
				xdist = abs(cx - bcx)
				ydist = abs(cy - bcy)

				if xdist < 10 and bcy - cy > 30 and bcy - cy < 50 and (self.actionstate == "jumping" or self.actionstate == "falling"):
					
					print bcy - cy

					globals.score += 100
					barrel.reset()
					return 0

				if xdist < (w/3.0 + bw/3.0) and ydist < (h/3.0 + bh/3.0):

					if self.animation == globals.mario_with_hammer_left_an or \
					   self.animation == globals.mario_with_hammer_right_an:
					   	globals.score += 100
						barrel.reset()
						return 0

					self.die()
					did_die = 1
		
		return did_die

	def die(self):
		self.pos.x = 100
		self.pos.y = globals.HEIGHT-60
		globals.mario_num_lives -= 1
		self.vel = Vector((0, 0))
		self.acc = Vector((0, 0))
		self.animationstate = "face_right"
		self.animation = globals.mario_walking_right_an
		self.jumptime = 0
		self.actionstate = "on_ground"
		
		self.ground = globals.HEIGHT - 20
		self.current_ground = None

	def reset(self):
		self.pos.x = 100
		self.pos.y = globals.HEIGHT-60
		globals.mario_num_lives = 3
		self.vel = Vector((0, 0))
		self.acc = Vector((0, 0))
		self.animationstate = "face_right"
		self.animation = globals.mario_walking_right_an
		self.jumptime = 0
		self.actionstate = "on_ground"
		self.hammer_time = 0

		self.ground = globals.HEIGHT - 20
		self.current_ground = None


	def checkTrailCollision(self, objects):
		for obj in objects:
			if self.objectCollision(self.pos, obj) == 1:
				return
		

	def objectCollision(self, pos, obj):
		
		if self.actionstate == "on_ladder":
			return

		min_x = obj[0][0][0]
		max_x = obj[0][0][0]

		for line in obj:
			for point in line:
				if point[0] < min_x:
					min_x = point[0]
				if point[0] > max_x:
					max_x = point[0]
					
		for line in obj:

			do_collide = 0

			v1 = Vector(line[0])
			v2 = Vector(line[1])
			v3 = copy.deepcopy(pos)
			v3.y = v3.y + self.animation._src.h
			v3.x = v3.x + self.animation._src.w / 2
			
			t1 = v2 - v1

			t2 = v3 - v1

			t = (vecDot(t1,t2)) / (vecDot(t1, t1))
			
			v = v1 + t1 * t
				
			distance = vecDist(v3, v)
			
			left_obj = line[1][0]
			right_obj = line[0][0]

			if line[0][0] < line[1][0]:
				left_obj = line[0][0]
				right_obj = line[1][0]			

			if distance < 5 and v3.x >= left_obj and v3.x <= right_obj and self.actionstate != "jumping":
				do_collide = 1
				self.pos.y = v.y - self.animation._src.h
				self.ground = v.y
				self.current_ground = line

			elif (v3.x < min_x or v3.x > max_x) and line == self.current_ground:
				self.ground = globals.HEIGHT - 20
				self.actionstate = "falling"

		return do_collide

	def sideCollision(self):
		if self.pos.x + self.animation._src.w > globals.WIDTH:
			self.pos.x = globals.WIDTH - self.animation._src.w
		if self.pos.x < 0:
			self.pos.x = 0

		if self.pos.y + self.animation._src.h > globals.HEIGHT:
			self.pos.y = globals.HEIGHT - self.animation._src.h
		if self.pos.y < 0:
			self.pos.y = 0

	def floorCollision(self, ground):
		
		if self.actionstate == "on_ladder":
			return

		if self.pos.y + self.animation._src.h > ground:
			self.pos.y = ground - self.animation._src.h
			self.vel.x = 0; self.acc.x = 0
			self.vel.y = 0; self.acc.y = 0
			self.jumptime = 0
			self.actionstate = "on_ground"

	def applyGroundForce(self, force, dt):

		if self.actionstate != "on_ground":
			return

		if force.x == 0:
			self.vel.x = 0
			self.acc.x = 0
			return

		self.acc += force * dt

		max_accx = 1.5

		if self.acc.x > max_accx:
			self.acc.x = max_accx

		if self.acc.x < -max_accx:
			self.acc.x = -max_accx

		if force.x > 0 and self.vel.x < 0:
			self.acc.x = 0.0

		if force.x < 0 and self.vel.x > 0:
			self.acc.x = 0.0

		self.vel = force + self.acc * dt

	def applyVerticalForce(self, force, dt):

		if self.actionstate != "on_ladder":
			return

		self.vel = force * dt

	def setAnimationState(self, s):
		self.animationstate = s

	def updateAnimation(self, dt):

		if self.hammer_time > 0:

			if self.animationstate == "walk_left" or self.animationstate == "face_left":
				self.animation = globals.mario_with_hammer_left_an
			elif self.animationstate == "walk_right" or self.animationstate == "face_right":
				self.animation = globals.mario_with_hammer_right_an

		if self.hammer_time > 500:

			self.actionstate = "falling"

			if self.animation == globals.mario_with_hammer_right_an:
				self.animation = globals.mario_facing_right_an

			if self.animation == globals.mario_with_hammer_left_an:
				self.animation = globals.mario_facing_left_an

			self.hammer_time = 0

		if self.animation == globals.mario_with_hammer_right_an or \
		   self.animation == globals.mario_with_hammer_left_an:
		   	self.hammer_time += dt
		   	return


		if self.animationstate == "face_left":
			self.animation = globals.mario_facing_left_an		
		
			if self.actionstate == "jumping" or self.actionstate == "falling":
				self.animation = globals.mario_jump_facing_left_an

		elif self.animationstate == "face_right":
			self.animation = globals.mario_facing_right_an

			if self.actionstate == "jumping" or self.actionstate == "falling":
				self.animation = globals.mario_jump_facing_right_an
		
		elif self.animationstate == "walk_left":
			self.animation = globals.mario_walking_left_an
			if self.vel.x == 0:
				self.animationstate = "face_left"

			if self.actionstate == "jumping" or self.actionstate == "falling":
				self.animation = globals.mario_jump_facing_left_an

		elif self.animationstate == "walk_right":
			self.animation = globals.mario_walking_right_an
			if self.vel.x == 0:
				self.animationstate = "face_right"

			if self.actionstate == "jumping" or self.actionstate == "falling":
				self.animation = globals.mario_jump_facing_right_an

		elif self.animationstate == "run_left":
			self.animation = globals.mario_running_right_an
			if self.vel.x == 0:
				self.animationstate = "face_left"

			if self.actionstate == "jumping" or self.actionstate == "falling":
				self.animation = globals.mario_jump_facing_left_an

		elif self.animationstate == "run_right":
			self.animation = globals.mario_running_right_an
			if self.vel.x == 0:
				self.animationstate = "face_right"

			if self.actionstate == "jumping" or self.actionstate == "falling":
				self.animation = globals.mario_jump_facing_right_an

		# elif self.animationstate == "climb_on_top":
		# 	self.animation = globals.mario_top_ladder_on_an

		# elif self.animationstate == "climb_off_top":
		# 	self.animation = globals.mario_top_ladder_off_an

		if self.actionstate == "on_ladder" and self.vel.y == 0.0:
			self.animation = globals.mario_climb_still_an

		elif self.animationstate == "climb_up":
			self.animation = globals.mario_climb_up_an

		elif self.animationstate == "climb_down":
			self.animation = globals.mario_climb_down_an
		
		elif self.animationstate == "face_back":
			self.animation = globals.mario_facing_back_an		


	def applyGravity(self, dt):
		if self.actionstate == "on_ground":
			return

		if self.actionstate == "on_ladder":
			return

		self.vel.y += (0.5 * dt)

	def update(self, dt):

		self.applyGravity(dt)
		
		self.applyJump(dt)
		
		self.floorCollision(self.ground)
		
		self.sideCollision()
	
		self.move(dt)

		self.updateAnimation(dt)
		self.animation.update(dt)

	def debug_print(self):
		print "pos: ", self.pos
		print "vel: ", self.vel
		print "acc: ", self.acc
		print "sta: ", self.animationstate
		print "ani: ", self.animation
		print "jmp: ", self.jumptime
		print "jst: ", self.actionstate
	 	print "grd: ", self.ground
		print "\n\n\n"

	def draw(self, surface):
		self.animation.draw(surface, self.pos.x, self.pos.y)

