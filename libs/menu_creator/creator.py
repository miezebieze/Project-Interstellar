# -*- coding: utf-8 -*-
import pygame
import disp_elem


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
					if var[0] == "#":
						#self.vars[var[1:]] = pygame.image.load(elem)
						self.vars[var[1:]] = elem
					if var[0] == "~":
						self.vars[var[1:]] = float(elem)
					if var[0] == "\"":
						self.vars[var[1:]] = elem
					if var[0] == "*":
						self.vars[var[1:]] = (int(elem[:elem.index(",")]),
								int(elem[elem.index(",") + 1:]
									[:(elem[elem.index(",") + 1:]).index(",")]),
								int(elem[5:][elem[5:].index(",") + 1:]))
					if var[0] == "%":
						self.vars[var[1:]] = float(elem) / 100.0
				if line[0] == "@":
					line = line[2:]

					text = (line[:line.index("|")]).rstrip()
					if text[0] == "$":
						text = self.vars[text[1:]]

					line = line[line.index("|") + 1:]
					if line[0] == "$":
						size = self.vars[line[1: line.index("|")]]
					else:
						size = float(line[1: line.index("|")])

					line = line[line.index("|") + 1:]
					if line[0] == "$":
						typeface = self.vars[line[1: line.index("|")]].rstrip()
					else:
						typeface = line[1: line.index("|")].rstrip()

					line = line[line.index("|") + 1:]
					if line[0] == "$":
						color = self.vars[line[1: line.index("|")]]
					else:
						color = (int(line[:line.index(",")]),
								int(line[line.index(",") + 1:]
									[:(line[line.index(",") + 1:]).index(",")]),
								int(line[5:][line[5:].index(",") + 1: line[5:].index("|")]))

					line = line[line.index("|") + 1:]
					if line[0] == "$":
						img = self.vars[line[1: line.index("|")]]
					else:
						img = line[1: line.index("|")].rstrip()

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

		if "background" in self.vars:
			self.elem = [pygame.transform.smoothscale(
					pygame.image.load(self.vars["background"]),
					ref.size)]
		self.elem.append(disp_elem.button(rel_x, rel_y, ref,
				text, typeface, color, img))


pygame.init()
screen = pygame.display.set_mode((int(1920 / 2.0), int(1080 / 2.0)))

men = create_menu("./test1.menu", screen.get_rect())
print men.vars
while True:
	for elem in men.elem:
		if type(elem) == pygame.Surface:
			screen.blit(elem, elem.get_rect())
		else:
			elem.blit(screen)
		pygame.display.flip()