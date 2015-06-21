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

"""Handles user input"""


def handle():

	screen_x = settings.screenx_current
	screen_y = settings.screeny_current

	#handles user input
	#i think nothing to explain here

	midi_in.do()

	for event in settings.events:
		if event.type == QUIT:
			exit()
		if event.type == KEYUP:
			key = pygame.key.name(event.key)
			if key == "x" or key == "y":
				settings.speed = 15
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
				settings.speed = 5
			if key == "y":
				settings.speed = 40
			if key == "w" or key == "up":
				settings.move = True
				settings.up = True
				settings.rot_dest = 0
			if key == "s" or key == "down":
				settings.move = True
				settings.down = True
				settings.rot_dest = 180
			if key == "a" or key == "left":
				settings.move = True
				settings.left = True
				settings.rot_dest = 270
			if key == "d" or key == "right":
				settings.move = True
				settings.right = True
				settings.rot_dest = 90
			if key == "o" and settings.pos_x >= 0.9 and settings.pos_y >= 0.9:
				pygame.mixer.music.load("./assets/music/$not$ard_tatort.ogg")
				pygame.mixer.music.play(1, 0.0)
			if key == "c":
				specials.fire = True

			if key == "f" or key == "space":
				tmpx = settings.pos_x * screen_x
				tmpy = settings.pos_y * screen_y
				tmp = objects.bullet(tmpx, tmpy, settings.rotation, settings.player_pos)
				settings.bullets.append(tmp)
			if key == "o":
				if pygame.key.get_mods() == 4416:
					settings.psycomode = settings.toggle(settings.psycomode, True, False)
					pass
			if key == "q":
				settings.volume = 0
			if key == "t":
				#settings.targets = []
				pass

		select_angle(settings.up, settings.down, settings.left, settings.right)

		specials.update()


def select_angle(up, down, left, right):

	rot_dest = settings.rot_dest
	move = False
	#sets the direction depending of input
	if not (up == down and left == right):
		#diagonal moves
		if up and left and not down and not right:
			move = True
			rot_dest = 315
		if up and right and not left and not down:
			move = True
			rot_dest = 45
		if down and left and not up and not right:
			move = True
			rot_dest = 225
		if down and right and not up and not left:
			move = True
			rot_dest = 135
		#moving in y != x
		if up and not down:
			if left == right:
				move = True
				rot_dest = 0
		if left and not right:
			if down == up:
				move = True
				rot_dest = 270
		if down and not up:
			if left == right:
				move = True
				rot_dest = 180
		if right and not left:
			if up == down:
				move = True
				rot_dest = 90

	settings.move = move
	settings.rot_dest = rot_dest


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
