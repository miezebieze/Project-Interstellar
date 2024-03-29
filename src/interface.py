# -*- coding: utf-8 -*-
import pygame
import time
import string
from . import settings
from . import menu
from . import sounds
from . import objects
from . import midi_in
from . import specials
from pygame.locals import *


def init():
	if settings.debugmode:
		midi_in.init()

"""Handles user input"""


def handle():

	# handles user input
	# i think nothing to explain here

	if settings.debugmode:
		midi_in.do()

	for event in settings.events:
		if event.type == QUIT:
			exit()
		if event.type == KEYUP:
			key = pygame.key.name(event.key)
			if key == "x" or key == "y":
				settings.player.speedboost = 1
			if key == "w" or key == "up":
				settings.up = False
			if key == "s" or key == "down":
				settings.down = False
			if key == "a" or key == "left":
				settings.left = False
			if key == "d" or key == "right":
				settings.right = False

		if event.type == KEYDOWN:
			key = pygame.key.name(event.key)
			if key == "escape":
				menu.pause()
			if key == "f3":
				settings.debugscreen = settings.toggle(settings.debugscreen, True, False)
			if key == "f12":
				filename = "./screenshots/screenshot" + time.strftime("^%d-%m-%Y^%H.%M.%S")
				pygame.image.save(settings.screen, filename + ".png")
			if key == "f6":
				sounds.music.play("next")
			if key == "x":
				settings.player.speedboost = 0.3
			if key == "y":
				settings.player.speedboost = 1.7
			if key == "w" or key == "up":
				settings.up = True
			if key == "s" or key == "down":
				settings.down = True
			if key == "a" or key == "left":
				settings.left = True
			if key == "d" or key == "right":
				settings.right = True
			if key == "o":
				if settings.player.pos.x >= 0.9 and settings.player.pos.y >= 0.9:
					pygame.mixer.music.load("./assets/music/$not$ard_tatort.ogg")
					pygame.mixer.music.play(1, 0.0)
			if key == "f" or key == "space":
				tmp = objects.bullet(settings.player.rotation, settings.player.pos)
				settings.bullets.append(tmp)
			if key == "c":
				specials.fire = True
			if settings.debugmode:
				if key == "r":
					settings.world.adjust_to_screen()
				if key == "q":
					settings.init()
				if key == "p":
					settings.psycomode = settings.toggle(settings.psycomode, True, False)
				if key == "q":
					settings.volume = 0
				if key == "n":
					settings.player.new_ship("ship_2")
				if key == "t":
					for target in settings.world.targets:
						target.test_ishit(pygame.Rect((-1000, -1000), (3000, 3000)))
				if key == "g":
					settings.localmap["1"].generate(settings.localmap["1"].background,
								settings.dstars, settings.dtargets)
					settings.world.generate(settings.world.background,
								settings.dstars, settings.dtargets)
				if key == "h":
					for target in settings.world.targets:
						print((target.pos))
				if len(key) == 3 and settings.debugmode:
					if key[0] == "[" and key[2] == "]":
						num = int(key[1])
						if num != 5:
							if num > 5:
								num -= 1
							settings.world = settings.localmap[str(num)]

		settings.player.select_angle(settings.up, settings.down,
				settings.left, settings.right)

		specials.update()


def getall(allkeys):
	"""Gets all pressed keys"""
	for event in settings.events:
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN:
			key = pygame.key.name(event.key)
			tmp = (not key == "return" and not allkeys)
			if (event.unicode in string.printable or (key[:5] == "world")) and tmp:
				return event.unicode
			elif allkeys:
				return key
