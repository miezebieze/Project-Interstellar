	# lint:ok
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *


def modrender(typeface, size, text, antialias, color, maxsize, borderoff):
	#local typeface!
	nofit = True
	while nofit:
		tmpfont = pygame.font.SysFont(typeface, size)
		bool1 = tmpfont.size(text)[0] < maxsize[0] - (2 * borderoff)
		nofit = not (bool1 and tmpfont.size(text)[1] < maxsize[1] - (2 * borderoff))
		if size <= 5:
			nofit = False
		else:
			size -= 1
	return tmpfont.render(text, antialias, color)


def getmaxsize(typeface, size, text, antialias, color, maxsize, borderoff):
	#local typeface!
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


class button():

	#TODO: Add rel x + y
	def __init__(self, rel_x, x, rel_y, y, ref, text, typeface, size,
			color, buttons_files, borderoff):
		"""Initalises with x and y as center point"""
		#basic font and then everything should be clear
		#going to be simplified next refactoring
		self.buttons = (pygame.image.load(buttons_files[0]),
				pygame.image.load(buttons_files[1]),
				pygame.image.load(buttons_files[2]))
		self.pos = self.buttons[0].get_rect()
		self.x = x
		self.y = y
		self.rel_x = rel_x
		self.rel_y = rel_y
		self.typeface = typeface
		self.text = text
		self.name = text
		self.text_img = modrender(typeface, 30,
			text, True, color,
			self.pos.size, borderoff)
		self.textpos = self.text_img.get_rect()
		self.textpos.center = self.pos.center
		self.klicked = False
		self.move(self.x, self.rel_x, self.y, self.rel_y, ref)

	def changetext(self, text, color):
		"""Changes the text inside the button"""
		self.text_img = modrender(self.typeface, 30,
			text, True, color,
			self.pos.size, 6)
		self.textpos = self.text_img.get_rect()
		self.textpos.center = self.pos.center

	def move(self, x, rel_x, y, rel_y, ref):
		"""Moves the button so that x and y are the center"""
		self.pos = self.buttons[0].get_rect()
		rel_x *= float(ref.w)
		rel_y *= float(ref.h)
		x += rel_x
		y += rel_y
		self.pos = self.pos.move(x - (self.pos.w / 2.0), y - (self.pos.h / 2.0))
		self.textpos = self.text_img.get_rect()
		self.textpos.center = self.pos.center

	def blit(self, screen, events):
		"""Blits the button"""
		#blitts the button and changes image when hovered over or being clicked
		#also posts a menu event to show that a button has been clicked
		#to increase performance should be easy to understand
		if self.pos.collidepoint(pygame.mouse.get_pos()) and not self.klicked:
			screen.blit(self.buttons[1], self.pos)
			for event in events:
				if event.type == MOUSEBUTTONDOWN and event.button == 1:
					menue = pygame.event.Event(USEREVENT, code="MENU")
					pygame.fastevent.post(menue)
					self.klicked = True
					screen.blit(self.buttons[2], self.pos)
		elif not self.klicked:
			screen.blit(self.buttons[0], self.pos)
		else:
			screen.blit(self.buttons[2], self.pos)

		screen.blit(self.text_img, self.textpos)


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

	def __init__(self, name, size, typeface, color, box,
		rel_x, x, rel_y, y, ref, options_list=False):
		"""Creates a new slider"""
		self.value = 0.0
		self.box = pygame.image.load(box[0])
		self.knob = pygame.image.load(box[1])
		self.knob_pos = self.knob.get_rect()
		self.dragged = False
		self.typeface = typeface
		self.color = color
		self.options_list = options_list
		self.name = name
		self.size = size
		self.borderoff = box[3]

		self.pos = self.box.get_rect()
		rel_x *= float(ref.w)
		rel_y *= float(ref.h)
		x += rel_x
		y += rel_y
		self.pos = self.pos.move(x - (self.pos.w / 2.0), y - (self.pos.h / 2.0))
		self.knob_pos.top = self.pos.top
		self.knob_pos.left = self.pos.left + (self.pos.w * self.value)
		self.scale = 1.0 / self.pos.w

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
			self.value = 1.0000000001
		tmp = (self.value * (self.pos.w - self.knob_pos.w))
		self.knob_pos.left = self.pos.left + tmp

	def blit(self, screen, events):
		#( name, options_list=False):
		"""Blits the slider"""
		self.modify(events)
		if type(self.options_list) == bool:
			tmp = self.name + ": " + str(self.value)[:4] + "%"
			tmp = tmp.replace("0.0", "0").replace("0.", "").replace(".", "")
			self.render_text = modrender(self.typeface, self.size,
				tmp, True, self.color,
				self.pos.size, self.borderoff)
		else:
			steps = 1.0 / len(self.options_list)
			for area in range(len(self.options_list)):
				area += 1
				if self.value <= steps * area and self.value >= steps * (area - 1):
					item = self.options_list[area - 1]
					break
			text = self.name + ": " + item
			self.render_text = modrender(self.typeface, 30,
				text, True, self.color,
				self.pos.size, 6)
		self.textpos = self.render_text.get_rect()
		self.textpos.center = self.pos.center
		screen.blit(self.box, self.pos)
		screen.blit(self.knob, self.knob_pos)
		screen.blit(self.render_text, self.textpos)