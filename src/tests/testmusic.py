# -*- coding: utf-8 -*-

import os
import pygame
import random
#from .. import settings

#TODO: finish system


class new_music_class():

	def __init__(self):
		"""creates a music handeling object"""
		self.playlist = []
		self.timeplayed = {}
		self.pauselevel = 0
		self.playing = 0
		self.currentsong = 0
		self.path = "./assets/music/"
		self.files = self.get_music()
		#Fills playlist with 4 songs already
		while len(self.playlist) < 4:
			self.add_random(0)
			self.remove_dublicates()

	def get_music(self):
		"""Returns all background music filenames"""
		files = []
		#Runs through all files and checks for filetype
		for filename in os.listdir("../../assets/music/"):
			fileissupportedmusic = [
				filename.endswith(".ogg") or filename.endswith(".mp3")
				or filename.endswith(".mid") or filename.endswith(".midi")
				or filename.endswith(".wav")]

			#Adds file if it is supported format and a background music
			if fileissupportedmusic[0] and filename[0:4] != "%AND":
				files.append(filename)
		return files

	def update(self):
		"""Update-routine like check if music has ended"""
		#self.volume = settings.volume
		pygame.mixer.music.set_volume(self.volume)
		if len(self.playlist) < 4:
			self.add_random("end")
		elif not pygame.mixer.music.get_busy() or self.force_update:
			pygame.mixer.music.stop()
			self.force_update = False
			self.play("next")
			self.show = 40 * 10

	def play(self, *options):
		"""Control music playback"""
		options = list(options)
		if options[0] == "play":
			#first song of playlist is played if none is playing
			if self.pauselevel == 0:
				if self.playing == 0:
					pygame.mixer.load(self.playlist[0])
					pygame.mixer.music.play(self.playlist[0])
				if self.playing == 1:
					pygame.mixer.music.play(self.playlist[self.currentsong])

		if options[0] == "pause":
			pass

		if options[0] == "unpause":
			pass

		if options[0] == "stop":
			pass

		if options[0] == "loop":
			pass

	def add_random(self, pos):
		"""Adds random song to playlist"""
		#makes it easier to add song at end by using "end" as pos
		if type(pos) is str:
			if pos == "end" and len(self.playlist) != 0:
				pos = len(self.playlist)
			else:
				pos = 0

		#selects a new song and ensures that never two songs are directly
		#after each other
		newsong = self.files[random.randint(0, len(self.files) - 1)]
		result = False
		if len(self.playlist) != 0:
			while not result:
				newsong = self.files[random.randint(0, len(self.files) - 1)]
				try:
					#checks right neighbor is diffrent
					right = not (newsong == self.playlist[pos + 1])
				except:
					#if has no neighbor, left decides
					#(if left is true then end result is true
					# if left is false then end result is false)
					right = True
				try:
					#checks left neighbor if diffrent and decides
					#if one of both partner is diffrent as newsong
					result = right and not (newsong == self.playlist[pos])
				except:
					#if no left neighbor right decides
					result = right
		else:
			newsong = self.files[random.randint(0, len(self.files) - 1)]

		#adds song at pos to playlist
		self.queue(pos, newsong)

	def remove_dublicates(self):
		"""Removes dublicate songs whilst preserving order"""
		#these three lines werent done by me
		#and only slightly modified
		#Thanks to http://www.peterbe.com/plog/uniqifiers-benchmark
		#for creating them (i think he did it but im not sure)
		seen = set()
		seen_add = seen.add
		self.playlist = [x for x in self.playlist if not (x in seen or seen_add(x))]

	def queue(self, pos, song):
		"""Queues the new song at position"""
		#makes it easier to add song at end by using "end" as pos
		if type(pos) is str:
			if pos == "end":
				pos = len(self.playlist)
			else:
				pos = 0

		#adds song at pos to playlist
		self.playlist.insert(pos, song)


test = new_music_class()
print test.playlist