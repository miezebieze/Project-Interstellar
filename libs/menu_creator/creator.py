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
		self.elems = []

		with open(filename) as conf_file:
			for line in conf_file:
				line = line.rstrip("\n")
				if len(line) < 1 or line[0] == "/":
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
					if var[0] == "[":
						self.vars[var[1:]] = convert2list(elem)

				if line[0] == "@":
					line = line[2:]

					text = (line[:line.index("|")]).strip()
					if text[0] == "$":
						text = self.vars[text[1:]]

					line = line[line.index("|") + 1:].lstrip()
					if line.strip()[0] == "$":
						maxsize = self.vars[line[1: line.index("|")].strip()]
					else:
						maxsize = float(line[: line.index("|")].strip())

					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						typeface = self.vars[line[1: line.index("|")].strip()]
					else:
						typeface = line[: line.index("|")].strip()

					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						color = self.vars[line[1: line.index("|")].strip()]
					else:
						color = []
						for elem in convert2list(line[:line.index("|")].rstrip()):
							color.append(int(elem))

					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						img = self.vars[line[1: line.index("|")].strip()]
					else:
						print("Error: Outline only accepts only variables")
						quit()

					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						rel_x = self.vars[line[1: line.index("|")].strip()]
					else:
						if line[0] == "%":
							rel_x = float(line[1:line.index("|")]) / 100
						else:
							rel_x = int(line[: line.index("|")])

					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						rel_y = self.vars[line[1: line.index("|")].strip()]
					else:
						if line[1] == "%":
							rel_y = float(line[1:line.index("|")]) / 100
						else:
							rel_y = int(line[: line.index("|")])

					self.elems.append(disp_elem.button(rel_x, rel_y, ref,
							text, typeface, maxsize, color, img[:3], int(img[3])))

				if line[0] == "-":
					line = line[2:]

					text = (line[:line.index("|")]).strip()
					if text[0] == "$":
						text = self.vars[text[1:]]

					if line.count("|") == 8:
						line = line[line.index("|") + 1:].lstrip()
						if line[0] == "$":
							options = self.vars[line[1: line.index("|")].strip()]
						else:
							options = line[: line.index("|")].strip()
					else:
						options = False

					line = line[line.index("|") + 1:].lstrip()
					if line.strip()[0] == "$":
						maxsize = int(self.vars[line[1: line.index("|")].strip()])
					else:
						maxsize = int(line[: line.index("|")].strip())

					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						typeface = self.vars[line[1: line.index("|")].strip()]
					else:
						typeface = line[: line.index("|")].strip()

					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						color = self.vars[line[1: line.index("|")].strip()]
					else:
						color = []
						for elem in convert2list(line[:line.index("|")]):
							color.append(int(elem))

					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						img = self.vars[line[1: line.index("|")].strip()]
					else:
						print("Error: Outline only accepts only variables")
						quit()

					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						rel_x = self.vars[line[1: line.index("|")].strip()]
					else:
						if line[0] == "%":
							rel_x = float(line[1:line.index("|")]) / 100
						else:
							rel_x = int(line[0: line.index("|")])

					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						rel_y = self.vars[line[1: line.index("|")].strip()]
					else:
						if line[0] == "%":
							rel_y = float(line[1:line.index("|")]) / 100
						else:
							rel_y = int(line[: line.index("|")])

					self.elems.append(disp_elem.sliders(text, maxsize, typeface,
							color, img, rel_x, rel_y, ref,
							options))

		if "background" in self.vars:
			self.elems.append(pygame.transform.smoothscale(
					pygame.image.load(self.vars["background"][0]),
					ref.size))
		self.elems = self.elems[::-1]

	def get_klicked(self):
		klicked = []
		for elem in self.elems:
			if isinstance(elem, disp_elem.button):
				if elem.klicked:
					klicked.append(elem)
		return klicked

	def get_elem(self, name):
		for elem in self.elems:
			if type(elem) != pygame.Surface:
				if elem.name == name:
					return elem