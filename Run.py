# -*- coding: utf-8 -*-
"""
Used to start the Game and ensure that everythings works fine.
Otherwise it reports an errormessage.
"""

try:
	import pygame
	import sys
	import traceback
	import os

	os.environ['SDL_VIDEO_CENTERED'] = '1'

	pygame.init()
	# checks if font module is availible
	pygame.font.init()
	# Checks for correct version
	if pygame.version.ver < "1.9.1":
		raise SystemExit("Old Pygame version: " + pygame.version.ver)
	if sys.version[:5] < "2.7.6":
		raise SystemExit("Outdated Python version: " + sys.version[:5])
	if sys.version[:5] >= "3.0.0":
		raise SystemExit("No support for Python3")

	# Run the game
	from src import main  # lint:ok
	#main.void() Not sure why this is here, main has no void member
	#else main would be unused - Max

# Handeling errors
except ImportError as message:
	if str(message)[len(str(message)) - 6:] == "pygame":  # pygame not installed
		raise SystemExit("Pygame not installed")
	else:
		# unknown import error
		print (("ERROR IMPORTING MODULES: %s" % message))
		raise SystemExit(traceback.format_exc())
except AttributeError as detail:
	# excuted if font module is not installed
	MESSAGE = str(detail)
	if MESSAGE[len(MESSAGE) - 5:][:4] == "font":  # the name of the module
		raise SystemExit("Font module not installed (SDL_ttf)!")
		#TODO: Would it be possible for this module not to be installed?
	else:
		print(("Unexpected error:", sys.exc_info()[0]))
		print("")
		raise SystemExit(traceback.format_exc())
except Exception as detail:
	# general errors
	print(("Unexpected error:", sys.exc_info()[0]))
	print("")
	raise SystemExit(traceback.format_exc())
