# -*- coding: utf-8 -*-
#Impossible

import pygame


class test():

	def __init__(self):
		self.img = pygame.Surface((20, 20))
		self.img.fill((255, 255, 255))

	def __repr__(self):
		return self.img

	def __call__(self):
		return self.img
a = test()

pygame.init()
screen = pygame.display.set_mode((50, 50))
screen.blit(a())