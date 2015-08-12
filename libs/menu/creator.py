# -*- coding: utf-8 -*-
import pygame
import disp_elem
from disp_elem import button
from disp_elem import slider
#button and sliders would be unsued
button
slider


def convert2list(string):
	num_of_elem = string.count(",") + 1
	elements = []
	string = string[1:]
	for a in range(num_of_elem - 1):
		elements.append(string[:string.index(",")].strip())
		string = string[string.index(",") + 1:].strip()
	elements.append(string[:-1])
	return elements


def analyse_num(string, variables):
	string = string.strip()
	lstring = string[:string.index("+")].rstrip()
	rstring = string[string.index("+") + 1:].lstrip()
	if lstring[0] == "%":
		rel = int(lstring[1:]) / 100.0
	elif lstring[0] == "$":
		if variables[lstring[1:]] < 1.0001 and type(variables[lstring[1:]]) == float:
			rel = variables[lstring[1:]]
		else:
			absol = variables[lstring[1:]]
	else:
		absol = int(lstring)

	if rstring[0] == "%":
		rel = int(rstring[1:]) / 100.0
	elif rstring[0] == "$":
		if variables[rstring[1:]] < 1.0001 and type(variables[rstring[1:]]) == float:
			rel = variables[rstring[1:]]
		else:
			absol = variables[rstring[1:]]
	else:
		absol = int(rstring)

	return rel, absol


class create_menu():

	def __init__(self, filename, variables, ref):
		self.vars = variables
		self.elems = {"buttons": [], "sliders": [], "surfs": {}}

		with open(filename) as conf_file:
			for line in conf_file:
				line = line.rstrip("\n")
				if len(line) < 1 or line[0] == "/":
					continue

				if line[0] == "&":
					file2 = line[1:]
					self.vars.update(create_menu(file2, {}, pygame.Rect(1, 1, 1, 1)).vars)
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

				if line[0] == "#":
					line = line[2:]
					text = (line[:line.index("|")]).strip()
					if text[0] == "$":
						text = self.vars[text[1:]]

					line = line[line.index("|") + 1:].lstrip()
					if line.strip()[0] == "$":
						img = self.vars[line[1: line.index("|")].strip()]
					else:
						print("Pictures only accept variables as image source")
						quit()

					line = line[line.index("|") + 1:].lstrip()
					rel_x, abs_x = analyse_num(line[0: line.index("|")].strip(), self.vars)

					line = line[line.index("|") + 1:-1].lstrip()
					rel_y, abs_y = analyse_num(line, self.vars)

					self.elems["surfs"][text] = [pygame.image.load(img[0]),
								pygame.Rect(
									(
										(ref.w * rel_x) + abs_x,
										(ref.h * rel_y) + abs_y,
									),
									(
										0,
										0
									)
									)]

				if line[0] == "*":
					line = line[2:]

					text = (line[:line.index("|")]).strip()
					if text[0] == "$":
						text = self.vars[text[1:]]

					line = line[line.index("|") + 1:].lstrip()
					if line.strip()[0] == "$":
						size = int(self.vars[line[1: line.index("|")].strip()])
					else:
						size = int(line[: line.index("|")].strip())

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
					rel_x, abs_x = analyse_num(line[0: line.index("|")].strip(), self.vars)

					line = line[line.index("|") + 1:-1].lstrip()
					rel_y, abs_y = analyse_num(line, self.vars)

					antialias = True

					img = pygame.font.SysFont(typeface, size).render(text, antialias, color)

					half_sizex = int(img.get_size()[0] / 2.0)
					half_sizey = int(img.get_size()[1] / 2.0)

					xpos = (ref.w * rel_x) + abs_x - half_sizex
					ypos = (ref.h * rel_y) + abs_y - half_sizey

					pos = pygame.Rect((xpos, ypos), (0, 0))

					self.elems["surfs"][text] = [img, pos]

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
					rel_x, abs_x = analyse_num(line[0: line.index("|")].strip(), self.vars)

					line = line[line.index("|") + 1:-1].lstrip()
					rel_y, abs_y = analyse_num(line, self.vars)

					self.elems["buttons"].append(disp_elem.button(rel_x, abs_x, rel_y, abs_y,
									ref, text, typeface, maxsize, color, img[:3],
									int(img[3])))

				if line[0] == "-":
					line = line[2:]

					text = (line[:line.index("|")]).strip()
					if text[0] == "$":
						text = self.vars[text[1:]]

					if line.count("|") == 9:
						line = line[line.index("|") + 1:].lstrip()
						if line[0] == "$":
							options = self.vars[line[1: line.index("|")].strip()]
						else:
							print("The options argument for sliders only accepts variables.")
							quit()

						line = line[line.index("|") + 1:].lstrip()
						if line.strip()[0] == "$":
							default_value = float(self.vars[
										line[1: line.index("|")].strip()
									]) / len(options)
							default_value += 0.5 / len(options)
						else:
							if (float(line[: line.index("|")].strip())
								== int(line[: line.index("|")].strip())):
									selected = float(line[: line.index("|")].strip())
									default_value = float(selected) / len(options)
									default_value += 0.5 / len(options)

					else:
						options = False
						line = line[line.index("|") + 1:].lstrip()
						if line.strip()[0] == "$":
							default_value = float(self.vars[line[1: line.index("|")].strip()])
						else:
							default_value = float(line[: line.index("|")].strip())

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
					rel_x, abs_x = analyse_num(line[0: line.index("|")].strip(), self.vars)

					line = line[line.index("|") + 1:-1].lstrip()
					rel_y, abs_y = analyse_num(line, self.vars)

					self.elems["sliders"].append(disp_elem.slider(text, default_value,
								maxsize, typeface, color, img,
								rel_x, abs_x, rel_y, abs_y, ref, options))

		if "background" in self.vars:
			self.elems["surfs"]["background"] = [pygame.transform.smoothscale(
					pygame.image.load(self.vars["background"][0]),
					ref.size), pygame.Rect(0, 0, 0, 0)]

	def blit(self, screen, events):
		try:
			screen.blit(self.elems["surfs"]["background"][0],
				self.elems["surfs"]["background"][1])
		except:
			pass
		try:
			for external in self.elems["externals"]:
				external.blit(screen)
		except:
			pass
		for surf in self.elems["surfs"]:
			if surf != "background":
				screen.blit(self.elems["surfs"][surf][0], self.elems["surfs"][surf][1])
		for elem in self.elems["buttons"] + self.elems["sliders"]:
			elem.update(events)
			elem.blit(screen)

	def get_klicked(self):
		klicked = []
		for elem in self.elems["buttons"]:
			if elem.klicked:
				klicked.append(elem)
		return klicked

	def get_elem(self, name):
		for elem in self.elems:
			if type(elem) != pygame.Surface:
				if elem.name == name:
					return elem