# -*- coding: utf-8 -*-
from libs.tygamusic import tygamusic
from . import settings


def init():
	global music

	music = tygamusic.CreateQueue("./assets/music/", "$not$",
				settings.variables.musicend)
	music.update(False, False)
	music.volume = settings.variables.volume
