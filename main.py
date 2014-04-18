import pygame, sys
from state import *
from event import *

#application
application_state = 0
game = Game()
game.changeState(StateIntro())

#################################################################
# Init Functions
#################################################################	
def init_game():
	application_state = 0
	pygame.display.set_caption("Donkey Kong")

#################################################################
# GAME
#################################################################

init_game()

while 1:

	game.update()