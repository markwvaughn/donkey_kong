from object import *
from globals import *

class LevelOne():

	def __init__(self):
		self.platforms = []
		self.ladders = []
		self.barrel = None
		self.lines = []
		self.ladderlines = []

		self.aesthetic_lines = []

	def platform_lines(self):
		
		# LEVEL 1
		p1 = (0, HEIGHT-20)
		p2 = (WIDTH * 0.5, HEIGHT-20)

		p3 = (WIDTH * 0.5, HEIGHT-20)
		p4 = (WIDTH, HEIGHT-30)

		line_group_1 = []
		line_group_1.append((p1,p2))
		line_group_1.append((p3,p4))
		self.lines.append(line_group_1)

		# LEVEl 2
		p5 = (WIDTH - 70, HEIGHT-80)
		p6 = (0, HEIGHT-100)

		line_group_2 = []
		line_group_2.append((p5,p6))
		self.lines.append(line_group_2)

		# LEVEl 3
		p7 = (70, HEIGHT-150)
		p8 = (WIDTH, HEIGHT-180)

		line_group_3 = []
		line_group_3.append((p7,p8))
		self.lines.append(line_group_3)

		# LEVEl 4
		p9 = (WIDTH - 70, HEIGHT-240)
		p10 = (0, HEIGHT-260)

		line_group_4 = []
		line_group_4.append((p9,p10))
		self.lines.append(line_group_4)

		# LEVEl 5
		p11 = (70, HEIGHT-310)
		p12 = (WIDTH, HEIGHT-340)

		line_group_5 = []
		line_group_5.append((p11,p12))
		self.lines.append(line_group_5)

		# LEVEL 6 - DK Platform
		p13 = (WIDTH - 70, HEIGHT-390)
		p14 = (WIDTH * 0.5, HEIGHT-400)

		p15 = (0, HEIGHT-400)
		p16 = (WIDTH * 0.50, HEIGHT-400)

		line_group_6 = []
		line_group_6.append((p13,p14))
		line_group_6.append((p15,p16))
		self.lines.append(line_group_6)

		# LEVEL 7 (Princess Platform)
		p17 = (WIDTH * 0.5 - 110, HEIGHT-460)
		p18 = (WIDTH * 0.5 - 10, HEIGHT-460)

		line_group_7 = []
		line_group_7.append((p17,p18))
		self.lines.append(line_group_7)

	def ladder_lines(self):

		# LEVEL 1
		# Full Ladder 1
		p1 = (WIDTH * 0.8, HEIGHT * 0.815)
		p2 = (WIDTH * 0.8, HEIGHT * 0.954)

		self.ladderlines.append((p1,p2))

		# LEVEL 2
		# Full Ladder 2
		p3 = (WIDTH * 0.5, HEIGHT * 0.69)
		p4 = (WIDTH * 0.5, HEIGHT * 0.855)

		self.ladderlines.append((p3,p4))
		
		# Full Ladder 3
		p5 = (WIDTH * 0.2, HEIGHT * 0.70)
		p6 = (WIDTH * 0.2, HEIGHT * 0.85)

		self.ladderlines.append((p5,p6))

		# LEVEL 3
		# Full Ladder 4
		p7 = (WIDTH * 0.58, HEIGHT * 0.74)
		p8 = (WIDTH * 0.58, HEIGHT * 0.56)

		self.ladderlines.append((p7,p8))
		
		# Full Ladder 5
		p9 = (WIDTH * 0.75, HEIGHT * 0.73)
		p10 = (WIDTH * 0.75, HEIGHT * 0.565)

		self.ladderlines.append((p9,p10))

		# LEVEL 4
		# Full Ladder 6
		p11 = (WIDTH * 0.4, HEIGHT * 0.44)
		p12 = (WIDTH * 0.4, HEIGHT * 0.605)

		self.ladderlines.append((p11,p12))
		
		# Full Ladder 7
		p13 = (WIDTH * 0.2, HEIGHT * 0.455)
		p14 = (WIDTH * 0.2, HEIGHT * 0.595)

		self.ladderlines.append((p13,p14))

		# LEVEL 5
		# Full Ladder 8
		p15 = (WIDTH * 0.80, HEIGHT * 0.330)
		p16 = (WIDTH * 0.80, HEIGHT * 0.475)

		self.ladderlines.append((p15,p16))
		

		# LEVEL 6
		# Full Ladder 9
		p17 = (WIDTH * 0.46, HEIGHT * 0.22)
		p18 = (WIDTH * 0.46, HEIGHT * 0.37)

		self.ladderlines.append((p17,p18))

	def aesthetics(self):
		p1 = (WIDTH * 0.2, HEIGHT * 0.24)
		p2 = (WIDTH * 0.2, 0)

		p3 = (WIDTH * 0.15, HEIGHT * 0.24)
		p4 = (WIDTH * 0.15, 0)

		self.aesthetic_lines.append((p1,p2))
		self.aesthetic_lines.append((p3,p4))

	def create(self):

		self.platform_lines()
		self.ladder_lines()

		for line_group in self.lines:

			for line in line_group:

				min_x = line[0][0]
				max_x = line[1][0]
				if line[1][0] < min_x:
					min_x = line[1][0]
					max_x = line[0][0]

				step_x = 20

				m 	= (line[1][1] - line[0][1]) / float(line[1][0] - line[0][0])
				y1 	= line[0][1]
				b 	= y1 - (m * line[0][0])

				while min_x < max_x:
					y = (m * min_x) + b

					self.platforms.append(Object(Vector((min_x, y)), Vector((0,0)), Vector((0,0)), red_platform_an))

					min_x += step_x

		for line in self.ladderlines:
			min_y = line[0][1]
			max_y = line[1][1]
			if line[1][1] < min_y:
				min_y = line[1][1]
				max_y = line[0][1]

			step_y = 16
			x = line[1][0]

			max_y = max_y - 16

			while max_y > min_y + 32:

				self.ladders.append(Object(Vector((x - 8, max_y)), Vector((0,0)), Vector((0,0)), white_ladder_middle_an))

				max_y -= step_y


	def update(self):
		pass


	def draw_bonus_display(self, surface):
		bonus = pixel_font30.render("BONUS", 1, (230,50,50))
		surface.blit(bonus, (WIDTH*0.755, 20))

		y1 = 30
		y2 = y1 + 50

		# BOX
		pygame.draw.line(surface, (255,255,255), (WIDTH*0.72, y1), (WIDTH*0.74, y1), 2) # Top Left
		pygame.draw.line(surface, (255,255,255), (WIDTH*0.88, y1), (WIDTH*0.90, y1), 2) # Top Right
		pygame.draw.line(surface, (255,255,255), (WIDTH*0.72, y1), (WIDTH*0.72, y2), 2) # Left
		pygame.draw.line(surface, (255,255,255), (WIDTH*0.90, y1), (WIDTH*0.90, y2), 2) # Right
		pygame.draw.line(surface, (255,255,255), (WIDTH*0.72, y2), (WIDTH*0.90, y2), 2) # Bottom

		bonus_rect = pygame.Rect((WIDTH*0.73, 45), (78, 32))
		pygame.draw.rect(surface, (230,50,50), bonus_rect, 2)

		# SCORE
		bonus_score = pixel_font30.render(str(int(globals.time_bonus)).zfill(4), 1, (255,255,255))
		surface.blit(bonus_score, (WIDTH*0.77, 45))



	def draw_hud(self, surface):
		self.draw_bonus_display(surface)

		# HIGH SCORE
		high_score_title = pixel_font30.render("HIGH SCORE", 1, (230,50,50))
		surface.blit(high_score_title, (WIDTH*0.35, 20))

		high_score_text = pixel_font30.render(str(Score().getHighScore()[1]).zfill(6), 1, (255,255,255))
		surface.blit(high_score_text, (WIDTH*0.35, 40))

		# CURRENT_PLAYER
		current_player_title = pixel_font30.render("1UP", 1, (230,50,50))
		surface.blit(current_player_title, (WIDTH*0.05, 20))

		# CURRENT SCORE
		current_score = pixel_font30.render(str(globals.score).zfill(6), 1, (255,255,255))
		surface.blit(current_score, (WIDTH*0.05, 40))

		# NUMBER OF LIVES
		for i in range(globals.mario_num_lives):
			spacing = i * 30
			surface.blit(mario_life_s, pygame.Rect(20 + spacing, 70, 25, 25), mario_life_s.get_rect())


	def destroy_platform(self, dt):
		pass

	def draw(self, surface):

		for platform in self.platforms:
			platform.draw(surface)
		
		for ladder in self.ladders:
			ladder.draw(surface)

		self.draw_hud(surface)

		# self.aesthetic_lines

		# for line_group in self.lines:
		# 	for line in line_group:
		# 		pygame.draw.line(surface, (255,0, 0), line[0], line[1], 1)

		# for line in self.ladderlines:
		# 	pygame.draw.line(surface, (0,255, 0), line[0], line[1], 1)


		# self.barrel.draw(surface)