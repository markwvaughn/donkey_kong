import pygame, sys
from globals import *
from timer import *
from levelOne import *
import time
import copy

#######################################################
#
#	State Machine Class
#
#	- current_state
#	
#	+ changeState
#	+ getCurrentState
#	+ update
#
#######################################################

class StateMachine:

	def __init__(self):
		self.current_state = None

	def changeState(self, s):
		self.current_state = s

	def getCurrentState(self):
		return self.current_state

	def update(self):
		current_state.update()

#######################################################
#
#	State Class
#
#	+ enter
#	+ update
#	+ exit
#
#######################################################


class State:

	def __init__(self):
		pass

	def enter(self, sm):
		pass

	def update(self, sm):
		pass

	def exit(self):
		pass

class Game(StateMachine):

	def __init__(self):
		self.current_state = None

	def changeState(self, s):
		self.current_state = s

		if self.current_state:
			self.current_state.enter(self)

	def getCurrentState(self):
		return self.current_state

	def update(self):
		if self.current_state:
			self.current_state.update(self)


class StateIntro(State):

	def __init__(self):
		pass

	def enter(self, sm):
		pass

	def update(self, sm):

		k = 0
		j = 0
		
		fade_in = 4
		still = 2
		fade_out = 4
		length = fade_in + still + fade_out + 1

		start_intro_time = time.time()
		step = 255.0 / (fade_in * 60.0);
		step2 = 255.0 / (fade_out * 60.0);

		while time.time() - start_intro_time < length:
		
			# Exit if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()

			# Goto Menu if tab pressed
			key = pygame.key.get_pressed()
			if key[pygame.K_TAB]:
				sm.changeState(StateMenu())
				break


			color1 = (k,0,0)
			color2 = (0,k,0)

			intro_title = pixel_font80.render("Donkey Kong", 1, color1)
			intro_copyright = pixel_font30.render("Written by Mark Vaughn", 1, color2)

			fade_time = time.time() - start_intro_time

			if fade_time <= fade_in:
				k += step

			if fade_time > fade_in and fade_time < fade_in + still:
				k = 255

			if fade_time >= fade_in + still and fade_time < fade_in + still + fade_out:
				k -= step2

			if k < 0:
				k = 0

			if k > 255:
				k = 255

			# Draw surface  
			surface.fill(BLACK)
			surface.blit(intro_title, (WIDTH/2 - 150, HEIGHT/2 - 100))
			surface.blit(intro_copyright, (WIDTH/2 - 125, HEIGHT/2 - 20))
			pygame.display.flip()

		sm.changeState(StateMenu())

	def exit(self):
		pass

class StateMenu(State):

	def __init__(self):
		pass

	def enter(self, sm):
		pass

	def update(self, sm):
		
		donkey_kong_step_count = 0
		donkey_kong_step = 0
		dktitleRect.center = (WIDTH / 2, HEIGHT / 2 + 170)
		single_player_bool = 1

		intro_scores = Score()

		timer = Timer(pygame.time.get_ticks())

		# menu_music.play(-1,0.0)

		while 1:
			
			# Exit if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()

			# Keypressed
			key = pygame.key.get_pressed()
			if key[pygame.K_UP] and single_player_bool == 1:
				single_player_bool = 1

			elif key[pygame.K_UP] and single_player_bool == 0:
				single_player_bool = 1

			elif key[pygame.K_DOWN] and single_player_bool == 1:
				single_player_bool = 0

			elif key[pygame.K_DOWN] and single_player_bool == 0:
				single_player_bool = 0


			if key[pygame.K_RETURN] and single_player_bool:
				sm.changeState(StateLevelOne())
				break
			elif key[pygame.K_RETURN] and not single_player_bool:
				sm.changeState(ViewHighScoreMenu())
				break

			# update
			timer.update(pygame.time.get_ticks())

			# Menu Pointer
			if single_player_bool:
				menuPointerRect.center = (WIDTH/2 - 88, HEIGHT/2 + 66)
			else:
				menuPointerRect.center = (WIDTH/2 - 88, HEIGHT/2 + 89)

			# Donkey Kong Animation
			if donkey_kong_step_count % 20 == 0:
				donkey_kong_step += 1

			donkey_kong_step = donkey_kong_step % 6
			donkey_kong_step_count += 1
			donkey_kong_step = donkey_kong_step % 100

			# Draw surface  
			surface.fill(BLACK)
			surface.blit(titleScreenImage,titleScreenImageRect)

			surface.blit(menuPointer,menuPointerRect)

			# Donkey Kong Sprite
			if donkey_kong_step == 0:
				surface.blit(dktitle01,dktitleRect)
			elif donkey_kong_step == 1:
				surface.blit(dktitle02,dktitleRect)
			elif donkey_kong_step == 2:
				surface.blit(dktitle03,dktitleRect)
			elif donkey_kong_step == 3:
				surface.blit(dktitle04,dktitleRect)
			elif donkey_kong_step == 4:
				surface.blit(dktitle05,dktitleRect)
			elif donkey_kong_step == 5:
				surface.blit(dktitle06,dktitleRect)

			intro_scores.displayScores(surface, timer.dt)

			pygame.display.flip()

	def exit(self):
		pass


