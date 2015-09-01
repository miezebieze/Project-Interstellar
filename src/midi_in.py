# -*- coding: utf-8 -*-
import pygame
import pygame.midi
from pygame.locals import *
from . import settings

pygame.init()
pygame.midi.init()
pygame.fastevent.init()


def init():
	global device
	global connected
	get_device()
	try:
		device = pygame.midi.Input(device_id)
		get_input()
		connected = True
	except NameError:
		connected = False
		print("No valid keyboard connected!")


def get_device():
	global device_id

	for i in range(pygame.midi.get_count()):
		tmp = pygame.midi.get_device_info(i)
		(interf, name, input, output, opened) = tmp

		out = ""
		if input:
			out = False
		if output:
			out = True

		if name == "USB2.0-MIDI MIDI 1" and not out:
			device_id = i


def get_input():
	for event in settings.events:
		if event.type == QUIT:
			settings.quit()
		if event.type == pygame.midi.MIDIIN:
			if event.data2 > 0:
				pressed = True
			else:
				pressed = False

			key = event.data1
			if key == 70 and pressed:
				settings.psycomode = settings.toggle(settings.psycomode, True, False)
			if key == 68 and pressed:
				settings.infinitevents["roundfire"] = (
					settings.toggle(settings.infinitevents["roundfire"], True, False))
			if key == 67 and pressed:
				settings.morevents.append("Remove")
			if key == 69 and pressed:
				settings.morevents.append("Add")
			if key == 66 and pressed:
				settings.morevents.append("Circle")
			if key == 96 and pressed:
				settings.morevents.append("Changedir")
			if key == 61:
				settings.infinitevents["fire1"] = (
					settings.toggle(settings.infinitevents["fire1"], True, False))
	if device.poll():
		midi_actions = device.read(10)
		midi_events = pygame.midi.midis2events(midi_actions, device_id)
		for event in midi_events:
			pygame.fastevent.post(event)


def quit():
	global device
	try:
		del device
	except:
		#I know, no device connected…
		pass


def do():

	global connected
	if settings.debugmode and connected:
		get_input()