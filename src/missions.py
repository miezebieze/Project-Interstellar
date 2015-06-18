# -*- coding: utf-8 -*-
from . import settings
import pygame
from pygame.locals import *


def init():
	global newtime
	newtime = pygame.time.get_ticks()


def handle(usage):

	global newtime

	timeplay = settings.timeplay

	if usage == "ingame":
		oldtime = newtime
		newtime = pygame.time.get_ticks()
		timeplay += newtime - oldtime
	if usage == "pause":
		oldtime = pygame.time.get_ticks()
		newtime = pygame.time.get_ticks()

	settings.timeplay = timeplay

	if len(settings.targets) == 0:
		from . import draw
		from . import movement

		while len(settings.explosions_disp) != 0:
			draw.ingame()
			movement.handle()

		screen = settings.screen

		settings.save(settings.current_game)

		fade = settings.fade
		fade_pos = settings.fade_pos

		font = pygame.font.SysFont(settings.typeface, 50)

		points = settings.timeplay
		color = settings.color
		texttime = font.render("Your time: " + str(points) + "ms", 1, color)
		tmp = str(points / 15.0)[:6]
		texttt = font.render("You needed " + tmp + "ms per target", 1, color)
		textrect = texttime.get_rect()
		textrectpertarget = texttt.get_rect()
		textrect.center = settings.screen.get_rect().center
		textrectpertarget.center = textrect.center
		textrectpertarget.top += 40

		while settings.run:
			settings.upd("get_events")

			for event in settings.events:
				if event.type == QUIT:
					settings.quit()
				if event.type == KEYDOWN:
					key = pygame.key.name(event.key)
					if key == "escape" or key == "return":
						settings.run = False
						settings.reset()

			screen.blit(fade, fade_pos)
			screen.blit(texttime, textrect)
			screen.blit(texttt, textrectpertarget)
			pygame.display.flip()