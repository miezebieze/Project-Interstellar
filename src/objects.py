# -*- coding: utf-8 -*-
import pygame
import random
import math
from . import settings
from pygame.locals import *

"""Classes for creating objects"""


class stars():

	def __init__(self):
		"""creates a new star"""

		screenx = settings.screenx_current
		screeny = settings.screeny_current

		self.image = pygame.image.load("./assets/sprites/star1.tif")
		imgsize = self.image.get_width()

		#random size between 0 and 100 %
		self.size = random.randint(0, 100) / 100.0
		minimum = 0.15
		maximum = 0.70
		#determing the depth of the star
		self.depth = (self.size * (maximum - minimum)
				) + minimum  # value mapped between .15 and .70
		self.image = pygame.transform.smoothscale(self.image,
						(int(imgsize * self.depth), int(imgsize * self.depth)))

		self.pos = self.image.get_rect()
		self.screenx = screenx - self.pos.w
		self.screeny = screeny - self.pos.h
		#gives a percentage where star is located
		relative_x = random.randint(-100, int(100 * (self.depth))) / 100.0
		relative_y = random.randint(-100, int(100 * (self.depth))) / 100.0
		#calculates pixel position
		self.pointx = relative_x * self.screenx
		self.pointy = relative_y * self.screeny

	def move(self, x, y):
		"""Moves the star according to player position"""
		#note: x and y are the player position
		#and that screenx and screeny are not actual screen width and height
		self.pos.left = ((self.screenx - x) * self.depth) - self.pointx
		self.pos.top = ((self.screeny - y) * self.depth) - self.pointy

	def blitstar(self):
		"""blits the star"""
		screeny = settings.screeny_current
		screenx = settings.screenx_current

		if 0 < self.pos.top < screeny and 0 < self.pos.left < screenx:
			settings.screen.blit(self.image, self.pos)
			return True
		return False

	def resize(self, ratio):
		"""Resizes star fitting to resolution"""
		size = int(self.size * (ratio / 2.0))
		if size > 5:
			self.image = pygame.image.load("./assets/sprites/star1.tif")
			self.image = pygame.transform.smoothscale(self.image, (size, size))
			self.pos = self.image.get_rect()


class button():

	def __init__(self, x, y, text, color):
		"""Initalises with x and y as center point"""
		#basic font and then everything should be clear
		#and the self.pos.move line basicly move its center to y and x
		#going to be simplified next refactoring
		self.button = settings.button
		self.pos = settings.button.get_rect()
		self.pos = self.pos.move(x - (self.pos.w / 2.0), y - (self.pos.h / 2.0))
		self.text = settings.modrender(settings.typeface, 30,
			text, True, color,
			self.pos.size, 6)
		self.textpos = self.text.get_rect()
		self.textpos.center = self.pos.center
		self.klicked = False

	def changetext(self, text, color):
		"""Changes the text inside the button"""
		self.text = settings.modrender(settings.typeface, 30,
			text, True, color,
			self.pos.size, 6)
		self.textpos = self.text.get_rect()
		self.textpos.center = self.pos.center

	def move(self, x, y):
		"""Moves the button so that x and y are the center"""
		self.button = settings.button
		self.pos = settings.button.get_rect()
		self.pos = self.pos.move(x - (self.pos.w / 2.0), y - (self.pos.h / 2.0))
		self.textpos = self.text.get_rect()
		self.textpos.center = self.pos.center

	def blit(self):
		"""Blits the button"""
		#blitts the button and changes image when hovered over or being clicked
		#also posts a menu event to show that a button has been clicked
		#to increase performance should be easy to understand
		screen = settings.screen
		self.klicked = False
		if self.pos.collidepoint(pygame.mouse.get_pos()):
			self.button = settings.buttonover
			screen.blit(self.button, self.pos)
			for event in settings.events:
				if event.type == MOUSEBUTTONDOWN and event.button == 1:
					self.button = settings.buttonclick
					screen.blit(self.button, self.pos)
					menue = pygame.event.Event(USEREVENT, code="MENU")
					pygame.fastevent.post(menue)
					self.klicked = True
		else:
			self.button = settings.button
			screen.blit(self.button, self.pos)

		screen.blit(self.text, self.textpos)


