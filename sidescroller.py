import pygame, copy, random
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("bg_music.ogg")
pygame.display.set_caption("Run Box run!")
win = pygame.display.set_mode((800, 420))
bg_img = pygame.image.load('bg_img.jpg').convert()
text = pygame.font.SysFont("Helvetica", 18)
clock = pygame.time.Clock()

red = (255, 0, 0)
green = (106, 231, 127)

class Player:
	def __init__(self):
		self.x = 200
		self.y = 330
		self.color = red
		self.width = 40
		self.height = 40
		self.vel = 10
		self.acc_up = False
		self.acc_down = False
		self.init_pos = 0
		self.on_top_obstacle = False

	def display(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

	def reset(self):
		self.x = 200
		self.y = 330
		self.vel = 10
		self.acc_up = False
		self.acc_down = False
		self.init_pos = 0
		self.on_top_obstacle = False


class Rectangle:
	"""This is an Obstacle class"""
	def __init__(self, x, y, width, height, is_floating=False):
		self.x = x
		self.y = y
		self.color = green
		self.width = width
		self.height = height
		self.is_floating = is_floating

	def display(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


class Triangle:
	"""This is an Obstacle class"""
	def __init__(self, x, y, width):
		self.x = x
		self.y = y
		self.width = width
		self.height = width
		self.apex_x = x + (self.width//2)
		self.apex_y = y - self.height
		self.right_base_corner = x+width
		self.color = green

	def display(self):
		pygame.draw.polygon(win, self.color, ((self.x, self.y), (self.apex_x, self.apex_y), (self.right_base_corner, self.y)))

class Platform():
	def __init__(self):
		self.x = 0
		self.y = 370
		self.color = green
		self.width = 800
		self.height = 50
		self.obstacles_vel = 10
		self.obstacles_list = [Rectangle(800, 330, 80, 40), Rectangle(800, 330, 120, 40), Rectangle(800, 290, 80, 80),
							   Rectangle(800, 290, 80, 80), Rectangle(800, 250, 80, 40, True), Rectangle(800, 250, 120, 120), 
							   Rectangle(800, 250, 80, 120), Rectangle(800, 210, 80, 40, True), Rectangle(800, 290, 120, 80)]
		self.obstacles_onscreen = [Triangle(640, 370, 20), Triangle(660, 370, 20),
								   Triangle(680, 370, 20), Rectangle(700, 330, 80, 40)]
		self.obstacle_under_box = None
		self.next_obstacle = None
		self.game_over = False
		self.score = 0

	def display(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

box = Player()
platform = Platform()

def createSpikes(no_of_spikes, last_obst):
	spike_x = last_obst.x + last_obst.width
	for no in range(0, no_of_spikes):
		spike = Triangle(spike_x, 370, 20)
		spike = copy.copy(spike)
		platform.obstacles_onscreen.append(spike)
		spike_x = platform.obstacles_onscreen[-1].x + platform.obstacles_onscreen[-1].width

def create_next_obstacle():
	obstacle = random.choice(platform.obstacles_list)
	platform.next_obstacle = copy.copy(obstacle)
	if (obstacle.y - 40) == platform.obstacles_onscreen[-1].y:
		if obstacle.is_floating:
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

def reset():
	platform.obstacles_onscreen =[Triangle(640, 370, 20), Triangle(660, 370, 20),
								   Triangle(680, 370, 20), Rectangle(700, 330, 80, 40)]
	platform.next_obstacle = None
	platform.obstacle_under_box = None
	platform.game_over = False
	box.reset()
	platform.obstacles_vel = 10


def createObstaclesAndSpikes():
	create_next_obstacle()
	if platform.next_obstacle.is_floating:
		index = platform.next_obstacle.width//20
		platform.next_obstacle.x = platform.obstacles_onscreen[-index].x
	else:
		platform.next_obstacle.x = platform.obstacles_onscreen[-1].x + platform.obstacles_onscreen[-1].width
	platform.obstacles_onscreen.append(platform.next_obstacle)
	platform.next_obstacle = None

run = True
i = 0
pygame.mixer.music.play(-1, 0, 0)

while run:
	pygame.time.delay(22)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and not box.acc_down and not box.acc_up:
				if not platform.game_over:
					box.init_pos = box.y
					box.acc_up = True
			if event.key == pygame.K_DOWN:
				reset()

	win.fill((0, 0, 0))
	win.blit(bg_img, (i, 0))
	win.blit(bg_img, (800+i, 0))
	win.blit(text.render("SCORE: " + str(platform.score), True, (0, 255, 0)), (700, 10))
	box.display()
	platform.display()

	if box.acc_up:
		box.y -= box.vel
		if box.y == box.init_pos - 60:
			box.vel = 5
		if box.y == box.init_pos - 80:
			box.init_pos = box.y
			box.acc_down = True
			box.acc_up = False
	elif box.acc_down:
		box.y += box.vel
		if box.y == box.init_pos + 20:
			box.vel = 10
		if box.y == 330:
			box.init_pos = box.y
			box.acc_up = False
			box.acc_down = False

	if not platform.game_over:
		if i == -800:
			i = 0
		i -= 10
		if platform.obstacles_onscreen[-1].x < 800:
			createObstaclesAndSpikes()
			
	for obst in platform.obstacles_onscreen[:]:
		obst.display()
		if type(obst) == Triangle:
			obst.x -= platform.obstacles_vel
			obst.apex_x -= platform.obstacles_vel
			obst.right_base_corner -= platform.obstacles_vel
		else:
			obst.x -= platform.obstacles_vel

	for obst in platform.obstacles_onscreen[:]:
		if obst.x + obst.width <= 0:
			if type(obst) == Rectangle:
				platform.score += 1
			platform.obstacles_onscreen.remove(obst)

	for obst in platform.obstacles_onscreen[:]:
		if type(obst) == Rectangle:
			if box.acc_down:
				if box.y + 40 == obst.y:
					if box.x in range(obst.x, obst.x + obst.width) or obst.x in range(box.x, box.x + box.width):
						box.acc_down = False
						platform.obstacle_under_box = obst
			if box.y in range(obst.y, obst.y + obst.height) or obst.y in range(box.y, box.y + box.height):
				if obst.x in range(box.x, box.x + box.width+1):
					platform.game_over = True
					box.vel = 0
					platform.obstacles_vel = 0
		else:
			if obst.y-20 in range(box.y, box.y + box.height):
				if obst.x in range(box.x, box.x + box.width+1):
					platform.game_over = True
					box.vel = 0
					platform.obstacles_vel = 0
			if obst.apex_x in range(box.x, box.x + box.width+1):
				if box.y + 40 >= obst.apex_y:
					platform.game_over = True
					box.vel = 0
					platform.obstacles_vel = 0

	if platform.obstacle_under_box:
		if box.x not in range(platform.obstacle_under_box.x, platform.obstacle_under_box.x+platform.obstacle_under_box.width):
			box.acc_down = True
			platform.obstacle_under_box = None

	pygame.display.flip()
	# clock.tick(35)
pygame.quit()
