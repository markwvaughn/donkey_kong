from globals import *
import pygame

class Score():

	def __init__(self):
		self.highscores = []
		self.getScores()
		self.slide_duration = 100
		self.current_slide = 0
		self.slide_x = 500

	def getScores(self):
		scores_file = open("data/highscores.txt", 'r')
		
		for score in scores_file:
			h1, h2 = score.split(':')

			h1 = h1.lstrip().rstrip()
			h2 = h2.lstrip().rstrip()

			self.highscores.append((h1,h2))

		scores_file.close()

	def addScore(self, name, score):
		self.highscores.append((name, score))

	def getHighScore(self):
		max_score = 0
		name = ""
		for score in self.highscores:
			if int(score[1]) > max_score:
				max_score = int(score[1])
				name = score[0]

		return (name, max_score)

	def saveScores(self):
		scores_file = open("data/highscores.txt", 'w')
		
		score_text = ""

		sorted_scores = []

		for i in range(len(self.highscores)):
			j = i
			for j in range(len(self.highscores)):
				if int(self.highscores[i][1]) > int(self.highscores[j][1]):
					t = copy.deepcopy(self.highscores[i])
					self.highscores[i] = self.highscores[j]
					self.highscores[j] = t

		for score in self.highscores:
			score_text += "%s:%s\n" % (score[0], score[1])

		scores_file.write(score_text)
		scores_file.close()

	def displayScores(self, surface, dt):
		if self.current_slide >= 5:
			self.current_slide = 0

		self.slide_x -= 2.5

		if self.slide_x + 160 < 0:
			self.slide_x = globals.WIDTH
			self.current_slide += 1

		i = 0
		while i < 5:
			if i == self.current_slide:
				thescore = globals.pixel_font30.render("%s %s" % (self.highscores[i][0], self.highscores[i][1]), 1, (230,50,50))
				surface.blit(thescore, (self.slide_x, 10))
			i += 1

	def displayAllScores(self, surface, dt, score_index):
		x = 100
		y = 200
		spacing = 0

		begin = score_index
		end = score_index + 5

		if end > len(self.highscores):
			end = len(self.highscores)

		while begin < end:		
			thescore = globals.pixel_font30.render("%s %s" % (self.highscores[begin][0], self.highscores[begin][1]), 1, (230,50,50))
			width = thescore.get_bounding_rect()[2]
			surface.blit(thescore, (globals.WIDTH/2.0 - (width / 2.0), y + spacing))
			spacing += 50
			begin += 1
