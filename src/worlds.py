from . import settings
from . import objects
from . import draw
import pygame
"""An abstact level for handeling multiple worlds."""


class world():

	def __init__(self, name):
		global variables
		self.variables = settings.variables
		self.name = name
		pass

	def generate(self, background, dstars, dtargets):
		# initialize a new "world"

		# load background image
		self.background = background
		self.background_pos = self.background.get_rect()
		# set background position
		self.background_pos.left = int(-(self.variables.player.rel_x * (
			self.variables.screenx_current * (self.variables.fake_size - 1))))
		self.background_pos.top = int(-(self.variables.player.rel_y * (
			self.variables.screeny_current * (self.variables.fake_size - 1))))

		# create targets and stars
		self.stars = []
		self.targets = []
		for counter in range(dstars):
			tmpstar = objects.stars()
			self.stars.append(tmpstar)
		for counter in range(dtargets):
			tmptarget = objects.target()
			self.targets.append(tmptarget)

		self.warp1 = objects.warp_station()

		self.adjust_to_screen()

	def move(self):
		"""Move everything in the world."""
		player_pos = self.variables.player.pos

		self.background_pos.left = int(-(self.variables.player.rel_x * (
			self.variables.screenx_current * (self.variables.fake_size - 1))))
		self.background_pos.top = int(-(self.variables.player.rel_y * (
			self.variables.screeny_current * (self.variables.fake_size - 1))))

		self.warp1.move(player_pos)
		self.warp1.test(player_pos)

		for star in self.stars:
			star.move(player_pos.left, player_pos.top)

		for bullet in self.variables.bullets:
			bullet.move(player_pos)
			if not bullet.pos.colliderect(self.background_pos):
				self.variables.bullets.remove(bullet)

		for target in self.targets:
			target.move(player_pos.left, player_pos.top)
			for bullet in self.variables.bullets:
				target.test_ishit(bullet.pos)
			if target.gothit:
				self.targets.remove(target)
				self.variables.explosions_disp.append(target)
				self.variables.explosions_disp = list(set(self.variables.explosions_disp))

		for explosion in self.variables.explosions_disp:
			if explosion.kill_entity:
				self.variables.explosions_disp.remove(explosion)
			else:
				explosion.move(player_pos.left, player_pos.top)

	def blit(self):
		"""Blit everything in the world."""

		# blit background
		self.variables.screen.blit(self.background, self.background_pos)

		# Blit all objects
		self.variables.objects_on_screen = 0
		for star in self.stars:
			isdisplayed = star.blitstar()
			if isdisplayed:
				self.variables.objects_on_screen += 1
		for bullet in self.variables.bullets:
			isdisplayed = bullet.blit()
			if isdisplayed:
				self.variables.objects_on_screen += 1
		for target in self.targets:
			isdisplayed = target.blit()
			if isdisplayed:
				self.variables.objects_on_screen += 1
		for explosion in self.variables.explosions_disp:
			explosion.blit()
		self.warp1.blit()

	def adjust_to_screen(self):

		tmpx = self.variables.screenx_current * self.variables.fake_size
		tmpy = self.variables.screeny_current * self.variables.fake_size
		screen_current = (int(tmpx), int(tmpy))
		background = pygame.image.load("./assets/sprites/Background2.tif").convert()
		self.background = pygame.transform.smoothscale(background, screen_current)
		self.background_pos = self.background.get_rect()

		tmp = -(self.variables.player.pos.x * (self.variables.screenx_current *
					(self.variables.fake_size - 1)))
		self.background_pos.left = int(tmp)
		tmp = -(self.variables.player.pos.y * (self.variables.screeny_current *
					(self.variables.fake_size - 1)))
		self.background_pos.top = tmp

		draw.no16to9 = False
		if self.variables.aspect_ratio != 16.0 / 9:
			draw.no16to9 = True
			delta_screeny = (self.variables.screeny_current
					- (self.variables.screenx_current * 9.0 / 16))
			draw.correcture = pygame.Surface((self.variables.screenx_current,
						delta_screeny)
						).convert_alpha()
			draw.correcture_pos = draw.correcture.fill((0, 0, 0))
			draw.correcture.set_alpha(255)
			draw.correcture_pos.topleft = (0,
						(self.variables.screenx_current * 9.0 / 16))

		for star in self.stars:
			star.update(self.variables.screenx_current / 1920.0)

		for target in self.targets:
			target.update()

		self.warp1.update()
