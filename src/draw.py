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
	# nothing to explain here
	global variables
	global fullscreenold
	global playerup
	global alpha
	global no16to9
	global correcture
	global correcture_pos
	global show

	variables = settings.variables
	alpha = 0
	variables.fullscreenold = variables.fullscreen
	no16to9 = False
	show = 0
	if variables.aspect_ratio != 16.0 / 9:
		# makes a black stripe if not 16 to 9
		no16to9 = True
		delta_screeny = (variables.screeny_current
				- (variables.screenx_current * 9.0 / 16))
		correcture = pygame.Surface((variables.screenx_current, delta_screeny)
					).convert_alpha()
		correcture_pos = correcture.fill((0, 0, 0))
		correcture.set_alpha(255)
		correcture_pos.topleft = (0, (variables.screenx_current * 9.0 / 16))


def ingame():
	"""Draws everything while game runs"""
	# nothing to explain here i guess

	variables.world.blit()

	status()

	variables.player.blit(variables.screen)
	debug()
	drawsongname()
	drawtargetsum()
	drawworldname()

	if no16to9:
		variables.screen.blit(correcture, correcture_pos)

	pygame.display.flip()


def debug():
	"""shows debug info on screen"""
	# nothing to explain here too?

	debugscreen = variables.debugscreen
	rot_dest = variables.player.rot_dest
	rotation = variables.player.rotation
	font = variables.stdfont
	player_pos = variables.player.pos
	screen = variables.screen
	speed = variables.player.speed
	move = variables.player.should_move
	move_x = variables.player.move_x * speed
	move_y = variables.player.move_y * speed
	pos_x = variables.player.rel_x
	pos_y = variables.player.rel_y
	clock = variables.clock
	objects_on_screen = variables.objects_on_screen
	color = variables.color

	if pos_x >= 0.9 and pos_y >= 0.9:
		isnear = "True"
	else:
		isnear = "False"

	if debugscreen:
		rot = str(rot_dest) + ", " + str(rotation) + ")"
		speed = "(" + str(round(move_x, 3)) + ", " + str(round(move_y, 3)) + ")"
		pos = ("(" + str(pos_x) + ", " + str(pos_y) + ")")
		fps = str(math.floor(clock.get_fps()))
		time = "time scince start: " + str(variables.player.timeplay)
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


def drawtargetsum():

	textlocaltargets = (str(len(variables.world.targets))
			+ " / "
			+ str(variables.dtargets))
	text1surf = variables.stdfont.render(textlocaltargets, 1, variables.color)
	text1rect = text1surf.get_rect()
	text1rect.right = variables.screenx_current
	text1rect.top = 40

	alltargets = 0
	for world in variables.localmap:
		alltargets += len(variables.localmap[world].targets)

	textglobaltargets = str(alltargets) + " / " + str(variables.dtargets * 8)
	text2surf = variables.stdfont.render(textglobaltargets, 1, variables.color)
	text2rect = text2surf.get_rect()
	text2rect.right = variables.screenx_current
	text2rect.top = 60
	variables.screen.blit(text1surf, text1rect)
	variables.screen.blit(text2surf, text2rect)


def drawsongname():
	"""shows the songname if new song is played"""
	global show
	global songname
	global font_pos
	global musics
	global alpha

	screenx = variables.screenx_current
	screen = variables.screen
	typeface = variables.typeface

	for event in variables.events:
		if pygame.mixer.music.get_pos() < 4000 and sounds.music.volume != 0:
			show = 40 * 8
			font = pygame.font.SysFont(typeface, 15)
			song = sounds.music.playlist[0].replace("_", " ")[:-4]
			# To all of you:
			# USE BACKGROUND COLOR
			# cant apply alpha otherwise (took hours to figure out)
			songname = font.render(song, True, variables.color, (0, 0, 5))
			font_pos = songname.get_rect()
			font_pos.right = screenx - 10
			font_pos.top = 10
			alpha = 255
		if event.type == USEREVENT + 1 and sounds.music.volume != 0:
			show -= 1 if show > 0 else False
			if show <= 40 * 4 and alpha > 0:
				alpha -= 1.6
			try:
				songname.set_alpha(int(alpha))
			except:
				pass
				# Timing error is not important

	if pygame.mixer.music.get_volume() != 0.0 and show != 0:
		screen.blit(songname, font_pos)


def drawworldname():
			font = pygame.font.SysFont(variables.typeface, 50)
			name = font.render("World: " + str(variables.world.name),
					True, variables.color)
			pos = name.get_rect()
			pos.centerx = variables.screenx_current / 2
			variables.screen.blit(name, pos)


def status():
	xsize = int(variables.screenx_current * 0.05)
	ysize = int(variables.screeny_current * 0.3) + 10
	bar = pygame.Surface((xsize, ysize)).convert_alpha()
	border = pygame.transform.scale(variables.border1, (xsize, ysize)
				).convert_alpha()
	border.set_alpha(0)
	borderpos = border.get_rect()
	borderpos.bottomright = (variables.screenx_current,
		variables.screeny_current - correcture_pos.h)
	pos = bar.fill((62, 186, 23, 40))
	pos.right = variables.screenx_current
	pos.top = (variables.screeny_current
		- (pos.h / 100.0) * specials.energy
		- correcture_pos.h)
	variables.screen.blit(bar, pos)
	variables.screen.blit(border, borderpos)
