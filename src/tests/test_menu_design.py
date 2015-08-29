# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from data import creator
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
os.chdir("../../")

global screen

pygame.init()
pygame.fastevent.init()
screen = pygame.display.set_mode((600, 400))


class fade_screen():

	def __init__(self, step, step2, max_alpha, screenx, screeny):
		self.fade = pygame.Surface((screenx, screeny))
		self.fade.fill((0, 0, 0))
		self.fade.set_alpha(0)
		self.timer = pygame.time.get_ticks()
		self.alpha = 0
		self.max_alpha = max_alpha
		self.step = step
		self.step2 = step2

	def blit(self, screen):
		time = pygame.time.get_ticks()
		if (time - self.timer) > self.step and self.alpha <= self.max_alpha:
			self.timer = pygame.time.get_ticks()
			self.alpha += self.step2
		self.fade.set_alpha(self.alpha)
		screen.blit(self.fade, pygame.Rect(0, 0, 0, 0))

	def update(self, screenx, screeny):
		self.__init__(self.step, self.max_alpha, screenx, screeny)


class menu():

	def __init__(self, menu_name, fade_step, fade_step2, fade_max,
			variables, externals):
		"""main menu"""

		#import variables
		self.screenx, self.screeny = screen.get_size()
		self.screen = screen
		self.fade_step = fade_step
		self.fade_max = fade_max
		self.variables = variables
		self.externals = externals
		self.menu_name = menu_name
		self.fade_step2 = fade_step2

		#set mouse visible
		pygame.mouse.set_visible(True)

		#create menu
		self.menu = creator.create_menu(
					"./assets/templates/" + self.menu_name + ".menu",
					self.variables, pygame.Rect((0, 0), (self.screenx, self.screeny)))

		#create fade effect
		fade = fade_screen(self.fade_step, self.fade_step2, self.fade_max,
				self.screenx, self.screeny)
		self.menu.elems["externals"] = [fade]

		for elem in self.externals:
			self.menu.elems["externals"].insert(0, elem)

	def run(self):

		events = pygame.event.get()
		self.menu.blit(self.screen, events)

		for event in events:
			if event.type == QUIT:
				pygame.mouse.set_visible(False)
				return(["event.EXIT"])
			if event.type == KEYDOWN:
				key = pygame.key.name(event.key)
				if key == "escape":
					pygame.mouse.set_visible(False)
					return(["event.EXIT"])
				if key == "return":
					pygame.mouse.set_visible(False)
					return(["event.CONTINUE"])
			if event.type == USEREVENT and event.code == "MENU":
				names = []
				klicked = self.menu.get_klicked()
				for elem in klicked:
					elem.klicked = False
					names.append(elem.name)
				return names
		return([])

	def update(self):
		for external in self.externals:
			external.update(settings.screenx_current, settings.screeny_current)
		self.__init__(self.menu_name, self.fade_step, self.fade_step2, self.fade_max,
				self.variables, self.externals)

#design = creator.create_outline("./assets/templates/nr1.design")
#design.create_box(0, 0, 200, 40)

men = menu("world", 0, 255, 255, {"savename": "This funny savegame",
				"image1": "./assets/sprites/logo.tif",
				"image2": "./assets/sprites/logo.png",
				"image3": "./assets/sprites/station1.tif",
				"image4": "./assets/sprites/bar1.tif",
				"image5": "./assets/sprites/inputbox1.tif",
				"image6": "./assets/sprites/inputbox2.tif",
				"image7": "./assets/sprites/mine_on.tif",
				"image8": "./assets/sprites/mine_off.tif"}, {})
#men.menu.elems["surfs"]["test"] = [design.box, pygame.Rect(0, 0, 0, 0)]
run = True
while run:
	events = men.run()
	for event in events:
		pygame.time.wait(100)
		if event in ["event.EXIT", "Exit"]:
			run = False
	pygame.display.flip()