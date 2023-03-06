import pygame, copy, random
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("bg_music.ogg")
pygame.display.set_caption("Run Box run!")
win = pygame.display.set_mode((800, 420))
bg_img = pygame.image.load('bg_img.jpg').convert()
text = pygame.font.SysFont("Helvetica", 18)

red = (255, 0, 0)
green = (0, 150, 0)

class Player:
	""" Player Class """
	def __init__(self):
		self.x = 200
		self.y = 330
		self.color = red
		self.width = 40
		self.height = 40
		self.vel = 0
		self.jump_count = 0

	def display(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

	def move(self):
		self.jump_count += 1
		self.y += self.vel

		if self.jump_count == -4:
			self.vel = -5
		if self.jump_count == 0:
			self.jump_count = 1
			self.vel = 5
			return

		if self.jump_count == 5:
			self.vel = 10
		if self.y == 330: # initial position of player on ground level
			self.vel = 0
			self.jump_count = -10


class Rectangle:
	""" Obstacle class: They are rectangular in shape """
	def __init__(self, x, y, width, height, is_floating=False):
		self.x = x
		self.y = y
		self.color = green
		self.width = width
		self.height = height
		self.is_floating = is_floating # If obstacle is floating above the platform

	def display(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


class Triangle:
	""" Spike Class: The spikes are triangular in shape """
	def __init__(self, x, y, width):
		self.x = x # X coordinate at the left base corner
		self.y = y # Y coordinate also at the left base corner
		self.width = width
		self.height = width
		self.apex_x = x + (self.width//2) # X coordinate of the triangle's apex
		self.apex_y = y - self.height # Y coordinate of the triangle's apex
		self.right_base_corner = x+width
		self.color = green

	def display(self):
		pygame.draw.polygon(win, self.color, ((self.x, self.y), (self.apex_x, self.apex_y), (self.right_base_corner, self.y)))


class Platform():
	"""
		Obstacles, spikes and the Player will all be positioned directly on top of the platform
		or at a certain distance above the platform
	"""
	def __init__(self):
		self.x = 0
		self.y = 370
		self.color = green
		self.width = 800
		self.height = 50
		self.vel = 10
		# List of all the possible obstacles
		self.obstacles_list = [Rectangle(800, 330, 80, 40), Rectangle(800, 330, 120, 40), Rectangle(800, 290, 80, 80),
							   Rectangle(800, 290, 80, 80), Rectangle(800, 250, 80, 40, True), Rectangle(800, 250, 120, 120), 
							   Rectangle(800, 250, 80, 120), Rectangle(800, 210, 80, 40, True), Rectangle(800, 290, 120, 80)]

		# List to store both Obstacles and Spikes on screen
		self.obstacles_onscreen = [Triangle(640, 370, 20), Triangle(660, 370, 20),
								   Triangle(680, 370, 20), Rectangle(700, 330, 80, 40)]
		self.obstacle_under_box = None
		self.next_obstacle = None # Next obstacle to be appended to obstacles_onscreen
		self.game_over = False
		self.score = 0
		self.game_paused = False

	def display(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

	def move_and_display_obstacles(self):
		for obst in self.obstacles_onscreen[:]:
			if obst.x + obst.width <= 0:
				if type(obst) == Rectangle:
					platform.score += 1
				platform.obstacles_onscreen.remove(obst)
				continue

			obst.display()
			self.check_for_collisions(obst)
			if type(obst) == Triangle:
				obst.x -= platform.vel
				obst.apex_x -= platform.vel
				obst.right_base_corner -= platform.vel
			else:
				obst.x -= platform.vel


	def check_for_collisions(self, obstacle):
		""" Checks for collisions between an Obstacle and a Player """
		if type(obstacle) == Rectangle:
			if box.vel > 0:
				if box.y + box.height == obstacle.y:
					# if player lands on rectangular obstacle, It should stop and stay on the obstacle
					if box.x + box.width >= obstacle.x and obstacle.x + obstacle.width >= box.x:
						platform.obstacle_under_box = obstacle
						return

			# if player collides with rectangular obstacle
			if box.y + box.height > obstacle.y and obstacle.y + obstacle.height > box.y:
				if obstacle.x == box.x + box.width:
					game_over()

		else:	
			if box.y + 40 >= obstacle.apex_y:
				if box.vel == 0 and box.x + box.width == obstacle.x: # if player collides with spikes
					game_over()
				if box.x + box.width >= obstacle.apex_x and obstacle.apex_x > box.x: # if player lands on spikes
					game_over()


def createSpikes(no_of_spikes, last_obst):
	""" 
		A certain amount of distance needs to be between different types of obstacles.
		Spikes fill that distance. Each spike is 20px wide so the no_of_spikes param is the no
		of spikes needed to fill up a particular distance 
	"""
	spike_x = last_obst.x + last_obst.width
	for no in range(0, no_of_spikes):
		spike = Triangle(spike_x, 370, 20)
		spike = copy.copy(spike)
		platform.obstacles_onscreen.append(spike)
		# Position the next spike directly after the last obstacle or spike on screen
		spike_x = platform.obstacles_onscreen[-1].x + platform.obstacles_onscreen[-1].width

def create_next_obstacle():
	obstacle = random.choice(platform.obstacles_list)
	platform.next_obstacle = copy.copy(obstacle)

	# if the next obstacle is lower than the last obstacle on screen with 40px
	if (obstacle.y - 40) == platform.obstacles_onscreen[-1].y:
		if obstacle.is_floating:
			# fills up the empty space under the floating obstacle with a number of 
			# spikes gotten from obstacle.width//20 since a spike has a base width of 20px.
			createSpikes(2 + obstacle.width//20, platform.obstacles_onscreen[-1])
		else:
			createSpikes(2, platform.obstacles_onscreen[-1])

	# if the next obstacle is higher than the last obstacle on screen with 40px
	elif obstacle.y == (platform.obstacles_onscreen[-1].y - 40):
		if obstacle.is_floating:
			createSpikes(5 + obstacle.width//20, platform.obstacles_onscreen[-1])
		else:
			createSpikes(5, platform.obstacles_onscreen[-1])

	# if the next obstacle and the last obstacle on screen are of same height above the platform
	elif obstacle.y == platform.obstacles_onscreen[-1].y:
		if obstacle.is_floating:
			createSpikes(7 + obstacle.width//20, platform.obstacles_onscreen[-1])
		else:
			createSpikes(7, platform.obstacles_onscreen[-1])

	else:
		create_next_obstacle()

def createObstaclesAndSpikes():
	create_next_obstacle()
	if platform.next_obstacle.is_floating:
		# no of spikes that were just added to obstacles_onscreen, the negative value will be used as an index
		# to get the first spike from the set of spikes that were just added to platform.obstacles_onscreen
		index = platform.next_obstacle.width//20
		
		# Setting their x coordinates to the same value will make platform.next_obstacle float 
		# over all spikes that were just added to obstacles_onscreen when they are rendered.
		platform.next_obstacle.x = platform.obstacles_onscreen[-index].x
	else:
		# Positions next obstacle directly after the last obstacle on screen
		platform.next_obstacle.x = platform.obstacles_onscreen[-1].x + platform.obstacles_onscreen[-1].width
	platform.obstacles_onscreen.append(platform.next_obstacle)
	platform.next_obstacle = None

# Resets all the important game values to default when called
def reset():
	pygame.mixer.music.play(-1, 0, 0)
	platform.__init__()
	box.__init__()

def display_msg(text1, text2):
	pygame.draw.rect(win, (255, 255, 255), (300, 50, 200, 100))
	pygame.draw.rect(win, green, (300, 50, 200, 30))
	win.blit(text.render(text1, False, red), (350, 55))
	win.blit(text.render(text2, True, green), (310, 100))

def game_over():
	pygame.mixer.music.stop()
	platform.game_over = True
	box.vel = 0
	platform.vel = 0
	display_msg("GAME OVER!", "Press SPACE to play again")

def pause_game(bool):
	platform.game_paused = True
	pygame.mixer.music.pause()
	platform.vel = 0

def resume_game():
	platform.game_paused = False
	pygame.mixer.music.unpause()
	platform.vel = 10
	

box = Player()
platform = Platform()
run = True
i = 0 # X coordinate of first background image
pygame.mixer.music.play(-1, 0, 0)

while run:
	pygame.time.delay(22)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and (platform.obstacle_under_box or box.vel == 0):
				if not platform.game_over and not platform.game_paused:
					box.vel = -10
					box.jump_count = -10
			if event.key == pygame.K_SPACE:
				if platform.game_over:
					reset()
				else:
					if not platform.game_paused:
						pause_game()
					else:
						resume_game()

	win.fill((0, 0, 0))
	win.blit(bg_img, (i, 0)) # Moving first background image to produce the illusion of moving player
	win.blit(bg_img, (800+i, 0)) # Moving second background image to produce the illusion of moving player 
	win.blit(text.render("SCORE: " + str(platform.score), True, green), (700, 10))
	box.display()
	platform.display()
	if platform.game_paused:
		display_msg("GAME PAUSED!", "Press SPACE to resume")

	if not platform.game_over and not platform.game_paused:
		if i == -800:
			i = 0
		i -= platform.vel

		if not platform.obstacle_under_box:
			box.move()

		if platform.obstacles_onscreen[-1].x < 800:
			createObstaclesAndSpikes()
	platform.move_and_display_obstacles()


	if platform.obstacle_under_box:
		# if the player is no longer on an obstacle
		if platform.obstacle_under_box.x + platform.obstacle_under_box.width < box.x:
			platform.obstacle_under_box = None

	pygame.display.flip()
pygame.quit()