class inputfield():

	def __init__(self, x, y, typ, text, color):
		"""Creates a new inputfield"""
		self.font = pygame.font.SysFont(settings.typeface, 30)
		self.header = text
		if typ == 1:
			self.field = settings.field
		elif typ == 2:
			self.field = settings.field1
		self.pos = settings.field.get_rect()
		self.pos = self.pos.move(x - (self.pos.w / 2.0), y - (self.pos.h / 2.0))
		self.text = ""
		self.render_text = settings.modrender(settings.typeface, 30, self.text,
			True, color,
			self.pos.size, 9)
		self.textpos = self.render_text.get_rect()
		self.textpos.center = self.pos.center
		self.render_header = settings.modrender(settings.typeface, 30, self.header,
			True, color,
			settings.screen.get_rect().size, 0)
		self.headerpos = self.render_header.get_rect()
		self.headerpos.center = self.pos.center
		self.headerpos.y -= 50

	def gettext(self):
		"""Returns text if return is pressed or removes one if return is pressed"""
		from . import interface
		key = interface.getall(False)
		if key is not None and self.textpos.width < self.pos.width - 18:
			self.text = self.text + key
		if key is None:
			key = interface.getall(True)
			if key == "return":
				return self.text
			if key == "backspace":
				self.text = self.text[:len(self.text) - 1]

	def blit(self):
		"""Blits the inputfield"""
		color = settings.color
		screen = settings.screen
		self.render_text = settings.modrender(settings.typeface, 30, self.text,
			True, color,
			self.pos.size, 9)
		self.textpos = self.render_text.get_rect()
		self.textpos.center = self.pos.center
		screen.blit(self.render_header, self.headerpos)
		screen.blit(self.field, self.pos)
		screen.blit(self.render_text, self.textpos)


class sliders():

	def __init__(self, value, x, y):
		"""Creates a new slider"""
		self.value = value
		self.box = settings.box
		self.knob = settings.knob
		self.pos = self.box.get_rect()
		self.knob_pos = self.knob.get_rect()
		self.pos.top = y - (self.pos.h / 2.0)
		self.pos.left = x - (self.pos.w / 2.0)
		self.knob_pos.top = self.pos.top
		self.knob_pos.left = self.pos.left + (self.pos.w * value)
		self.scale = 1.0 / self.pos.w
		self.dragged = False

	def modify(self, events):
		"""Modifies the slider (e.g. pos)"""
		for event in events:
			if event.type == MOUSEBUTTONUP:
				if event.button == 1:
					self.dragged = False
			if event.type == MOUSEBUTTONDOWN:
					if self.pos.collidepoint(pygame.mouse.get_pos()):
						if event.button == 1:
							self.dragged = True
			if self.dragged:
				self.value = (pygame.mouse.get_pos()[0] - self.pos.left) * self.scale

		if self.value < 0:
			self.value = 0
		if self.value > 1:
			self.value = 1

		if self.value <= 0.01:
			self.value = 0.0
		if self.value >= 0.995:
			self.value = 1.0
		tmp = (self.value * (self.pos.w - self.knob_pos.w))
		self.knob_pos.left = self.pos.left + tmp

	def blit(self, name):
		"""Blits the slider"""
		screen = settings.screen
		tmp = name + "{0:.2f}".format(self.value) + "%"
		tmp = tmp.replace("0.0", "").replace("0.", "").replace(".", "")
		self.render_text = settings.modrender(settings.typeface, 30,
			tmp, True, settings.color,
			self.pos.size, 6)
		self.textpos = self.render_text.get_rect()
		self.textpos.center = self.pos.center

		screen.blit(self.box, self.pos)
		screen.blit(self.knob, self.knob_pos)
		screen.blit(self.render_text, self.textpos)


