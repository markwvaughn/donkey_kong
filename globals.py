import pygame, sys
from animation import *
from object import *
from character import *
from vector import *
from event import *
from score import *

#########################################################################################
# HUD Variables
#########################################################################################

game_score = Score()

score = 0
time_bonus = 5000
bonus_timer = 0
mario_num_lives = 3


#########################################################################################
# pygame
#########################################################################################
pygame.init()

#########################################################################################
# screen
#########################################################################################
WIDTH = 480
HEIGHT = 640
SIZE = (WIDTH, HEIGHT)

#########################################################################################
# surface
#########################################################################################
surface = pygame.display.set_mode(SIZE)

#########################################################################################
# color
#########################################################################################
BLACK = (0, 0, 0)
RED = (255,0,0)

#########################################################################################
# fonts
#########################################################################################
pixel_font80 = pygame.font.SysFont("minipixel7", 80)
pixel_font30 = pygame.font.SysFont("minipixel7", 30)

#########################################################################################
# strings
#########################################################################################

#########################################################################################
# physics
#########################################################################################
# GRAVITY = 0.875

#########################################################################################
# images
#########################################################################################
titleScreenImage = pygame.image.load("images/TitleScreenLarge.png")
titleScreenImageRect = titleScreenImage.get_rect()

dktitle01	= pygame.image.load("images/dktitle01.png")
dktitle02	= pygame.image.load("images/dktitle02.png")
dktitle03	= pygame.image.load("images/dktitle03.png")
dktitle04 	= pygame.image.load("images/dktitle04.png")
dktitle05 	= pygame.image.load("images/dktitle05.png")
dktitle06 	= pygame.image.load("images/dktitle06.png")
dktitleRect = dktitle01.get_rect()

menuPointer = pygame.image.load("images/menu_pointer.png")
menuPointerRect = menuPointer.get_rect()

#########################################################################################
#sounds
#########################################################################################
menu_music = pygame.mixer.Sound("sounds/dkca.wav")
level_one_start_music = pygame.mixer.Sound("sounds/dk-stagestart.wav")
level_one_music = pygame.mixer.Sound("sounds/DKLevel1.wav")
win_music = pygame.mixer.Sound("sounds/Donkey_Kong_Win.wav")
game_over_music = pygame.mixer.Sound("sounds/Donkey_Kong_Falls.wav")

mario_die_music = pygame.mixer.Sound("sounds/mario_die.wav")
mario_hammer_music = pygame.mixer.Sound("sounds/dk-hammer2.wav")
mario_jump_music = pygame.mixer.Sound("sounds/jump.wav")
mario_jump_bar_music = pygame.mixer.Sound("sounds/jump_bar.wav")
mario_walk_music = pygame.mixer.Sound("sounds/walking.wav")


#########################################################################################
#sprites
#########################################################################################

# mario
mario_walking_right_s 			= pygame.image.load("images/mario_running_right3.png")
mario_walking_left_s 			= pygame.image.load("images/mario_running_left3.png")
mario_climbing_up_s 			= pygame.image.load("images/mario_climbing.png")
mario_climbing_down_s 			= pygame.image.load("images/mario_climbing2.png")
mario_life_s					= pygame.image.load("images/mario_lives.png")
mario_with_hammer_left_s		= pygame.image.load("images/mario_brown_hammer.png")
mario_with_hammer_right_s		= pygame.image.load("images/mario_brown_hammer2.png")

# objects
barrel_cement_flower_s 			= pygame.image.load("images/barrel_cement_flower.png")
bluebarrel_fireball_hammer_s 	= pygame.image.load("images/bluebarrel_fireball_hammer.png")
oil_barrel_fire_s 				= pygame.image.load("images/fire_oil_explosion.png")


# stage
ladder_platforms_s 				= pygame.image.load("images/ladder_platforms2.png")
ladder_s 						= pygame.image.load("images/white_ladder.png")


# characters
donkey_kong_s 					= pygame.image.load("images/donkey_kong.png")
pauline_s 						= pygame.image.load("images/pauline.png")


#########################################################################################
#animations
#########################################################################################

# mario
mario_facing_right_an 		= Animation(mario_walking_right_s, 0, 40, 40, 1, 0)
mario_facing_left_an 		= Animation(mario_walking_left_s, 0, 40, 40, 1, 0)

mario_walking_right_an 		= Animation(mario_walking_right_s, 0, 120, 40, 1, 15)
mario_walking_left_an 		= Animation(mario_walking_left_s, 0, 120, 40, 1, 15)

mario_running_right_an 		= Animation(mario_walking_right_s, 0, 120, 40, 1, 20)
mario_running_left_an 		= Animation(mario_walking_left_s, 0, 120, 40, 1, 20)

mario_jump_facing_right_an 	= Animation(mario_walking_right_s, 80, 120, 40, 1, 0)
mario_jump_facing_left_an 	= Animation(mario_walking_left_s, 80, 120, 40, 1, 0)

