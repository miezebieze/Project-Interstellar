import pygame
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((300, 300))

pos = pygame.Rect(100, 100, 100, 100)
pygame.draw.rect(screen, (255, 255, 255), pos, 0)

while True:

	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
		if event.type == KEYDOWN:
			key = pygame.key.name(event.key)
			print key

	pygame.display.flip()
	pass