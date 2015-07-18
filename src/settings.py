# -*- coding: utf-8 -*-

"""The class that stores all of the settings and variables"""

import pygame
#from pygame.locals import *
from ConfigParser import SafeConfigParser
from libs.pyganim import pyganim
import os
import shutil
import sys
import traceback


class Settings:

	def __init__(self):

		#set up screen
		pygame.event.set_grab(False)
		pygame.mouse.set_visible(False)

		screenx, screeny = pygame.display.list_modes()[0]
		self.aspect_ratio = screenx / float(screeny)
		self.screenx_current = screenx
		self.screeny_current = int(self.screenx_current * 9.0 / 16.0)

		#create empty folders if needed
		if not os.path.exists("./assets/sprites/player/"):
			os.makedirs("./assets/sprites/player/")
		if not os.path.exists("./screenshots/"):
			os.makedirs("./screenshots/")

		#load images
		self.background = pygame.image.load(
					"./assets/sprites/Background2.tif").convert()
		self.fade = pygame.Surface((screenx, screeny))
		self.button = pygame.image.load("./assets/sprites/Button1.tif")
		self.buttonover = pygame.image.load("./assets/sprites/Button2.tif")
		self.buttonclick = pygame.image.load("./assets/sprites/Button3.tif")
		self.field = pygame.image.load("./assets/sprites/inputbox1.tif")
		self.field1 = pygame.image.load("./assets/sprites/inputbox2.tif")
		self.knob = pygame.image.load("./assets/sprites/knob1.tif")
		self.box = pygame.image.load("./assets/sprites/Button1.tif")
		self.bullet_img = pygame.image.load("./assets/sprites/Bullet.tif")
		self.targeton_img = pygame.image.load("./assets/sprites/mine_on.tif")
		self.targetoff_img = pygame.image.load("./assets/sprites/mine_off.tif")
		self.border1 = pygame.image.load("./assets/sprites/bar1.tif")

		self.fade_pos = fade.get_rect()  # lint:ok

		#define some konstants or default values
		self.clock = pygame.time.Clock()
		self.typeface = "monospace"
		self.stdfont = pygame.font.SysFont(self.typeface, 15)

		self.version = "0.3.2.8 dev"
		self.up = False
		self.down = False
		self.left = False
		self.right = False
		self.konstspeed = 0.0025

		self.fullscreen = False
		self.debugscreen = True
		self.dstars = 500
		self.isnear = "False"
		self.code = ""
		self.events = []
		self.color = (255, 255, 10)
		self.skip = False
		self.volume = 0.5
		self.fullscreenold = False
		self.fake_size = 8 / 7.0
		self.psycomode = False
		self.current_game = "default"
		self.run = True
		self.dtargets = 15
		self.include_music = False
		self.morevents = []
		self.bullets = []
		self.infinitevents = {"fire1": False, "roundfire": False}
		self.musicend = pygame.USEREVENT + 100
		self.events = []

		from .player import player as player
		self.player = player()

		pygame.display.set_caption("Project Interstellar " + self.version)
		pygame.display.set_icon(pygame.image.load("./assets/sprites/logo.png"))

		#more complex default settings like creation of stars and targets and so on
		if self.debugscreen:
			self.volume = 0.0
			self.fullscreen = False

		def get_anim_source(num, quantity):
			animationsourcetmp = []
			if num >= 10:
				num = str(num)
			else:
				num = "0" + str(num)
			for a in range(quantity):
				a = str(a)
				if int(a) < 10:
					a = "0" + str(a)
				tmp = ("./assets/sprites/explosions/expl_" + num + "_00" + a + ".tif", 0.04)
				animationsourcetmp.append(tmp)
			return animationsourcetmp

		self.explosion9 = pyganim.PygAnimation(self.get_anim_source(9, 32),
					loop=False)
		self.explosion10 = pyganim.PygAnimation(self.get_anim_source(10, 32),
					loop=False)
		self.explosion11 = pyganim.PygAnimation(self.get_anim_source(11, 24),
					loop=False)
		self.explosions = [self.explosion9, self.explosion10, self.explosion11]
		self.explosions_disp = []

		self.saves = []
		for filename in os.listdir("./saves"):
			if filename.endswith(".ini"):
				filename = filename[:-4]
				self.saves.append(filename)

		if self.fullscreen:
			#This should really be handled in the main file
			self.screen = pygame.display.set_mode(
				(self.screenx_current, self.screeny_current),
				pygame.FULLSCREEN, 32)
		if not self.fullscreen:
			self.screenx_current = int(self.screenx_current / 2.0)
			self.screeny_current = int(self.screeny_current / 2.0)
		self.screen = pygame.display.set_mode(
				(self.screenx_current, self.screeny_current),
				0, 32)

		from . import worlds
		self.localmap = {}
		for a in range(9):
			self.world = worlds.world()
			self.world.generate(self.background, self.dstars, self.dtargets)
			self.localmap["[" + str(a + 1) + "]"] = self.world

		self.upd("adjust_screen")

	def reset(self):

		"""resets some settings"""
		pygame.event.set_grab(False)
		pygame.mouse.set_visible(False)

		self.player.reset()
		self.fade_pos = fade.get_rect()  # lint:ok

		self.konstspeed = 0.0025
		self.color = (255, 255, 10)

		from . import missions
		missions.handle("pause")

		if self.debugscreen:
			self.fullscreen = False  # lint:ok

		self.world.generate(self.world.background, self.dstars, self.dtargets)

	def upd(self, level):

		"""updates various variables"""
		if level == "get_events":
			self.events = pygame.fastevent.get()
			return

		if level == "screenvalues+vol":  # So 1 counts too
			self.screenx_current = pygame.display.Info().current_w
			self.screeny_current = int(self.screenx_current * 9.0 / 16.0)
			self.volume = pygame.mixer.music.get_volume()
			return

		if level == "get_saves":
			self.saves = []
			for filename in os.listdir("./saves"):
				if filename.endswith(".ini"):
					filename = filename[:-4]
					if not filename in ("default"):
						self.saves.append(filename)
			return

		if level == "adjust_screen":
			from . import draw
			draw.adjustscreen()

			self.upd("screenvalues+vol")

			self.konstspeed = 0.0025
			self.konstspeed *= (self.screenx_current / 1920.0)

			self.world.adjust_to_screen()
			return

	print("Something went wrong here")

	raise "No acceptable input recieved"
	"""int("test")  # Used to crash the game to see where no option is selected"""
	#why? why not just raise
	"""Because it is not a critical error and should only raise
			when I did something wrong
			but it is of seldom need now."""

	#These next few don't NEED to be part of the class,
		#but I'm too lazy to completely do this file.
	#These should be in the class because of the current usage of settings.
		#And I would need to import setting.settings as settings
		#as well as import settings as somethingelse
	def toggle(self, var, option1, option2):
		#toggles between option1 and 2 and retunr var, saves some space
		if var == option1:
			var = option2
		elif var == option2:
			var = option1
		else:
			print ("var does not equal either option!")
		return var

	def modrender(self, typeface, size, text,
			antialias, color, maxsize, borderoff):
		#local typeface!
		nofit = True
		while nofit:
			tmpfont = pygame.font.SysFont(typeface, size)
			bool1 = tmpfont.size(text)[0] < maxsize[0] - (2 * borderoff)
			nofit = not (bool1 and tmpfont.size(text)[1] < maxsize[1] - (2 * borderoff))
			if size <= 5:
				nofit = False
			else:
				size -= 1
		return tmpfont.render(text, antialias, color)

	def getmaxsize(typeface, size, text, antialias, color, maxsize, borderoff):
		#local typeface!
		nofit = True
		while nofit:
			tmpfont = pygame.font.SysFont(typeface, size)
			bool1 = tmpfont.size(text)[0] < maxsize[0] - (2 * borderoff)
			nofit = not (bool1 and tmpfont.size(text)[1] < maxsize[1] - (2 * borderoff))
			if size <= 5:
				nofit = False
			else:
				size -= 1
		return size

		class save():

			def __init__(self, name):
				"""create a new savegame"""

				#TODO: check if single self selects
					#correct variable

				name = name.encode("utf-8")
				self.name = name

				self.upd("get_saves")

				if len(self.saves) >= 50:
					return False

				#removes invalid characters
				if "/" in name:
					name = name.replace("/", "\\")
				if "%" in name:
					name = name.replace("%", "")

				self.current_game = name

				#handles the configparser object
				self.config = SafeConfigParser()
				self.config.read("./saves/" + name + ".ini")
				if not os.path.isfile("./saves/" + name + ".ini"):
					self.config.add_section("main")

				#sets values
				self.config.set("main", "fullscreen", str(self.fullscreen))
				self.config.set("main", "screenx_current", str(self.screenx_current))
				self.config.set("main", "screeny_current", str(self.screeny_current))
				self.config.set("main", "debug", str(self.debugscreen))
				self.config.set("main", "skip", "True")
				self.config.set("main", "posx", str(self.player.pos.x))
				self.config.set("main", "posy", str(self.player.pos.y))
				self.config.set("main", "volume", str(self.volume))
				#and writes them
				with open("./saves/" + name + ".ini", "w") as tmp:
					self.config.write(tmp)

	"""You get my point. Much less globals, and all stored here in this class.
		It would take a lot of work to get all all of the files up to standards
		and to remove all the globals, but I think in the end it would be worth
		it. I feel like if you don't do this now, eventually you may get so fed
		up with how clunky and hard to manage the project becomes that you may
		give it up.
	"""

	def load(self, name):
		"""Load savegame"""

		self.upd("get_saves")

		config = SafeConfigParser()
		for a in self.saves:
			if a == name.encode("utf-8"):
				config.read("./saves/" + a + ".ini")
		if not (self.saves == []):

			#tries to load and returns values in terminal that couldnt be loaded
			try:
				#from ConfigParser import *
				from . import sounds
				#lint:disable
				fullscreen = config.getboolean("main", "fullscreen")
				screenx_current = int(config.getfloat("main", "screenx_current"))
				screeny_current = int(config.getfloat("main", "screeny_current"))
				debugscreen = config.getboolean("main", "debug")
				skip = config.getboolean("main", "skip")
				pos_x = config.getfloat("main", "posy")
				pos_y = config.getfloat("main", "posx")
				sounds.music.volume = config.getfloat("main", "volume")
				highscore = config.getint("main", "highscore")
				#lint:enable
			except SafeConfigParser.NoOptionError as test:
				print(("Saved game couldn't be loaded completly: " + str(test)))
			except Exception:
				print(("Unexpected error:", sys.exc_info()[0]))
				print((traceback.format_exc()))

		self.screen = pygame.display.set_mode(
				(self.screenx_current, self.screeny_current))

	def quit():
		"""Routine for exiting"""
		from . import midi_in
		midi_in.quit()
		pygame.quit()
		shutil.rmtree('./assets/sprites/player')
		sys.exit()
