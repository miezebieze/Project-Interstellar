import pygame

pygame.init()

iterations = 100000

timestart = pygame.time.get_ticks()

for a in range(iterations):
	pygame.time.delay(0)

timeold = pygame.time.get_ticks()
timeperloop1 = (timeold - timestart) / float(iterations)


timestart = pygame.time.get_ticks()

for a in range(iterations):
	pygame.time.delay(1)

timeold = pygame.time.get_ticks()
timeperloop2 = (timeold - timestart) / float(iterations)

print timeperloop2 - timeperloop1

#pygame.time.delay - pass = 0.000106
#pygame.time.delay(0) - pygame.time.delay(1) - 1 = 0.01313 (100000)
#pygame.time.delay(10) - pygame.time.delay(11) - 1 = 0.09928 (10000)
#pygame.time.delay(50) - pygame.time.delay(51) - 1 = 0.0997 (1000)
#pygame.time.delay(100) - pygame.time.delay(101) - 1 = 0.08 (500)
#pygame.time.delay(1000) - pygame.time.delay(1001) - 1 = 0.016667 (60)