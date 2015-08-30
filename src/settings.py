# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from ConfigParser import SafeConfigParser
from libs.pyganim import pyganim
import os
import shutil
import sys
import traceback
import random


def init():

	global up  # player should move up
	global down  # player should move down
	global left  # player should move left
	global right  # player should move right
#		global player  # player surf
#		global player_pos  # player rect
#		global rotation  # current rotation of player
#		global rot_dest  # destination in which to rotate
#		global move  # determines if player should move at all
#		global move_x  # movement in x direction in pixels
#		global move_y  # movement in y direction in pixels
#		global pos_x  # percentage position of screen
#		global pos_y  # percentage position of screen
#		global speed  # speed of player
	global konstspeed  # some konstant for speed
	global clock  # clock object of pygame
	global stdfont  # global font defenition
	global typeface  # the typeface...
	global fullscreen  # determines current state if fullscreen or not
	global fullscreenold  # used to check if fullscreen has changes
	global screen  # the screen
	global screenx  # maximum x pixels
	global screeny  # maximum y pixels
	global aspect_ratio  # aspect ratio
	global screenx_current  # current x pixels
	global screeny_current  # current y pixels
	global fade  # a black surface
	global fade_pos  # position of the black surface
	global fake_size  # the ratio of screenx_current and the size of the background
	global bullets  # list of all bullets
	global dstars  # amount of stars
	global debugscreen  # determines wether to show debug info
	global isnear  # easteregg
	global button  # image for the button
	global buttonover  # = when hovered over
	global buttonclick  # = when clicked
	global field  # image for the inputfield
	global field1  # other image for inputfield
	global knob  # knob image
	global box  # button image
	global bullet_img  # image for the bullet
	global targeton_img  # surf for target whenlight turned on
	global targetoff_img  # surf for target when turned off
	global code  # used for custom user events
	global events  # events
	global music  # the music playlist object
	global color  # global color defenition
	global skip  # unsused (currently)
	global volume  # volume
	global musics  # the list of music titles assoziated wih the music files
	global saves  # all savegames
	global psycomode  # if psycomode is turned on
#		global timeplay  # time how long the player has been playing
	global current_game  # the current savegame and default when no game is saved
	global explosions  # list of surfs of explosions
	global explosions_disp  # list of showing explosions
	global run  # boolean for main loop
	global dtargets  # amount of targets
#		global update  # determines whether new image needs to be loaded
	global include_music
	global morevents
	global infinitevents
	global musicend
	global border1
	global world  # a placeholder for the world class
	global objects_on_screen  # entitys currently blitted to screen
	global player  # abstract player class
	global localmap  # A dict of the local worlds
	global loading_time  # time until first blit
	global seed

	#for this operation os.urandom is used
	seed_size = 16
	seed = random.randint(10 ** (seed_size - 1), (10 ** seed_size) - 1)
	random.seed(seed)

	#set up screen
	pygame.event.set_grab(False)
	pygame.mouse.set_visible(False)

	screenx = pygame.display.Info().current_w
	screeny = pygame.display.Info().current_h
	pygame.display.set_mode((1, 1))
	aspect_ratio = screenx / float(screeny)
	screenx_current = screenx
	screeny_current = int(screenx_current * 9.0 / 16.0)

	#create empty folders if needed
	if not os.path.exists("./assets/sprites/player/"):
		os.makedirs("./assets/sprites/player/")
	if not os.path.exists("./screenshots/"):
		os.makedirs("./screenshots/")

	#load images and convert them to the fatest blittable format
	background = pygame.image.load("./assets/sprites/Background2.tif").convert()
	fade = pygame.Surface((screenx, screeny))
	button = pygame.image.load("./assets/sprites/Button1.tif").convert_alpha()
	buttonover = pygame.image.load("./assets/sprites/Button2.tif").convert_alpha()
	buttonclick = pygame.image.load("./assets/sprites/Button3.tif").convert_alpha()
	field = pygame.image.load("./assets/sprites/inputbox1.tif").convert_alpha()
	field1 = pygame.image.load("./assets/sprites/inputbox2.tif").convert_alpha()
	knob = pygame.image.load("./assets/sprites/knob1.tif").convert()
	box = pygame.image.load("./assets/sprites/Button1.tif").convert_alpha()
	bullet_img = pygame.image.load("./assets/sprites/Bullet.tif").convert_alpha()
	targeton_img = pygame.image.load("./assets/sprites/mine_on.tif"
				).convert_alpha()
	targetoff_img = pygame.image.load("./assets/sprites/mine_off.tif"
				).convert_alpha()
	border1 = pygame.image.load("./assets/sprites/bar1.tif").convert_alpha()

	fade_pos = fade.get_rect()  # lint:ok

	#define some konstants or default values
	clock = pygame.time.Clock()
	typeface = "monospace"
	stdfont = pygame.font.SysFont(typeface, 15)

	version = "0.3.2.8 dev"
	up = False
	down = False
	left = False
	right = False
	konstspeed = 0.0025

	fullscreen = False
	debugscreen = True
	dstars = 500
	isnear = "False"
	code = ""
	events = []
	color = (255, 255, 10)
	skip = False
	volume = 0.5
	fullscreenold = False
	fake_size = 8 / 7.0
	psycomode = False
	current_game = "default"
	run = True
	dtargets = 15
	include_music = False
	morevents = []
	bullets = []
	infinitevents = {"fire1": False, "roundfire": False}
	musicend = USEREVENT + 100
	events = []
	loading_time = 0

	from .player import player as player
	player = player()

	pygame.display.set_caption("Project Interstellar " + version)
	pygame.display.set_icon(pygame.image.load("./assets/sprites/logo.png"))

	#more complex default settings like creation of stars and targets and so on
	if debugscreen:
		volume = 0.0
		fullscreen = False

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

	explosion9 = pyganim.PygAnimation(get_anim_source(9, 32), loop=False)
	explosion10 = pyganim.PygAnimation(get_anim_source(10, 32), loop=False)
	explosion11 = pyganim.PygAnimation(get_anim_source(11, 24), loop=False)
	explosions = [explosion9, explosion10, explosion11]
	explosions_disp = []

	saves = []
	for filename in os.listdir("./saves"):
		if filename.endswith(".ini"):
			filename = filename[:-4]
			saves.append(filename)

	if fullscreen:
		screen = pygame.display.set_mode(
			(screenx_current, screeny_current),
			pygame.FULLSCREEN, 32)
	if not fullscreen:
		screenx_current = int(screenx_current / 2.0)
		screeny_current = int(screeny_current / 2.0)
		screen = pygame.display.set_mode((screenx_current, screeny_current),
		0, 32)

	from . import worlds
	localmap = {}
	for a in range(9):
		world = worlds.world()
		world.generate(background, dstars, dtargets)
		localmap["[" + str(a + 1) + "]"] = world

	upd("adjust_screen")


