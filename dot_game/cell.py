import pygame
def distance(p1, p2):
	return ((p1[0]-p2[0])**2 + (p1[1] - p2[1])**2)**0.5

class Cell:
	def __init__(self, x, y, cell, isBorder = False):
		self.x = x
		self.y = y 
		self.cell = cell
		self.edges = [0, 0, 0, 0] # top, right, bottom, left
		self.filled = False
		self.player = None
		self.isBorder = isBorder
	
	def update(self, mouse, curr_player):


		top = (self.x+self.cell//2, self.y)
		bottom = (self.x+self.cell//2, self.y+ self.cell)
		left = (self.x, self.y + self.cell//2)
		right = (self.x + self.cell, self.y+self.cell//2)

		bounding_radius = self.cell//4
		nextplayer = curr_player

		if distance(mouse, top) <= bounding_radius and self.edges[0] == 0:
			self.edges[0] = 1
			nextplayer = (curr_player+1)%2 if self.isBorder else curr_player


		if distance(mouse, right) <= bounding_radius and self.edges[1] == 0:
			self.edges[1] = 1
			nextplayer = (curr_player+1)%2


		if distance(mouse, bottom) <= bounding_radius and self.edges[2] == 0:
			self.edges[2] = 1
			nextplayer = (curr_player+1)%2

		if distance(mouse, left) <= bounding_radius and self.edges[3] == 0:
			self.edges[3] = 1
			nextplayer = (curr_player+1)%2 if self.isBorder else curr_player

		if not self.filled and all(self.edges):
			self.filled = True
			self.player = curr_player
			nextplayer = self.player 

		return nextplayer



	def draw(self, gameDisplay):
		width = 3

		x, y, cell = self.x, self.y, self.cell

		if self.filled:
			if self.player == 0:
				color = (150, 0, 0, 50)
			else:
				color = (0, 0, 150, 50)

			pygame.draw.rect(gameDisplay, color, [x, y, cell, cell])

		if self.edges[0] == 1:
			pygame.draw.line(gameDisplay, (255, 255, 255), (x, y), (x + cell, y), width)

		if self.edges[1] == 1:
			pygame.draw.line(gameDisplay, (255, 255, 255), (x+ cell, y), (x + cell, y + cell), width)

		if self.edges[2] == 1:
			pygame.draw.line(gameDisplay, (255, 255, 255), (x , y+cell), (x + cell, y + cell), width)
		
		if self.edges[3] == 1:
			pygame.draw.line(gameDisplay, (255, 255, 255),  (x, y), (x, y+ cell), width)