class StateLevelOne(State):

	def __init__(self):
		pass

	def enter(self, sm):
		globals.score = 0
		globals.time_bonus = 5000
		globals.bonus_timer = 0
		_ , globals.highscore = game_score.getHighScore()
		
		mario.reset()

		regular_barrels.reset(1)
		blue_barrels.reset(1)

		hammer1.reset()
		hammer2.reset()

	def update(self, sm):

		levelOne = LevelOne()
		levelOne.create()

		timer = Timer(pygame.time.get_ticks())

		clock_time = 0
		insert_flag = 0

		while 1:
			
			# Exit if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
			

			# Goto Menu if esc pressed
			key = pygame.key.get_pressed()
			if key[pygame.K_ESCAPE]:
				sm.changeState(StateMenu())
				break


			# timer
			timer.update(pygame.time.get_ticks())
			clock_time += timer.dt2

			globals.bonus_timer += (timer.dt2 / 1000.0)
			
			if globals.bonus_timer > 2:	
				globals.time_bonus -= 100
				globals.bonus_timer = 0

			if globals.time_bonus <= 0:
				globals.time_bonus = 0


			# Keypressed Section
			key = pygame.key.get_pressed()
			
			keypressed = 0

			if mario.actionstate != "on_ladder":
				if key[pygame.K_LEFT]:
					mario.setAnimationState("walk_left")
					mario.applyGroundForce(Vector((-1.5,0)), timer.dt)
					keypressed = 1

				if key[pygame.K_RIGHT]:
					mario.setAnimationState("walk_right")
					mario.applyGroundForce(Vector((1.5,0)), timer.dt)
					keypressed = 1

				if key[pygame.K_SPACE]:
					mario.jump(timer.time)
					keypressed = 1

			if key[pygame.K_UP]:
				mario.climb(levelOne.ladderlines, "up")
				mario.applyVerticalForce(Vector((0,-1.5)), timer.dt)
				keypressed = 1

			if key[pygame.K_DOWN]:
				mario.climb(levelOne.ladderlines, "down")
				mario.applyVerticalForce(Vector((0,1.5)), timer.dt)
				keypressed = 1

			if keypressed == 0:
				mario.applyVerticalForce(Vector((0,0)), timer.dt)
				mario.applyGroundForce(Vector((0,0)), timer.dt)


			# Update Objects
			mario.checkTrailCollision(levelOne.lines)
			reset1 = mario.barrelCollision(regular_barrels.barrels)
			reset2 = mario.barrelCollision(blue_barrels.barrels)

			mario.hammerCollision(hammer1)
			mario.hammerCollision(hammer2)

			levelOne.destroy_platform(timer.dt)

			win = mario.reachPaulineWin(pauline)

			mario.update(timer.dt)
			oilDrum.update(timer.dt)
			oilDrumFire.update(timer.dt)

			pauline.update(timer.dt)
			donkeykong.update(timer.dt)


			barrel_activate_flag = random.randrange(2)
			if barrel_activate_flag == 1:
				if regular_barrels.insert_flag == 0:
					blue_barrels.activate()
			else:
				if blue_barrels.insert_flag == 0:
					regular_barrels.activate()

			regular_barrels.update(timer, reset1 or reset2)
			regular_barrels.checkCollisions(levelOne)

			blue_barrels.update(timer, reset1 or reset2)
			blue_barrels.checkCollisions(levelOne)


			# Update Level
			levelOne.update()


			# Draw Objects
			surface.fill(BLACK)
			levelOne.draw(surface)

			for stacked_barrel in stacked_barrels:
				stacked_barrel.draw(surface)

			oilDrum.draw(surface)
			oilDrumFire.draw(surface)
	
			donkeykong.draw(surface)
			pauline.draw(surface)			

			hammer1.draw(surface)
			hammer2.draw(surface)

			mario.draw(surface)

			regular_barrels.draw(surface)
			blue_barrels.draw(surface)

			if win == True:
				game_over_win_title = pixel_font80.render("You Won", 1, (50,230,50))
				surface.blit(game_over_win_title, (135, 80))
				pygame.display.flip()
				sm.changeState(EnterHighScoreMenu())
				return

			if globals.mario_num_lives <= 0:
				game_over_lose_title = pixel_font80.render("Game Over", 1, (50,50,230))
				surface.blit(game_over_lose_title, (100, 80))
				pygame.display.flip()

				for i in range(1000):
					pygame.time.delay(5)
				
				sm.changeState(StateMenu())
				return


			pygame.display.flip()


	def exit(self):
		pass

class StateLevelTwo(State):

	def __init__(self):
		pass

	def enter(self, sm):
		pass

	def update(self, sm):
		while 1:
			
			# Exit if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()

			surface.fill(BLACK)
			pygame.display.flip()

	def exit(self):
		pass

