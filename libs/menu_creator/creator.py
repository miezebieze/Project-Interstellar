# -*- coding: utf-8 -*-
import pygame
import disp_elem


def convert2list(string):
	num_of_elem = string.count(",") + 1
	elements = []
	string = string[1:]
	for a in range(num_of_elem - 1):
		elements.append(string[:string.index(",")])
		string = string[string.index(",") + 1:]
	elements.append(string[:-1])
	return elements


class create_menu():

	def __init__(self, filename, ref):
		self.vars = {}
		self.elem = []

		with open(filename) as conf_file:
			for line in conf_file:
				line = line.rstrip("\n")
				if len(line) < 1:
					continue
				if line[0] == "<":
					var = line[1:line.index(" ")]
					elem = line[line.index("=") + 2:]
					if var[0] == "\"":
						self.vars[var[1:]] = elem
					if var[0] == "~":
						self.vars[var[1:]] = float(elem)
					if var[0] == "#":
						elems = convert2list(elem)
						try:
							elems[len(elems) - 1] = int(elems[len(elems) - 1])
							if len(elems) == 2:
								elems.insert(0, elems[0])
								elems.insert(0, elems[0])
							if len(elems) == 3:
								elems.insert(2, elems[1])
						except:
							if len(elems) == 1:
								elems.append(elems[0])
								elems.append(elems[0])
								elems.append(0)
							if len(elems) == 2:
								elems.append(elems[1])
								elems.append(0)
							if len(elems) == 3:
								elems.append(0)
						self.vars[var[1:]] = elems
					if var[0] == "*":
						self.vars[var[1:]] = []
						for numelem in convert2list(elem):
							self.vars[var[1:]].append(int(numelem))
					if var[0] == "%":
						self.vars[var[1:]] = float(elem) / 100.0
				if line[0] == "@":
					line = line[2:]

					text = (line[:line.index("|")]).rstrip()
					if text[0] == "$":
						text = self.vars[text[1:]]

					line = line[line.index("|") + 1:]
					if line[0] == "$":
						maxsize = self.vars[line[1: line.index("|")]]
					else:
						maxsize = float(line[1: line.index("|")])

					line = line[line.index("|") + 1:]
					if line[0] == "$":
						typeface = self.vars[line[1: line.index("|")]].rstrip()
					else:
						typeface = line[1: line.index("|")].rstrip()

					line = line[line.index("|") + 1:]
					if line[0] == "$":
						color = self.vars[line[1: line.index("|")]]
					else:
						color = []
						for elem in convert2list(line[:line.index("|")]):
							color.append[int(elem)]

					line = line[line.index("|") + 1:]
					if line[0] == "$":
						img = self.vars[line[1: line.index("|")]]
					else:
						print("Error: Outline only accepts only variables")
						print(("In line " + str(conf_file.index(line))))
						quit()

					line = line[line.index("|") + 1:]
					if line[0] == "$":
						rel_x = self.vars[line[1: line.index("|")]]
					else:
						if line[1] == "%":
							rel_x = float(line[3:line.index("|") - 1]) / 100
						else:
							rel_x = int(line[0: line.index("|")])

					line = line[line.index("|") + 1:]
					if line[0] == "$":
						rel_y = self.vars[line[1: line.index("|")]]
					else:
						if line[1] == "%":
							rel_y = float(line[3:line.index("|") - 1]) / 100
						else:
							rel_y = int(line[0: line.index("|")])

					self.elem.append(disp_elem.button(rel_x, rel_y, ref,
							text, typeface, maxsize, color, img[:3], int(img[3])))

		if "background" in self.vars:
			self.elem.append(pygame.transform.smoothscale(
					pygame.image.load(self.vars["background"][0]),
					ref.maxsize))
		self.elem = self.elem[::-1]

	def get_klicked(self):
		klicked = []
		for elem in self.elem:
			if isinstance(elem, disp_elem.button):
				if elem.klicked:
					klicked.append(elem)
		return klicked


pygame.init()
pygame.fastevent.init()
screen = pygame.display.set_mode((int(1920 / 2.0), int(1080 / 2.0)))

men = create_menu("./test1.menu", screen.get_rect())
print((men.vars))
print((men.elem))
while True:
	events = pygame.fastevent.get()
	for elem in men.elem:
		if type(elem) == pygame.Surface:
			screen.blit(elem, elem.get_rect())
		elif isinstance(elem, disp_elem.button):
			elem.blit(screen, events)

	for event in events:
		if event.type == pygame.locals.USEREVENT and event.code == "MENU":
			for elem in men.get_klicked():
				if elem.text == "Exit":
					quit()

	pygame.display.flip()