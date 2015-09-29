# -*- coding: utf-8 -*-
from . import settings
import pygame
from pygame.locals import *


def init():
	global newtime
	newtime = pygame.time.get_ticks()


def handle(usage):

	global newtime

	if usage == "ingame":
		oldtime = newtime
		newtime = pygame.time.get_ticks()
		settings.player.timeplay += newtime - oldtime
	if usage == "pause":
		oldtime = pygame.time.get_ticks()
		newtime = pygame.time.get_ticks()

	alltargets = 0
	for world in settings.localmap:
		alltargets += len(settings.localmap[world].targets)

	if alltargets == 0:
		from . import draw
		from . import movement

		while len(settings.explosions_disp) != 0:
			draw.ingame()
			movement.handle()

		screen = settings.screen

		settings.save(settings.current_game)

		fade = pygame.Surface((settings.screenx_current, settings.screeny_current))
		fade.fill((0, 0, 0))
		fade.set_alpha(0)
		fade_pos = fade.get_rect()

		font = pygame.font.SysFont(settings.typeface, 50)

		points = settings.player.timeplay
		color = settings.color
		texttime = font.render("Your time: " + str(points) + "ms", True, color)
		tmp = str(points / (settings.dtargets * 8.0))[:6]
		texttt = font.render("You needed " + tmp + "ms per target", True, color)
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
