# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *


def run():
	"""Displayes the credits"""
	from . import settings

	global lines
	global font
	global color

	color = settings.color
	lines = []
	lines_pos = []
	itera = -1
	fade = pygame.Surface((settings.screenx_current, settings.screeny_current))
	fade.fill((0, 0, 0))
	fade.set_alpha(0)
	fade_pos = fade.get_rect()
	pygame.mouse.set_visible(False)

	fade.set_alpha(255)
	screen = settings.screen
	screen.blit(fade, fade_pos)
	pygame.display.flip()

	settings.upd("screenvalues")

	# load the credits.txt and assign place
	with open("./assets/lang/credits.txt") as credits_file:
		# find the longest line to optimize font size
		biggest = 1000
		for line in credits_file:
			line = line[:-1]
			size = settings.getmaxsize(settings.typeface, 50,
				line, True, color,
				screen.get_rect().size, 0)
			if biggest > size:
				biggest = size
	with open("./assets/lang/credits.txt") as credits_file:
		for line in credits_file:
			itera += 1
			line = line[:-1]
			line = settings.modrender(settings.typeface, biggest,
				line, True, color,
				screen.get_rect().size, 0)
			line_pos = line.get_rect()
			# Distance from line to line is 5 pixel more than height
			line_pos.top = ((line_pos.h + 5) * itera) + settings.screeny_current
			line_pos.left = (settings.screenx_current / 2) - (line_pos.w / 2.0)
			lines.append(line)
			lines_pos.append(line_pos)

	# diplays content of credits.txt
	while not lines_pos[len(lines_pos) - 1].top <= -80:
		settings.upd("get_events")
		for event in settings.events:
			if event.type == QUIT:
				settings.quit()
			if event.type == KEYDOWN:
				if pygame.key.name(event.key) == "escape":
					lines_pos[len(lines_pos) - 1].top = -90
			if event.type == USEREVENT + 1:

				screen.blit(fade, fade_pos)

				for credit in range(len(lines)):
					screen.blit(lines[credit], lines_pos[credit])

				pygame.display.flip()

				for credit in range(len(lines)):
					lines_pos[credit].top -= 2

	pygame.mouse.set_visible(True)
