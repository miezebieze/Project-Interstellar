# -*- coding: utf-8 -*-
import pygame
import math
from . import settings
from . import sounds
from . import specials
from pygame.locals import *

"""Blits everything and flips screen"""


def init():
	"""Some variable initializing"""
	#nothing to explain here
	global fullscreenold
	global player
	global playerup
	global alpha
	global no16to9
	global correcture
	global correcture_pos
	global show
	alpha = 0
	create_images("Player")
	player = playerup
	settings.fullscreenold = settings.fullscreen
	no16to9 = False
	show = 0
	if settings.aspect_ratio != 16.0 / 9:
		#makes a black stripe if not 16 to 9
		no16to9 = True
		delta_screeny = settings.screeny - settings.screeny_current
		correcture = pygame.Surface((settings.screenx, delta_screeny))
		correcture_pos = correcture.fill((0, 0, 0))
		correcture.set_alpha(255)
		correcture_pos.bottomleft = (0, settings.screeny)


def ingame():
	"""Draws everything while game runs"""
	#nothing to explain here i guess
	from . import movement
	global player

	screen = settings.screen
	screenx = settings.screenx_current
	player_pos = movement.player_pos

	texttargets = str(len(settings.world.targets)) + " / " + str(settings.dtargets)
	textsurf = settings.stdfont.render(texttargets, 1, settings.color)
	textrect = textsurf.get_rect()
	textrect.right = screenx
	textrect.top = 40

	adjustscreen()

	settings.world.blit()

	status()

	screen.blit(player, player_pos)  # lint:ok
	debug()
	drawsongname()
	screen.blit(textsurf, textrect)

	if no16to9:
		screen.blit(correcture, correcture_pos)

	pygame.display.flip()


def debug():
	"""shows debug info on screen"""
	#nothing to explain here too?
	from . import movement

	debugscreen = settings.debugscreen
	rot_dest = settings.rot_dest
	rotation = settings.rotation
	font = settings.stdfont
	player_pos = settings.player_pos
	screen = settings.screen
	speed = settings.speed
	move = settings.move
	move_x = movement.move_x * speed
	move_y = movement.move_y * speed
	pos_x = settings.pos_x
	pos_y = settings.pos_y
	clock = settings.clock
	objects_on_screen = settings.objects_on_screen
	color = settings.color

	if settings.pos_x >= 0.9 and settings.pos_y >= 0.9:
		isnear = "True"
	else:
		isnear = "False"

	if debugscreen:
		rot = str(rot_dest) + ", " + str(rotation) + ")"
		speed = "(" + str(round(move_x, 3)) + ", " + str(round(move_y, 3)) + ")"
		pos = ("(" + str(pos_x) + ", " + str(pos_y) + ")")
		fps = str(math.floor(clock.get_fps()))
		time = "time scince start: " + str(settings.timeplay)
		pixpos = "(" + str(player_pos.left) + ", " + str(player_pos.top) + ")"
		entitys = "Entitys: " + str(objects_on_screen)

		texttime = font.render(time, True, color)
		textfps = font.render("fps: " + fps, True, color)
		textxy = font.render("(x%, y%): " + pos, True, color)
		textpixpos = font.render("(x, y): " + pixpos, True, color)
		textrot = font.render("(destination, current): (" + rot, True, color)
		textspeed = font.render("(speedx, speedy): " + speed, True, color)
		isnear = font.render("Inzone: " + isnear, True, color)
		textdoesmove = font.render("move?: " + str(move), True, color)
		textentitys = font.render(entitys, True, color)

		screen.blit(textfps, (0, 0))
		screen.blit(textxy, (0, 20))
		screen.blit(textpixpos, (0, 40))
		screen.blit(textrot, (0, 60))
		screen.blit(textspeed, (0, 80))
		screen.blit(isnear, (0, 100))
		screen.blit(textdoesmove, (0, 120))
		screen.blit(texttime, (0, 140))
		screen.blit(textentitys, (0, 160))


