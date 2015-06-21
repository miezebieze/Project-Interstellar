# -*- coding: utf-8 -*-
from pygame.locals import *
import math
from . import settings

"""This handles the movement of nearly everything"""


def init():
	"""Initzializing variables"""
	from . import draw
	global player_pos
	global rotation
	global rot_dest
	global move
	global background_pos
	global draw
	player_pos = settings.player_pos
	background_pos = settings.world.background_pos
	background_pos.left = -(player_pos.left / 7.0) - 1
	background_pos.top = -(player_pos.top / 7.0) - 1
	rotation = 0
	rot_dest = 0
	move = False
	draw.playerpicturehandler()


def handle():
	"""Handle movement"""
	global player_pos
	global move_x
	global move_y
	global background_pos

	move = settings.move
	rot_dest = settings.rot_dest
	speed = settings.speed
	rotation = settings.rotation
	pos_x = settings.pos_x
	pos_y = settings.pos_y
	konstspeed = settings.konstspeed
	windowwidth = settings.screenx_current
	windowheight = settings.screeny_current

	if rotation > 360:
		rotation -= 360
	if rotation < 0:
		rotation += 360

	#handles rotation and gives signal to update player image/surface
	if rotation != rot_dest:
		settings.update = True

		if rot_dest > rotation:
			if (rot_dest - rotation) <= 180:
				rotation += 5.625
			if (rot_dest - rotation) > 180:
				rotation -= 5.625
		if rot_dest < rotation:
			if (rot_dest - rotation) > -180:
				rotation -= 5.625
			if (rot_dest - rotation) <= -180:
				rotation += 5.625

	#this part is responsible for the movement of the player
	#this calculates speed in y and x direction
	move_x = konstspeed * math.degrees(math.sin((math.radians(rotation))))
	move_y = -konstspeed * math.degrees(math.cos((math.radians(rotation))))

	#this actually moves the rect and ensures that you stay in screen
	if move:
		pos_x += float(move_x * speed) / (windowwidth)
		pos_y += float(move_y * speed) / (windowheight)

		if pos_x < 0:
			pos_x -= pos_x
		if pos_x > (1 - (float(player_pos.w) / windowwidth)):
			pos_x = 1 - (float(player_pos.w) / windowwidth)
		if pos_y < 0:
			pos_y -= pos_y
		if pos_y > (1 - (float(player_pos.h) / windowheight)):
			pos_y = 1 - (float(player_pos.h) / windowheight)

		player_pos.top = int(pos_y * windowheight)
		player_pos.left = int(pos_x * windowwidth)

	player_pos.top = int(pos_y * windowheight)
	player_pos.left = int(pos_x * windowwidth)

	#the following routines just handle moving everything thats generated

	settings.move = move
	settings.player_pos = player_pos
	settings.pos_x = pos_x
	settings.pos_y = pos_y
	settings.rotation = rotation

	#updates player image if neccesary
	draw.playerpicturehandler()