# -*- coding: utf-8 -*-
from pygame.locals import *
from . import settings

"""This handles the movement of nearly everything"""


def init():
	"""Initzializing variables"""
	global background_pos
	global draw

	background_pos = settings.variables.world.background_pos
	background_pos.left = -(settings.variables.player.pos.left / 7.0) - 1
	background_pos.top = -(settings.variables.player.pos.top / 7.0) - 1


def handle():
	"""Handle movement"""

	settings.variables.world.move()
	settings.variables.player.move()
