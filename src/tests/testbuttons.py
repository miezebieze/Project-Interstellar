# -*- coding: utf-8 -*-
import pygame
import pygame.midi
import string
from pygame.locals import *

pygame.init()
pygame.midi.init()
pygame.fastevent.init()

pygame.display.set_mode((100, 100))

b = True

global device_id

global device
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

device = pygame.midi.Input(device_id)

while b:
	evs = pygame.fastevent.get()

	for a in evs:
		if a.type == KEYDOWN:
			key = pygame.key.name(a.key)
			if key == "escape":
				del device
				exit()
		if a.type == KEYDOWN:
			if a.unicode in string.printable:
				print pygame.key.name(a.key)
		if a.type == MOUSEBUTTONDOWN:
			print a.button
			#print
		if a.type == pygame.midi.MIDIIN:
			print a.data1

	if device.poll():
		midi_actions = device.read(10)
		midi_events = pygame.midi.midis2events(midi_actions, device_id)
		for event in midi_events:
			pygame.fastevent.post(event)