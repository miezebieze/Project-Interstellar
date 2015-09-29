# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *


def modrender(typeface, size, text, antialias, color, maxsize, borderoff):
	size = getmaxsize(typeface, size, text, maxsize, borderoff)
	tmpfont = pygame.font.SysFont(typeface, size)
	return tmpfont.render(text, antialias, color)


def getmaxsize(typeface, size, text, maxsize, borderoff):
	# local typeface!
	nofit = True
	while nofit:
		tmpfont = pygame.font.SysFont(typeface, size)
		bool1 = tmpfont.size(text)[0] < maxsize[0] - (2 * borderoff)
		nofit = not (bool1 and tmpfont.size(text)[1] < maxsize[1] - (2 * borderoff))
		if size <= 5:
			nofit = False
		else:
			size -= 1
	return size


def run():
	"""Displayes the credits"""
	from . import settings

	variables = settings.variables
	color = variables.color
	lines = []
	lines_pos = []
	itera = -1
	fade = pygame.Surface((variables.screenx_current, variables.screeny_current))
	fade.fill((0, 0, 0))
	fade.set_alpha(0)
	fade_pos = fade.get_rect()
	pygame.mouse.set_visible(False)

	fade.set_alpha(255)
	screen = variables.screen
	screen.blit(fade, fade_pos)
	pygame.display.flip()

	variables.upd("screenvalues")

	# load the credits.txt and assign place
	with open("./assets/lang/credits.txt") as credits_file:
		# find the longest line to optimize font size
		biggest = 1000
		for line in credits_file:
			line = line[:-1]
			size = getmaxsize(variables.typeface, 50,
				line, screen.get_rect().size, 0)
			if biggest > size:
				biggest = size
	with open("./assets/lang/credits.txt") as credits_file:
		for line in credits_file:
			itera += 1
			line = line[:-1]
			line = modrender(variables.typeface, biggest,
				line, True, color,
				screen.get_rect().size, 0)
			line_pos = line.get_rect()
			# Distance from line to line is 5 pixel more than height
			line_pos.top = ((line_pos.h + 5) * itera) + variables.screeny_current
			line_pos.left = (variables.screenx_current / 2) - (line_pos.w / 2.0)
			lines.append(line)
			lines_pos.append(line_pos)

	# diplays content of credits.txt
	while not lines_pos[len(lines_pos) - 1].top <= -80:
		variables.upd("get_events")
		for event in variables.events:
			if event.type == QUIT:
				variables.quit()
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