class bullet():

	def __init__(self, x, y, angle, refrence):
		"""Creates new bullet"""
		self.start = (x, y)
		self.image = settings.bullet_img
		self.pos = self.image.get_rect()
		half_img = int(refrence.w / 2.0)
		self.pos_left = half_img - int(self.pos.w / 2.0)
		self.pos_top = half_img - int(self.pos.h / 2.0)
		self.pos = self.pos.move(x, y)
		self.__angle = angle
		self.__add_speedx = (settings.speed / 40) + 1
		self.__add_speedy = (settings.speed / 40) + 1
		self.__move_x = 0.15 * math.degrees(math.sin((math.radians(self.__angle))))
		self.__move_y = -0.15 * math.degrees(math.cos((math.radians(self.__angle))))
		self.__move_x *= self.__add_speedx + 0.1
		self.__move_y *= self.__add_speedy + 0.1
		self.inscreen = True
		self.move(settings.player_pos)

	def move(self, player_pos):
		"""Moves the bullet"""
		self.pos.topleft = (0, 0)
		self.pos_left += self.__move_x
		self.pos_top += self.__move_y
		tmpx = self.start[0] + self.pos_left + (self.start[0] - player_pos[0])
		tmpy = self.start[1] + self.pos_top + (self.start[1] - player_pos[1])
		self.pos = self.pos.move(tmpx, tmpy)
		if not self.pos.colliderect(settings.screen.get_rect()):
			self.inscreen = False

	def blit(self):
		"""Blits the bullet"""
		screeny = settings.screeny_current
		screenx = settings.screenx_current

		if 0 < self.pos.top < screeny and 0 < self.pos.left < screenx:
			settings.screen.blit(self.image, self.pos)
			return True
		return False


class target():

	def __init__(self):
		"""Creates new random target"""
		self.image = settings.targeton_img
		self.chooser = True
		self.pos = self.image.get_rect()
		self.pos_xper = random.randint(0, 10000) / 10000.0
		self.pos_yper = random.randint(0, 10000) / 10000.0
		self.pos_x = self.pos_xper * settings.world.background_pos.w - 20 - self.pos.w
		self.pos_y = self.pos_yper * settings.world.background_pos.h - 20 - self.pos.h
		if self.pos_x < 20:
			self.pos_x += 40 + 2 * self.pos.w
		if self.pos_y < 20:
			self.pos_y += 40 + 2 * self.pos.h
		self.timer = random.randint(0, 1000)
		self.gothit = False
		random_explosion = random.randint(0, len(settings.explosions) - 1)
		self.explosion = settings.explosions[random_explosion]
		self.movex = int(self.explosion.getRect().w / 2.0)
		self.movey = int(self.explosion.getRect().h / 2.0) - 5
		self.kill_entity = False
		self.inscreen = True
		self.move(settings.player_pos.x, settings.player_pos.y)

	def update(self):
		"""Adjusts position according to screen size"""
		self.pos_x = self.pos_xper * settings.screenx_current * 2 - 20 - self.pos.w
		self.pos_y = self.pos_yper * settings.screeny_current * 2 - 20 - self.pos.h

	def move(self, x, y):
		"""Moves rect according to playerposition"""
		newtime = pygame.time.get_ticks()
		if newtime > self.timer:
			while newtime > self.timer:
				self.timer += 1000
			self.chooser = settings.toggle(self.chooser, True, False)
			if self.chooser:
				self.image = settings.targeton_img
			elif not self.chooser:
				self.image = settings.targetoff_img
		if self.pos.colliderect(settings.screen.get_rect()):
			self.inscreen = True
		else:
			self.inscreen = False

		self.pos.left = self.pos_x - x
		self.pos.top = self.pos_y - y

	def test_ishit(self, bulletrect):
		"""Tests if target got hit"""
		if self.pos.colliderect(bulletrect) and not self.gothit:
			self.pos_x -= self.movex
			self.pos_y -= self.movey
			self.explosion.play()
			self.gothit = True

	def blit(self):
		"""Blits target and explosion"""
		if self.gothit:
			anfin = self.explosion.state == "stopped" or self.explosion.state == "paused"
			if self.explosion.isFinished() or anfin:
				self.kill_entity = True
			elif not self.kill_entity:
				self.explosion.blit(settings.screen, self.pos)

		else:
			if self.inscreen:
				settings.screen.blit(self.image, self.pos)