class StateLevelThree(State):

	def __init__(self):
		pass

	def enter(self, sm):
		pass

	def update(self, sm):
		while 1:
			
			# Exit if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()

			surface.fill(BLACK)
			pygame.display.flip()


	def exit(self):
		pass

class StateLevelFour(State):

	def __init__(self):
		pass

	def enter(self, sm):
		pass

	def update(self, sm):
		while 1:
			
			# Exit if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()

			surface.fill(BLACK)
			pygame.display.flip()

	def exit(self):
		pass

#######################################################
# Level Intros
#######################################################
class StateLevelOneIntro(State):

	def __init__(self):
		pass

	def enter(self, sm):
		pass

	def update(self, sm):
		while 1:
			
			# Exit if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()

			surface.fill(BLACK)
			pygame.display.flip()

	def exit(self):
		pass

#######################################################
# Level Transitions
#######################################################
class StateLevelTransition(State):

	def __init__(self):
		pass

	def enter(self, sm):
		pass

	def update(self, sm):
		while 1:
			
			# Exit if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()

			surface.fill(BLACK)
			pygame.display.flip()

	def exit(self):
		pass

#######################################################
# High Score States
#######################################################
class EnterHighScoreMenu(State):

	def __init__(self):
		pass

	def enter(self, sm):
		pass

	def is_letter(self, char):

		char.lower()

		for c in "abcdefghijklmnopqrstuvwxyz":
			if char == c:
				return True

		return False

	def leftSpaces(self, name_string):
		num_spaces =  0
		string_rev = name_string[::-1]
		for c in string_rev:
			if c == " ":
				num_spaces += 1
			else:
				break

		return num_spaces

	def update(self, sm):

		name_string = ""

		time = 0

		while 1:
			
			# Exit if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					sys.exit()

				if event.type == pygame.KEYUP:

					if pygame.key.name(event.key) == "return" and len(name_string) > 0:
						sm.changeState(StateMenu())
						game_score.addScore(name_string, globals.score + globals.time_bonus)
						game_score.saveScores()
						return

					elif pygame.key.name(event.key) == "backspace" and len(name_string) > 0:
						name_string = name_string[:len(name_string)-1]

					elif len(name_string) <= 10:
						
						if self.is_letter(pygame.key.name(event.key)):

							if pygame.key.get_mods() == 1 or pygame.key.get_mods() == 2:
								name_string += pygame.key.name(event.key).upper()
							else:
								name_string += pygame.key.name(event.key)

						elif pygame.key.name(event.key) == "space":
							name_string += " "

			# ENTER NAME

			pygame.draw.rect(surface, (0,0,0), pygame.Rect(globals.WIDTH/2 - (250/2.0), globals.HEIGHT/2 - 100, 250, 100))

			pygame.draw.rect(surface, (230,50,50), pygame.Rect(globals.WIDTH/2 - (250/2.0) + 25/2.0, globals.HEIGHT/2 - 50, 225, 40), 2)
			pygame.draw.rect(surface, (255,255,255), pygame.Rect(globals.WIDTH/2 - (250/2.0), globals.HEIGHT/2 - 100, 250, 100), 2)

			high_score_title = pixel_font30.render("Enter Name", 1, (230,50,50))
			surface.blit(high_score_title, (globals.WIDTH/2 - 55, globals.HEIGHT/2 - 90))
			
			num_spaces = self.leftSpaces(name_string)
			high_score_name = pixel_font30.render(name_string, 1, (230,50,50))
			width = high_score_name.get_bounding_rect()[2] + 8 * num_spaces
			surface.blit(high_score_name, (globals.WIDTH/2 - width / 2.0, globals.HEIGHT/2-45))

			if time % 50 < 40 and len(name_string) <= 10:
				pygame.draw.rect(surface, (255,255,255), pygame.Rect(globals.WIDTH/2 + width / 2.0, globals.HEIGHT/2-20, 10, 2))
			
			time += 1

			pygame.display.flip()

	def exit(self):
		pass


class ViewHighScoreMenu(State):

	def __init__(self):
		pass

	def enter(self, sm):
		pass

	def update(self, sm):

		high_scores = Score()
		timer = Timer(pygame.time.get_ticks())

		while 1:
			
			# Exit if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					sys.exit()

				if event.type == pygame.KEYUP:

					if pygame.key.name(event.key) == "escape":
						sm.changeState(StateMenu())
						return

			timer.update(pygame.time.get_ticks())

			# ENTER NAME
			surface.fill(BLACK)

			high_score_title = pixel_font80.render("High Scores", 1, (230,50,50))
			surface.blit(high_score_title, (globals.WIDTH/2 - 135, 90))
			
			high_scores.displayScores(surface, timer.dt)
			pygame.display.flip()

	def exit(self):
		pass


#######################################################
# Game Over State
#######################################################
class StateGameOver(State):

	def __init__(self):
		pass

	def enter(self, sm):
		pass

	def update(self, sm):
		while 1:
			
			# Exit if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()

			surface.fill(BLACK)
			pygame.display.flip()

	def exit(self):
		pass
