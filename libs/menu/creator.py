# -*- coding: utf-8 -*-
import pygame
import disp_elem
from .disp_elem import button
from .disp_elem import slider
from .disp_elem import create_outline
#button and sliders would be unsued
button
slider
create_outline


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

				#This checks for the identation
				ident = 0
				if line[0].isspace():
					for counter in range(len(line)):
						if line[counter].isspace():
							#If true multiple types of
							#whitespace is used in one line
							#as identation
							if line[counter] != line[0]:
								raise SyntaxError("Usage of both tabs and spaces.")
						else:  # First non-whitespace character
							if line[0] == " ":  # Identation is spaces
								#4 spaces = 1 identation
								ident = line[:counter + 1].count(" ") / 4.0
								#print warning when the amount of spaces
								#is not divisible by four
								#(might be the cause for some nasty to find
								#errors)
								if type(ident) != int:
									print(("Warning: Unusual amount of identation: "
										+ str(ident * 4)))
							if line[0] == "	":  # Identation is tabs
								ident = line[:counter + 1].count("	")
							break
					line = line.strip()  # removes whitespace for analysis

				#Here are the diferent types of elements
				#and comments that can be used
				if line[0] == "&":  # An import of existing variables
					file2 = line[1:]
					self.vars.update(create_menu(file2, {}, pygame.Rect(1, 1, 1, 1)).vars)
				if line[0] == "<":  # A variable is defined in language
					var = line[1:line.index(" ")]
					elem = line[line.index("=") + 2:]
					if var[0] == "\"":  # A string variable
						self.vars[var[1:]] = elem
					if var[0] == "~":  # A float variable
						self.vars[var[1:]] = float(elem)
					if var[0] == "#":  # A desing variable
						elems = convert2list(elem)
						#this adds non-existing types
						#(hoverover and klicked)
						#to the desing if they are missing
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
					if var[0] == "*":  # A color variable
						self.vars[var[1:]] = []
						for numelem in convert2list(elem):
							self.vars[var[1:]].append(int(numelem))
					if var[0] == "%":  # A float defenition as percentage
						self.vars[var[1:]] = float(elem) / 100.0
					if var[0] == "[":  # A general list
						self.vars[var[1:]] = convert2list(elem)

				if line[0] == "#":  # An image is defined in language
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

					self.elems["surfs"][text] = [pygame.image.load(img[0]).convert_alpha(),
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

				if line[0] == "*":  # A title is defined in language
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

				if line[0] == "@":  # A button is defined in language
					line = line[2:]

					text = (line[:line.index("|")]).strip()
					if text[0] == "$":
						text = self.vars[text[1:]]
					content = text

					if line.count("|") == 7:
						imagemode = True
						line = line[line.index("|") + 1:].lstrip()
						if line.strip()[0] == "$":
							content = self.vars[line[1: line.index("|")].strip()]
						else:
							content = str(line[: line.index("|")].strip())
					else:
						imagemode = False

					if not imagemode:
						line = line[line.index("|") + 1:].lstrip()
						if line.strip()[0] == "$":
							size = self.vars[line[1: line.index("|")].strip()]
						else:
							size = float(line[: line.index("|")].strip())

						line = line[line.index("|") + 1:].lstrip()
						if line.strip()[0] == "$":
							ratio = self.vars[line[1: line.index("|")].strip()]
						else:
							ratio = float(line[: line.index("|")].strip())

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
					else:
						size = 0
						typeface = "monospace"
						color = (255, 255, 255)

					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						design = self.vars[line[1: line.index("|")].strip()]
					else:
						print("Error: Outline only accepts variables")
						quit()

					#Reads the relation point
					#(Topleft, Topright, Bottomleft, Bottomright)
					line = line[line.index("|") + 1:].lstrip()
					if line[0] == "$":
						relation = self.vars[line[1: line.index("|")].strip()]
					else:
						relation = line[: line.index("|")].strip()
					relation = relation.lower()  # All lowercase to allow customizability

					line = line[line.index("|") + 1:].lstrip()
					rel_x, abs_x = analyse_num(line[0: line.index("|")].strip(), self.vars)
					line = line[line.index("|") + 1:-1].lstrip()
					rel_y, abs_y = analyse_num(line, self.vars)
					#If relative to another button
					if ident > 0:
						old_button = self.elems["buttons"][-1].buttons[0]
						border_size = old_button.modes[0][0].get_height()
						amount_of_buttons = len(self.elems["buttons"])
						#The plus one is needed because the current
						#button has not yet been addded to list
						pos_in_list = amount_of_buttons - (ident + 1)
						#Adds absolute x and y value to current button
						if relation[:3] == "top":
							abs_y += self.elems["buttons"][-1 * ident].pos.top
						if relation[:6] == "bottom":
							abs_y += self.elems["buttons"][pos_in_list].buttons[0].pos.bottom
							abs_y += border_size
						if relation[-4:] == "left":
							abs_x += self.elems["buttons"][-1 * ident].pos.left
						if relation[-5:] == "right":
							abs_x += self.elems["buttons"][-1 * ident].pos.right
							abs_x += border_size
						#Ignores relative placement
						rel_x = 0
						rel_y = 0

					self.elems["buttons"].append(disp_elem.button(text,
									rel_x, abs_x, rel_y, abs_y, ref,
									content,
									typeface, size, ratio, color, design[:3]))
					#Centers non-relative buttons so their center is on the
					#given x and y coordiante
					if ident == 0:
						self.elems["buttons"][-1].center()
					else:
						button = self.elems["buttons"][-2].buttons[0]
						border = button.modes[0][0].get_height()
						self.elems["buttons"][-1].pos.x += 2 * border
						self.elems["buttons"][-1].pos.y += 4 * border

				if line[0] == "-":
					line = line[2:]

					text = (line[:line.index("|")]).strip()
					if text[0] == "$":
						text = self.vars[text[1:]]

					if line.count("|") == 10:
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
						size = int(self.vars[line[1: line.index("|")].strip()])
					else:
						size = int(line[: line.index("|")].strip())

					line = line[line.index("|") + 1:].lstrip()
					if line.strip()[0] == "$":
						ratio = self.vars[line[1: line.index("|")].strip()]
					else:
						ratio = float(line[: line.index("|")].strip())

					line = line[line.index("|") + 1:].lstrip()
					if line.strip()[0] == "$":
						typeface = self.vars[line[1: line.index("|")].strip()]
					else:
						typeface = line[: line.index("|")].strip()

					line = line[line.index("|") + 1:].lstrip()
					if line.strip()[0] == "$":
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
								size, ratio, typeface, color, img,
								rel_x, abs_x, rel_y, abs_y, ref, options))

		if "background" in self.vars:
			self.elems["surfs"]["background"] = [pygame.transform.smoothscale(
					pygame.image.load(self.vars["background"][0]).convert(),
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