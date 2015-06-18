# -*- coding: utf-8 -*-
import pygame
import string
from pygame.locals import *

pygame.init()

pygame.display.set_mode((100, 100))

b = True

while b:
	a = pygame.event.wait()
	if a.type == KEYDOWN:
		key = pygame.key.name(a.key)
		if key == "escape":
			exit()
	if a.type == KEYDOWN:
		if a.unicode in string.printable:
			print pygame.key.name(a.key)
	if a.type == MOUSEBUTTONDOWN:
		print a.button
		#print