def drawsongname():
	"""shows the songname if new song is played"""
	global show
	global songname
	global font_pos
	global musics
	global alpha

	screenx = settings.screenx_current
	screen = settings.screen
	typeface = settings.typeface

	for event in settings.events:
		if pygame.mixer.music.get_pos() < 4000 and sounds.music.volume != 0:
			show = 40 * 8
			font = pygame.font.SysFont(typeface, 15)
			song = sounds.music.playlist[0].replace("_", " ")[:-4]
			#To all of you:
			#USE BACKGROUND COLOR
			#cant apply alpha otherwise (took hours to figure out)
			songname = font.render(song, True, settings.color, (0, 0, 5))
			font_pos = songname.get_rect()
			font_pos.right = screenx - 10
			font_pos.top = 10
			alpha = 255
		if event.type == USEREVENT + 1 and sounds.music.volume != 0:
			show -= 1 if show > 0 else False
			if show <= 40 * 4 and alpha > 0:
				alpha -= 1.6

			songname.set_alpha(int(alpha))

	if pygame.mixer.music.get_volume() != 0.0 and show != 0:
		screen.blit(songname, font_pos)


def adjustscreen():
	"""Changes to fullscreen and back"""
	#changes resolution and so on when fullscreen is toggled
	global fullscreenold

	screenx = settings.screenx
	screeny = settings.screeny
	fullscreen = settings.fullscreen
	fullscreenold = settings.fullscreenold

	if fullscreenold != fullscreen:
		if fullscreen:
			pygame.display.set_mode((screenx, screeny), pygame.FULLSCREEN)
		if not fullscreen:
			pygame.display.set_mode((screenx / 2, screeny / 2))
		settings.fullscreenold = fullscreen


def playerpicturehandler():
	"""changes the playerimage corresponding to the movement direction"""
	global player
	global update
	global rotation
	global playerup
	global playeruple
	global playerle
	global playerdole
	global playerdo
	global playerdori
	global playerupri
	rotation = settings.rotation
	update = settings.update

	if update:
		settings.update = False
		if rotation == 0 or rotation == 360:
			player = playerup
		if rotation == 45:
			player = playerupri
		if rotation == 90:
			player = playerri
		if rotation == 135:
			player = playerdori
		if rotation == 180:
			player = playerdo
		if rotation == 225:
			player = playerdole
		if rotation == 270:
			player = playerle
		if rotation == 315:
			player = playeruple


def create_images(name):
	"""creates new images from one image for the player"""
	global playerup
	global playeruple
	global playerle
	global playerdole
	global playerdo
	global playerdori
	global playerri
	global playerupri

	folder = "./assets/sprites/player/"

	names = [
		name + "_upri", name + "_ri", name + "_dori", name + "_do",
		name + "_dole", name + "_le", name + "_uple"]

	#generates new images in ./assets/sprites/player
	for nameoffile in names:
		playerup = pygame.image.load("./assets/sprites/" + name + "_up.tif")
		angle = (names.index(nameoffile) + 1) * -45
		nameoffile = folder + nameoffile + ".png"
		pygame.image.save(pygame.transform.rotate(playerup, angle), nameoffile)

	#loads images into ram
	playerup = pygame.image.load("./assets/sprites/" + name + "_up.tif")
	playerupri = pygame.image.load(folder + name + "_upri.png")
	playerri = pygame.image.load(folder + name + "_ri.png")
	playerdori = pygame.image.load(folder + name + "_dori.png")
	playerdo = pygame.image.load(folder + name + "_do.png")
	playerdole = pygame.image.load(folder + name + "_dole.png")
	playerle = pygame.image.load(folder + name + "_le.png")
	playeruple = pygame.image.load(folder + name + "_uple.png")


def status():
	xsize = int(settings.screenx_current * 0.05)
	ysize = int(settings.screeny_current * 0.3) + 10
	bar = pygame.Surface((xsize, ysize))
	border = pygame.transform.scale(settings.border1, (xsize, ysize))
	borderpos = border.get_rect()
	borderpos.bottomright = (settings.screenx_current,
		settings.screeny_current)
	pos = bar.fill((62, 186, 23))
	pos.right = settings.screenx_current
	pos.top = settings.screeny_current - (pos.h / 100.0) * specials.energy
	settings.screen.blit(bar, pos)
	settings.screen.blit(border, borderpos)