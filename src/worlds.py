from . import settings
from . import objects
from . import draw
from . import menu
import pygame
import random
import math
"""An abstact level for handeling multiple worlds."""


class world():

	def __init__(self, name):
		self.name = name
		pass

	def generate(self, background, dstars, dtargets):
		#initialize a new "world"

		#load background image
		self.background = background
		self.background_pos = self.background.get_rect()
		#set background position
		self.background_pos.left = int(-(settings.player.rel_x * (
			settings.screenx_current * (settings.fake_size - 1))))
		self.background_pos.top = int(-(settings.player.rel_y * (
			settings.screeny_current * (settings.fake_size - 1))))

		#create targets and stars
		self.stars = []
		self.targets = []
		for counter in range(dstars):
			tmpstar = objects.stars()
			self.stars.append(tmpstar)
		for counter in range(dtargets):
			tmptarget = objects.target()
			self.targets.append(tmptarget)

		class warp():

			def __init__(self):
				self.x_pos = random.random()
				self.y_pos = random.random()
				self.screen = settings.screen
				self.update()

			def update(self):
				self.img = pygame.image.load("./assets/sprites/station1.tif")
				self.img = pygame.transform.smoothscale(self.img,
								(int(settings.screenx_current * 0.1),
									int(settings.screenx_current * 0.1)
								))
				self.pos = self.img.get_rect()
				self.pos.x = self.x_pos * (settings.world.background_pos.w - self.pos.w)
				self.pos.y = self.y_pos * (settings.world.background_pos.h - self.pos.h)
				self.anchorx, self.anchory = self.pos.topleft

			def move(self, playerpos):
				self.pos.left = self.anchorx - playerpos.x
				self.pos.top = self.anchory - playerpos.y

			def test(self, playerpos):
				def testpoint(point):
					x_sqr = ((point[0] * point[0])
						- (2.0 * self.pos.centerx * point[0])
						+ (self.pos.centerx * self.pos.centerx))
					y_sqr = ((point[1] * point[1])
						- (2.0 * self.pos.centery * point[1])
						+ (self.pos.centery * self.pos.centery))
					if math.sqrt(x_sqr + y_sqr) < self.pos.w / 2.0:
						return True
					else:
						return False

				def test_collide():
					test = testpoint(playerpos.topleft)
					test = test or testpoint(playerpos.bottomleft)
					test = test or testpoint(playerpos.topright)
					test = test or testpoint(playerpos.bottomright)
					return test
				if test_collide():
					#Warps to the selected world and gets a bit pushed off the station
					selected_num = menu.choose_world()
					if selected_num >= 0:
						settings.world = settings.localmap[selected_num]
						settings.world.adjust_to_screen()
					settings.player.up = False
					settings.player.down = False
					settings.player.left = False
					settings.player.right = False
					settings.up = False
					settings.down = False
					settings.left = False
					settings.right = False
					while test_collide():
						if settings.player.pos.center[0] < self.pos.center[0]:
							settings.player.move_ip(-20, 0)
						else:
							settings.player.move_ip(20, 0)
						if settings.player.pos.center[1] < self.pos.center[1]:
							settings.player.move_ip(0, -20)
						else:
							settings.player.move_ip(0, 20)
						playerpos = settings.player.pos

			def blit(self):
				self.screen.blit(self.img, self.pos)

		self.warp1 = warp()

		self.adjust_to_screen()

	def move(self):
		"""Move everything in the world."""
		player_pos = settings.player.pos

		self.background_pos.left = int(-(settings.player.rel_x * (
			settings.screenx_current * (settings.fake_size - 1))))
		self.background_pos.top = int(-(settings.player.rel_y * (
			settings.screeny_current * (settings.fake_size - 1))))

		self.warp1.move(player_pos)
		self.warp1.test(player_pos)

		for star in self.stars:
			star.move(player_pos.left, player_pos.top)

		for bullet in settings.bullets:
			bullet.move(player_pos)
			if not bullet.pos.colliderect(self.background_pos):
				settings.bullets.remove(bullet)

		for target in self.targets:
			target.move(player_pos.left, player_pos.top)
			for bullet in settings.bullets:
				target.test_ishit(bullet.pos)
			if target.gothit:
				self.targets.remove(target)
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
		settings.objects_on_screen = 0
		for star in self.stars:
			isdisplayed = star.blitstar()
			if isdisplayed:
				settings.objects_on_screen += 1
		for bullet in settings.bullets:
			isdisplayed = bullet.blit()
			if isdisplayed:
				settings.objects_on_screen += 1
		for target in self.targets:
			isdisplayed = target.blit()
			if isdisplayed:
				settings.objects_on_screen += 1
		for explosion in settings.explosions_disp:
			explosion.blit()
		self.warp1.blit()

	def adjust_to_screen(self):

		tmpx = settings.screenx_current * settings.fake_size
		tmpy = settings.screeny_current * settings.fake_size
		screen_current = (int(tmpx), int(tmpy))
		background = pygame.image.load("./assets/sprites/Background2.tif").convert()
		self.background = pygame.transform.smoothscale(background, screen_current)
		self.background_pos = self.background.get_rect()

		tmp = -(settings.player.pos.x * (settings.screenx_current *
					(settings.fake_size - 1)))
		self.background_pos.left = int(tmp)
		tmp = -(settings.player.pos.y * (settings.screeny_current *
					(settings.fake_size - 1)))
		self.background_pos.top = tmp

		draw.no16to9 = False
		if settings.aspect_ratio != 16.0 / 9:
			draw.no16to9 = True
			delta_screeny = settings.screeny - settings.screeny_current
			draw.correcture = pygame.Surface((settings.screenx, delta_screeny))
			draw.correcture_pos = draw.correcture.fill((0, 0, 0))
			draw.correcture_pos.bottomleft = (0, settings.screeny)

		for star in self.stars:
			star.update(settings.screenx_current / 1920.0)

		for target in self.targets:
			target.update()

		self.warp1.update()