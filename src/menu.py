# -*- coding: utf-8 -*-
from . import settings
from . import namings
from . import objects
from . import sounds
from . import missions
from libs.pyganim import pyganim
import pygame
from pygame.locals import *

"""Responsible tor the menus"""


def main():
	"""Main menu"""
	#i hope its easy to understand
	screen = settings.screen
	screenx = settings.screenx_current
	screeny = settings.screeny_current
	fade = settings.fade
	fade_pos = settings.fade_pos
	color = settings.color
	planets = []
	background = pygame.image.load("./assets/sprites/Background1.tif")
	background = pygame.transform.scale(background, (screenx, screeny))
	background_pos = background.get_rect()
	src = "./assets/sprites/spinning_planet/planet-"
	for num in range(150):
		planets.append((src + str(num) + ".png", 0.065))
	planet = pyganim.PygAnimation(planets)
	planet.rotozoom(20, 0.5)
	planet_pos = planet.getRect()
	planet_pos = planet_pos.move(int(screenx * 0.65), int(screeny * 0.33))
	planet.play()

	settings.upd("screenvalues+vol")

	screenx /= 2.0
	screeny /= 4.0
	pygame.mouse.set_visible(True)
	run = True

	start = objects.button(screenx, screeny, "Start", color)
	setting = objects.button(screenx, screeny + 40, "Settings", color)
	credit = objects.button(screenx, screeny + 80, "Credits", color)
	escape = objects.button(screenx, screeny + 120, "Exit", color)

	sounds.music.queue("$not$menue.ogg", 0)
	sounds.music.play("stop")
	sounds.music.play("play", -1)

	alpha = 0.0

	while run:

		if alpha < 200:
			alpha += 1
			fade.set_alpha(alpha / 2)

		screen.blit(background, background_pos)
		screen.blit(fade, fade_pos)
		planet.blit(screen, planet_pos)
		screen.blit(fade, fade_pos)
		start.blit()
		setting.blit()
		credit.blit()
		escape.blit()
		pygame.display.flip()

		settings.upd("get_events")

		sounds.music.update(False, False)
		for event in settings.events:
			if event.type == QUIT:
				settings.quit()
			if event.type == KEYDOWN:
				key = pygame.key.name(event.key)
				if key == "escape":
					settings.quit()
				if key == "return":
					settings.reset()
					sounds.music.play("next")
					run = False
			if event.type == USEREVENT and event.code == "MENU":
				pygame.time.delay(200)
				if start.klicked:
					settings.reset()
					sounds.music.play("next")
					run = False
				if setting.klicked:
					options()
					screenx = settings.screenx_current
					screeny = settings.screeny_current
					planet_pos.topleft = (int(screenx * 0.65), int(screeny * 0.33))
					background = pygame.transform.scale(background,
						(int(screenx), int(screeny)))
					screenx /= 2.0
					screeny /= 4.0
					start.move(screenx, screeny)
					setting.move(screenx, screeny + 40)
					credit.move(screenx, screeny + 80)
					escape.move(screenx, screeny + 120)
				if credit.klicked:
					namings.run()
					alpha = 0
				if escape.klicked:
					settings.quit()
	pygame.mouse.set_visible(False)


def pause():
	"""pausing menu"""
	#should be easy to understand too
	screen = settings.screen
	screenx = settings.screenx_current / 2
	screeny = settings.screeny_current / 4
	fade = settings.fade
	fade_pos = settings.fade_pos
	color = settings.color

	sounds.music.play("pause")
	pygame.mouse.set_visible(True)
	fade.set_alpha(255)
	screen.blit(fade, fade_pos)
	fade.set_alpha(100)

	run = True
	back = objects.button(screenx, screeny, "Continue", color)
	save = objects.button(screenx, screeny + 40, "Save Game", color)
	load = objects.button(screenx, screeny + 80, "Load Game", color)
	option = objects.button(screenx, screeny + 120, "Settings", color)
	escape = objects.button(screenx, screeny + 160, "Quit", color)

	while run:

		screen.blit(fade, fade_pos)
		back.blit()
		save.blit()
		load.blit()
		option.blit()
		escape.blit()
		pygame.display.flip()

		missions.handle("pause")

		settings.upd("get_events")

		for event in settings.events:
			if event.type == QUIT:
				settings.quit()
			if event.type == KEYDOWN:
				key = pygame.key.name(event.key)
				if key == "escape":
					main()
					run = False
					pass
				if key == "return":
					sounds.music.play("unpause")
					run = False
					pass
			if event.type == USEREVENT and event.code == "MENU":
				pygame.time.delay(200)
				if back.klicked:
					sounds.music.play("unpause")
					run = False
				if save.klicked:
					savename = inputpopup(screenx, screeny * 2, "Save Game")
					if savename != "Exit":
						settings.save(savename)
				if load.klicked:
					savegame = savegames()
					if savegame != "Exit":
						settings.load(savegame)
						sounds.music.play("unpause")
						run = False
				if option.klicked:
					options()
					screenx = settings.screenx_current / 2.0
					screeny = settings.screeny_current / 4.0
					back.move(screenx, screeny)
					save.move(screenx, screeny + 40)
					load.move(screenx, screeny + 80)
					option.move(screenx, screeny + 120)
					escape.move(screenx, screeny + 160)
				if escape.klicked:
					main()
					run = False

	run = True
	pygame.mouse.set_visible(False)


