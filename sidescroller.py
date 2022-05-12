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
		self.vel = 10
		self.acc_up = False # variable to control upward acceleration when jumping
		self.acc_down = False # variable to control downward acceleration when jumping
		self.init_pos = 0 # initial position before jumping up
		self.on_top_obstacle = False

	def display(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

	def reset(self):
		""" Resets all the attributes of player to default after new game starts """
		self.x = 200
		self.y = 330
		self.vel = 10
		self.acc_up = False
		self.acc_down = False
		self.init_pos = 0
		self.on_top_obstacle = False


class Rectangle:
	""" Obstacle class: They are rectangular in shape """
	def __init__(self, x, y, width, height, is_floating=False):
		self.x = x
		self.y = y
		self.color = green
		self.width = width
		self.height = height
		self.is_floating = is_floating # If obstacle is floating above the above the platform

	def display(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


class Triangle:
	""" Spike Class: The spikes are triangular in shape """
	def __init__(self, x, y, width):
		self.x = x # X coordinate at the left base corner
		self.y = y # Y coordinate at the left base corner
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
		All the obstacles, spikes and the player will be positioned directly on top of the platform
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
	if (obstacle.y - 40) == platform.obstacles_onscreen[-1].y:
		if obstacle.is_floating:
			# fills up the empty space under the floating obstacle with spikes
			createSpikes(2 + obstacle.width//20, platform.obstacles_onscreen[-1])
		else:
			createSpikes(2, platform.obstacles_onscreen[-1])

	elif obstacle.y == (platform.obstacles_onscreen[-1].y - 40):
		if obstacle.is_floating:
			createSpikes(5 + obstacle.width//20, platform.obstacles_onscreen[-1])
		else:
			createSpikes(5, platform.obstacles_onscreen[-1])

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
		index = platform.next_obstacle.width//20
		platform.next_obstacle.x = platform.obstacles_onscreen[-index].x
	else:
		# Positions next obstacle directly after the last obstacle on screen
		platform.next_obstacle.x = platform.obstacles_onscreen[-1].x + platform.obstacles_onscreen[-1].width
	platform.obstacles_onscreen.append(platform.next_obstacle)
	platform.next_obstacle = None

# Resets all the important game values to default when called
def reset():
	pygame.mixer.music.play(-1, 0, 0)
	platform.obstacles_onscreen = [Triangle(640, 370, 20), Triangle(660, 370, 20),
								   Triangle(680, 370, 20), Rectangle(700, 330, 80, 40)]
	platform.next_obstacle = None
	platform.obstacle_under_box = None
	platform.game_over = False
	box.reset()
	platform.vel = 10
	platform.score = 0

def display_game_over_msg():
	pygame.draw.rect(win, (255, 255, 255), (350, 10, 230, 150))
	pygame.draw.rect(win, green, (350, 10, 230, 30))
	win.blit(text.render("GAME OVER!", False, red), (370, 20))
	win.blit(text.render("Press SPACE to play again", True, green), (360, 50))

def game_over():
	pygame.mixer.music.stop()
	platform.game_over = True
	box.vel = 0
	platform.vel = 0
	display_game_over_msg()

def pause_game():
	platform.game_paused = True
	pygame.mixer.music.pause()
	platform.vel = 0

def resume_game():
	platform.game_paused = False
	pygame.mixer.music.unpause()
	platform.vel = 10

def display_paused_game_msg():
	pygame.draw.rect(win, (255, 255, 255), (300, 50, 200, 100))
	pygame.draw.rect(win, green, (300, 50, 200, 30))
	win.blit(text.render("GAME PAUSED!", False, red), (320, 50))
	win.blit(text.render("Press SPACE to resume", True, green), (310, 100))

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
			if event.key == pygame.K_UP and not box.acc_down and not box.acc_up:
				if not platform.game_over and not platform.game_paused:
					box.init_pos = box.y
					box.acc_up = True # Make the player jump up 
			if event.key == pygame.K_SPACE:
				if platform.game_over:
					reset()
				else:
					if not platform.game_paused:
						pause_game()
					else:
						resume_game()

	win.fill((0, 0, 0))
	win.blit(bg_img, (i, 0)) # Moving first background image to give the illusion of moving player
	win.blit(bg_img, (800+i, 0)) # Moving second background image to give the illusion of moving player 
	win.blit(text.render("SCORE: " + str(platform.score), True, green), (700, 10))
	box.display()
	platform.display()
	if platform.game_paused:
		display_paused_game_msg()

	if not platform.game_over and not platform.game_paused:
		if i == -800:
			i = 0
		i -= platform.vel

		if box.acc_up: # if player is accelerating upwards during jump
			box.y -= box.vel
			if box.y == box.init_pos - 60:
				box.vel = 5 # reduce speed as player approaches maximum jump height
			if box.y == box.init_pos - 80: # Maximum jump height
				box.init_pos = box.y
				box.acc_down = True
				box.acc_up = False
		elif box.acc_down: # if player is accelerating downwards during jump
			box.y += box.vel
			if box.y == box.init_pos + 20:
				box.vel = 10 # increase speed after some distance after certain distance
			if box.y == 330: # initial position of player on ground level
				box.init_pos = box.y
				box.acc_up = False
				box.acc_down = False

		if platform.obstacles_onscreen[-1].x < 800:
			createObstaclesAndSpikes()
	
	# Moving obstacles on screen
	for obst in platform.obstacles_onscreen[:]:
		obst.display()
		if type(obst) == Triangle:
			obst.x -= platform.vel
			obst.apex_x -= platform.vel
			obst.right_base_corner -= platform.vel
		else:
			obst.x -= platform.vel

	# If an obstacle has left the viewport, It should be removed from the list
	for obst in platform.obstacles_onscreen[:]:
		if obst.x + obst.width <= 0:
			if type(obst) == Rectangle:
				platform.score += 1
			platform.obstacles_onscreen.remove(obst)

	for obst in platform.obstacles_onscreen[:]:
		if type(obst) == Rectangle:
			if box.acc_down:
				if box.y + 40 == obst.y:
					# if player lands on rectangular obstacle, It should stop and stay on the obstacle
					if box.x in range(obst.x, obst.x + obst.width+1) or obst.x in range(box.x, box.x + box.width+1):
						box.acc_down = False
						platform.obstacle_under_box = obst

			# if player collides with rectangular obstacle
			if box.y in range(obst.y, obst.y + obst.height+1) or obst.y in range(box.y, box.y + box.height+1):
				if obst.x == box.x + box.width:
					game_over()
		else:
			# if player collides with spikes
			if obst.apex_y in range(box.y, box.y + box.height):
				if obst.x == box.x + box.width and not box.acc_up:
					game_over()

			# if player lands on spikes
			if obst.apex_x in range(box.x, box.x + box.width+1):
				if box.y + 40 >= obst.apex_y:
					game_over()

	if platform.obstacle_under_box:
		# if the player is no longer on an obstacle
		if platform.obstacle_under_box.x + platform.obstacle_under_box.width < box.x:
			box.acc_down = True # Player should fall down
			platform.obstacle_under_box = None

	pygame.display.flip()
pygame.quit()