def reset():

	"""resets some settings"""
	global up
	global down
	global left
	global right
	global player
	global player_pos
	global fade_pos
	global background_pos
	global rot_dest
	global move
	global move_x
	global move_y
	global speed
	global konstspeed
	global debugscreen
	global color
	global timeplay
	global dstars
	global dtargets

	pygame.event.set_grab(False)
	pygame.mouse.set_visible(False)

	player.reset()
	fade_pos = fade.get_rect()  # lint:ok

	konstspeed = 0.0025
	color = (255, 255, 10)

	from . import missions
	missions.handle("pause")

	if debugscreen:
		fullscreen = False  # lint:ok

	world.generate(world.background, dstars, dtargets)


def upd(level):

	"""updates various variables"""
	if level == "get_events":
		global events
		events = pygame.fastevent.get()
		return
	if level == "screenvalues":
		global screenx_current
		global screeny_current
		screenx_current = pygame.display.Info().current_w
		screeny_current = int(screenx_current * 9.0 / 16.0)
		return
	if level == "get_saves":
		global saves
		saves = []
		for filename in os.listdir("./saves"):
			if filename.endswith(".ini"):
				filename = filename[:-4]
				if not filename in ("default"):
					saves.append(filename)
		return
	if level == "adjust_screen":
		from . import draw
		global background
		global background_pos
		global konstspeed
		global no16to9

		draw.adjustscreen()
		upd("screenvalues")

		konstspeed = 0.0025
		konstspeed = konstspeed * (screenx_current / 1920.0)

		world.adjust_to_screen()

		return
	print("Something went wrong here")
	int("test")  # Used to crash the game to see where no option is selected


def toggle(var, option1, option2):
	#toggles between option1 and 2 and retunr var, saves some space
	if var == option1:
		var = "yep"
	if var == option2:
		var = option1
	if var == "yep":
		var = option2
	return var


def modrender(typeface, size, text, antialias, color, maxsize, borderoff):
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
		global saves
		global current_game

		name = name.encode("utf-8")
		self.name = name

		upd("get_saves")

		if len(saves) >= 50:
			return False

		#removes invalid characters
		if "/" in name:
			name = name.replace("/", "\\")
		if "%" in name:
			name = name.replace("%", "")

		current_game = name

		#handles the configparser object
		self.config = SafeConfigParser()
		self.config.read("./saves/" + name + ".ini")
		if not os.path.isfile("./saves/" + name + ".ini"):
			self.config.add_section("main")

		#sets values
		self.config.set("main", "fullscreen", str(fullscreen))
		self.config.set("main", "screenx_current", str(screenx_current))
		self.config.set("main", "screeny_current", str(screeny_current))
		self.config.set("main", "debug", str(debugscreen))
		self.config.set("main", "skip", "True")
		self.config.set("main", "posx", str(player.pos.x))
		self.config.set("main", "posy", str(player.pos.y))
		self.config.set("main", "volume", str(volume))
		#and writes them
		with open("./saves/" + name + ".ini", "w") as tmp:
			self.config.write(tmp)


def load(name):
	"""Load savegame"""
	global fullscreen
	global screenx_current
	global screeny_current
	global debugscreen
	global config
	global skip
	global pos_x
	global pos_y
	global volume
	global saves
	global screen

	upd("get_saves")

	config = SafeConfigParser()
	for a in saves:
		if a == name.encode("utf-8"):
			config.read("./saves/" + a + ".ini")
	if not (saves == []):

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
		except NoOptionError as test:
			print(("Saved game couldn't be loaded completly: " + str(test)))
		except Exception:
			print(("Unexpected error:", sys.exc_info()[0]))
			print((traceback.format_exc()))

	screen = pygame.display.set_mode((screenx_current, screeny_current))


def quit():
	"""Routine for exiting"""
	from . import midi_in
	midi_in.quit()
	pygame.quit()
	shutil.rmtree('./assets/sprites/player')
	sys.exit()