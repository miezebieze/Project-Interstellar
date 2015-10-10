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
	pygame.font
	# Checks for correct version
	if pygame.version.ver < "1.9.1":
		raise SystemExit("Old Pygame version: " + pygame.version.ver)
	required = "2.7.6"
	for i in range(len(required)):
		if sys.version_info[i] < required.split('.')[i]:
			raise SystemExit("Outdated Python version: %s; required: %s" % (sys.version.split()[0], required))
	if sys.version[:1] >= "3":
		raise SystemExit("No support for Python3")

	# Run the game
	from src import main
	main.void()

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
	detail = str(detail)
	print(detail)
	if detail[len(detail) - 5:][:4] == "font":  # Basicly the name of the module
		raise SystemExit("Font module not installed (SDL_ttf)!")
	else:
		print(("Unexpected error:", sys.exc_info()[0]))
		print("")
		raise SystemExit(traceback.format_exc())
except Exception as detail:
	# general errors
	print(("Unexpected error:", sys.exc_info()[0]))
	print("")
	raise SystemExit(traceback.format_exc())
