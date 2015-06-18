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
	global update
	global draw
	player_pos = settings.player_pos
	background_pos = settings.background_pos
	background_pos.left = -(player_pos.left / 7.0) - 1
	background_pos.top = -(player_pos.top / 7.0) - 1
	rotation = 0
	rot_dest = 0
	move = False
	update = False
	draw.playerpicturehandler()


def handle():
	"""Handle movement"""
	global player_pos
	global speed
	global rotation
	global rot_dest
	global move
	global move_x
	global move_y
	global background_pos
	global update

	up = settings.up
	down = settings.down
	left = settings.left
	right = settings.right
	speed = settings.speed
	pos_x = settings.pos_x
	pos_y = settings.pos_y
	konstspeed = settings.konstspeed
	stars = settings.stars
	bullets = settings.bullets
	windowwidth = settings.screenx_current
	windowheight = settings.screeny_current
	fake_size = settings.fake_size
	move = False

	#this part sets the direction depending of input
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
	if up == down and left == right:
		move = False

	if rotation > 360:
		rotation -= 360
	if rotation < 0:
		rotation += 360

	#handles rotation and gives signal to update player image/surface
	if rotation != rot_dest:
		update = True

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
		tmp = -(pos_x * (windowwidth * (fake_size - 1)))
		background_pos.left = int(tmp)
		tmp = -(pos_y * (windowheight * (fake_size - 1)))
		background_pos.top = tmp

	player_pos.top = int(pos_y * windowheight)
	player_pos.left = int(pos_x * windowwidth)

	#the following routines just handle moving everything thats generated
	for star in stars:
		star.move(player_pos.left, player_pos.top)

	settings.move = move
	settings.player_pos = player_pos
	settings.pos_x = pos_x
	settings.pos_y = pos_y

	for bullet in bullets:
		bullet.move(player_pos)
		if not bullet.inscreen:
			settings.bullets.remove(bullet)

	for explosion in settings.explosions_disp:
		if explosion.kill_entity:
			settings.explosions_disp.remove(explosion)
		else:
			explosion.move(player_pos.left, player_pos.top)

	for target in settings.targets:
		target.move(player_pos.left, player_pos.top)
		for bullet in bullets:
			target.test_ishit(bullet.pos)
		if target.gothit:
			settings.targets.remove(target)
			settings.explosions_disp.append(target)
			settings.explosions_disp = list(set(settings.explosions_disp))

	#updates player image if neccesary
	draw.playerpicturehandler()