# -*- coding: utf-8 -*-
"""
The Main function of the Game.
Controlls the general flow.
"""

import pygame
from . import movement
from . import settings
from . import interface
from . import draw
from . import menu
from . import missions
from . import specials
from . import sounds
#TODO: Remove all * imports

#TODO: Replace all variables refering to settings
	#with refering to settings.variables

#Starts timer/clock for the movement, so it stays constant
pygame.time.set_timer(pygame.USEREVENT + 1, 25)

# initialize all variables for the modules
settings.init()
interface.init()
draw.init()
movement.init()
sounds.init()
movement.handle()
specials.init()

if not settings.variables.skip:
	menu.main()

#start clock for checking time how long has been played
#TODO: variables that are not inside functions or classes should be all caps
print(("Loading time:" + str(settings.loading_time / 1000.0)))
print(("Your seed is:" + str(settings.seed)))

# start clock for checking time how long has been played
global clock
clock = settings.clock

# start the missions
missions.init()


def main():
	"""The main loop of the program.

	Personally I think this should be in the Run.py file - Jarvis
	For me Run.py is a initiator which is responsible for starting the game
		while main.py is responsible for executing the game - Max
	"""

	while settings.run:
		# get events/user-input
		settings.upd("get_events")
		sounds.music.update(settings.events)
		sounds.music.volume = settings.volume

		# handle the user input
		interface.handle()

		# handles the movement every 25 milliseconds
		#TODO: Why every 25?
		#Because I defined it that way
		#	may be changed, but everything will speed up that way - max
		for event in settings.events:
			if event.type == pygame.USEREVENT + 1:
				movement.handle()

		# makes a clock tick (pygame internal stuff)
		clock.tick()

		# display everything
		draw.ingame()

		# check if missions have been fulfilled
		missions.handle("ingame")

while True:
	# basic cycle: Start game, when won show main menu
	main()
	settings.run = True
	settings.reset()
	menu.main()
