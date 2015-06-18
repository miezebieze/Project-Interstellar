from . import settings
from . import objects
"""An abstact level for handeling multiple worlds."""
#TODO:implement into actual game


class world():

	def __init__(self):
		pass

	def create(self, dstars, dtargets):
		#initialize a new "world"
		#TODO: Change loading of things to this class
		#load background image
		self.background = settings.background
		self.background_pos = settings.background_pos
		#set background position
		self.background_pos.left = int(-(settings.pos_x * (
			settings.screenx_current * (settings.fake_size - 1))))
		self.background_pos.top = int(-(settings.pos_y * (
			settings.screeny_current * (settings.fake_size - 1))))

		#create targets and stars
		self.stars = []
		self.targets = []
		for counter in range(dstars):
			tmpstar = objects.stars()
			self.stars.append(tmpstar)
		for counter in range(dtargets):
			self.targets.append(objects.target())

	def move(self):
		"""Move everything in the world."""
		player_pos = settings.player_pos

		self.background_pos.left = int(-(settings.pos_x * (
			settings.screenx_current * (settings.fake_size - 1))))
		self.background_pos.top = int(-(settings.pos_y * (
			settings.screeny_current * (settings.fake_size - 1))))

		for star in self.stars:
			star.move(player_pos.left, player_pos.top)

		for bullet in settings.bullets:
			bullet.move(player_pos)
			if not bullet.inscreen:
				settings.bullets.remove(bullet)

		for target in self.targets:
			target.move(player_pos.left, player_pos.top)
			for bullet in settings.bullets:
				target.test_ishit(bullet.pos)
			if target.gothit:
				settings.targets.remove(target)
				settings.explosions_disp.append(target)
				settings.explosions_disp = list(set(settings.explosions_disp))

		for explosion in settings.explosions_disp:
			if explosion.kill_entity:
				settings.explosions_disp.remove(explosion)
			else:
				explosion.move(player_pos.left, player_pos.top)

	def blit(self):
		"""Blit everything in the world."""

		#blit background
		settings.screen.blit(self.background, self.background_pos)

		#Blit all objects
		for star in self.stars:
			star.blitstar()
		for bullet in settings.bullets:
			bullet.blit()
		for target in self.targets:
			target.blit()
		for explosion in settings.explosions_disp:
			explosion.blit()
