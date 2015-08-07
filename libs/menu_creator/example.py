import creator
import pygame
from creator import disp_elem

#initialize engine ad create window
pygame.init()
pygame.fastevent.init()
screen = pygame.display.set_mode((int(1920 / 2.0), int(1080 / 2.0)))

#read menu config file and print vars and elemens
men = creator.create_menu("./main.menu", screen.get_rect())
print((men.vars))
print((men.elems))
#General loop
while True:

	#Updates and blits the elements
	events = pygame.fastevent.get()
	for elem in men.elems:
		if type(elem) == pygame.Surface:
			screen.blit(elem, elem.get_rect())
		elif isinstance(elem, (disp_elem.button, disp_elem.sliders)):
			elem.blit(screen, events)

	#Prints The value of the slider when Start button has been clicked
	if men.get_elem("Start").klicked:
		value = str((men.get_elem("Volume").value * 100))
		value = value[:value.index(".")]
		print value
		#events havent updated yet so manual reset
		pygame.time.delay(100)
		elem.klicked = False

	#Checks for interaction with elements
	for event in events:
		#This triggers when there has been any interaction
		if event.type == pygame.locals.USEREVENT and event.code == "MENU":
			#iterates through the clicked elemets
			for elem in men.get_klicked():
				#if exit button has been pressed , exit
				if elem.text == "Exit":
					pygame.time.delay(100)
					quit()
				#returns clicked buttons to normal state after 100ms
				pygame.time.delay(100)
				elem.klicked = False

	#updates the diplay
	pygame.display.flip()