def inputpopup(x, y, header):
	"""Method for having an inputfield or selecting savegame"""
	#as said takes and input and returns a string or returns
	#savegame if header is saying so

	screen = settings.screen
	fade = settings.fade
	fade_pos = settings.fade_pos

	infield1 = objects.inputfield(x, y, 1, header, settings.color)
	screen.blit(fade, fade_pos)

	run = True

	while run:

		screen.blit(fade, fade_pos)

		if header == "Load Game":
			text = savegames()
			return text
		settings.upd("get_events")

		text = infield1.gettext()

		for event in settings.events:
			if event.type == KEYDOWN:
				if pygame.key.name(event.key) == "escape":
					return "Exit"

		infield1.blit()
		pygame.display.flip()

		if text is not None:
			run = False

	return text


def savegames():
	"""creates wall with savegames to select"""
	#problem? ask me.

	settings.upd("get_saves")

	saves = settings.saves
	screen = settings.screen
	screenx = settings.screenx_current
	screeny = settings.screeny_current
	color = settings.color
	fade = settings.fade
	fade_pos = settings.fade_pos

	xaxis = []
	yaxis = []
	saves_buttons = []
	run = True

	fade.set_alpha(20)

	for y in range(10):
		y += 1
		for x in range(5):
			x += 1
			xaxis.append(screenx / 6 * x)
			yaxis.append(screeny / 11 * y + 50)

	for a in range(len(saves)):
		tmp = saves[a].replace("\\", "/")
		saves_buttons.append(objects.button(xaxis[a], yaxis[a], tmp, color))

	a = 0
	while run:
		for a in range(len(saves)):
			saves_buttons[a].blit()
		settings.upd("get_events")
		for event in settings.events:
			if event.type == QUIT:
				settings.quit()
			if event.type == KEYDOWN:
				key = pygame.key.name(event.key)
				if key == "escape":
					return "Exit"
			if event.type == USEREVENT and event.code == "MENU":
				for a in range(len(saves)):
					if saves_buttons[a].klicked:
						pygame.display.flip()
						pygame.time.delay(200)
						return saves[a]

		pygame.display.flip()
		screen.blit(fade, fade_pos)

	run = True


def options():
	"""The settings menu"""
	#again: fairly easy

	fade = settings.fade
	fade_pos = settings.fade_pos
	screenx = settings.screenx_current / 2.0
	screeny = settings.screeny_current / 4.0
	color = settings.color
	screen = settings.screen
	fullscreen = settings.fullscreen

	if fullscreen == 1:
		ison = "ON"
	else:
		ison = "OFF"

	sounds.music.update()
	sound = objects.sliders(sounds.music.volume, screenx, screeny)
	fulscren = objects.button(screenx, screeny + 40, "Fullscreen : " + ison, color)
	menu = objects.button(screenx, screeny + 80, "Back", color)

	run = True

	fade.set_alpha(255)
	screen.blit(fade, fade_pos)
	fade.set_alpha(100)

	sounds.music.play("pause")
	sounds.music.queue("$not$testsound.mp3", 0)
	sounds.music.play("play")

	while run:

		screen.blit(fade, fade_pos)
		sound.blit("Volume: ")
		fulscren.blit()
		menu.blit()
		pygame.display.flip()

		settings.upd("get_events")

		sounds.music.update(False, False)
		for event in settings.events:
			if event.type == KEYDOWN:
				key = pygame.key.name(event.key)
				if key == "escape":
					pygame.mixer.music.pause()
					sounds.music.play("unpause")
					run = False
			if event.type == QUIT:
				settings.quit()
			if event.type == USEREVENT and event.code == "MENU":
				pygame.time.delay(200)
				if fulscren.klicked:
					fullscreen = settings.toggle(fullscreen, False, True)
					if fullscreen:
						fulscren.changetext("Fullscreen : ON", color)
					elif not fullscreen:
						fulscren.changetext("Fullscreen : Off", color)
				if menu.klicked:
					sounds.music.play("unpause")
					run = False

		sound.modify(settings.events)
		sounds.music.volume = sound.value
		sounds.music.update(False, False)

	settings.fullscreen = fullscreen
	settings.upd("adjust_screen")