mario_climb_up_an 			= Animation(mario_climbing_up_s, 0, 80, 40, 1, 4)
mario_climb_down_an			= Animation(mario_climbing_down_s, 120, 200, 40, 1, 4)
mario_climb_still_an 		= Animation(mario_climbing_down_s, 120, 160, 40, 1, 0)
mario_facing_back_an 		= Animation(mario_climbing_down_s, 0, 40, 40, 1, 0)

mario_with_hammer_left_an	= Animation(mario_with_hammer_left_s, 0, 360, 60, 1, 20)
mario_with_hammer_right_an	= Animation(mario_with_hammer_right_s, 0, 360, 60, 1, 20)

# stage
red_platform_an 				= Animation(ladder_platforms_s, 240, 260, 20, 1, 1)
	
white_ladder_middle_an 			= Animation(ladder_s, 0, 16, 16, 1, 0)
white_ladder_top_an 			= Animation(ladder_s, 16, 32, 16, 1, 0)
white_ladder_bot_an				= Animation(ladder_s, 32, 48, 16, 1, 0)
	
oil_barrel_an 					= Animation(oil_barrel_fire_s, 160, 200, 40, 1, 0)
oil_barrel_fire_an 				= Animation(oil_barrel_fire_s, 0, 160, 40, 1, 7)
explosion_an 					= Animation(oil_barrel_fire_s, 200, 400, 40, 1, 15)
	
barrel_sideways_an 				= Animation(barrel_cement_flower_s, 0, 160, 40, 1, 4)
barrel_wide_an 					= Animation(barrel_cement_flower_s, 160, 240, 40, 1, 4)
barrel_vertical_an 				= Animation(barrel_cement_flower_s, 240, 280, 40, 1, 0)
	
bluebarrel_sideways_an 			= Animation(bluebarrel_fireball_hammer_s, 0, 160, 40, 1, 4)
bluebarrel_wide_an				= Animation(bluebarrel_fireball_hammer_s, 160, 240, 40, 1, 4)
bluebarrel_vertical_an 			= Animation(bluebarrel_fireball_hammer_s, 240, 280, 40, 1, 0)


# characters
donkey_kong_stomp_an 			= Animation(donkey_kong_s, 0, 600, 100, 1, 3)
donkey_kong_dead_an 			= Animation(donkey_kong_s, 600, 900, 100, 1, 0)
donkey_kong_carry_pauline_an 	= Animation(donkey_kong_s, 900, 1200, 100, 1, 0)
donkey_kong_throw_barrel_an 	= Animation(donkey_kong_s, 1200, 1400, 100, 1, 0)

pauline_still_an				= Animation(pauline_s, 0, 50, 50, 1, 0)
pauline_motion_an 				= Animation(pauline_s, 0, 150, 50, 1, 0)


# objects
hammer_an						= Animation(bluebarrel_fireball_hammer_s, 360, 400, 40, 1, 0)
fireball_an						= Animation(bluebarrel_fireball_hammer_s, 280, 360, 40, 1, 2)


#########################################################################################
# Characters
#########################################################################################
mario 		= Mario(Vector((100,HEIGHT-60)), Vector((0,0)), "face_right", mario_walking_right_an)
donkeykong 	= DonkeyKong(Vector((30,160)),Vector((0,0)),Vector((0,0)), donkey_kong_stomp_an)
pauline 	= Pauline(Vector((110,140)),Vector((0,0)),Vector((0,0)),pauline_still_an)

#########################################################################################
# Objects
#########################################################################################
oilDrum 	= OilDrum(Vector((20,HEIGHT-60)),Vector((0,0)),Vector((0,0)),oil_barrel_an)
oilDrumFire = OilDrumFire(Vector((20,HEIGHT-95)),Vector((0,0)),Vector((0,0)),oil_barrel_fire_an)
hammer1 	= Hammer(Vector((120,250)),Vector((0,0)),Vector((0,0)),hammer_an)
hammer2		= Hammer(Vector((380,475)),Vector((0,0)),Vector((0,0)),hammer_an)

# blue rolling barrels
blue_barrels = BlueBarrelList()

# regular rolling barrels
regular_barrels = RegularBarrelList()

# stacked barrels
num_stacked_barrels = 4
stacked_barrels = []

sb1 = RegularBarrel(Vector((5,165)),Vector((0,0)),Vector((0,0)),barrel_vertical_an, 1)
sb2 = RegularBarrel(Vector((35,165)),Vector((0,0)),Vector((0,0)),barrel_vertical_an, 1)
sb3 = RegularBarrel(Vector((5,200)),Vector((0,0)),Vector((0,0)),barrel_vertical_an, 1)
sb4 = RegularBarrel(Vector((35,200)),Vector((0,0)),Vector((0,0)),barrel_vertical_an, 1)

stacked_barrels.append(sb1)
stacked_barrels.append(sb2)
stacked_barrels.append(sb3)
stacked_barrels.append(sb4)

