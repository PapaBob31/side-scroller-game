import pygame, copy, random
pygame.init()
pygame.display.set_caption("Run Box run!")
win = pygame.display.set_mode((800, 450))
bg_img = pygame.image.load('background.jpg')
clock = pygame.time.Clock()

red = (255, 0, 0)
green = (108, 184, 132)# (126, 191, 147)

class Player:
	def __init__(self):
		self.x = 200
		self.y = 360
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
		self.y = 360
		self.vel = 10
		self.acc_up = False
		self.acc_down = False
		self.init_pos = 0
		self.on_top_obstacle = False


class Rectangle:
	"""This is an Obstacle class"""
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.color = green
		self.width = width
		self.height = height
		self.lower = False
		self.same_height = False

	def display(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))


class Triangle:
	"""This is an Obstacle class"""
	def __init__(self, x, base):
		self.x = x
		self.base = base
		self.y = self.base-40
		self.width = 40
		self.color = green

	def display(self):
		pygame.draw.polygon(win, self.color, ((self.x, self.base),  (self.x+(self.width//2), self.y), (self.x+self.width, self.base)))


class Platform():
	def __init__(self):
		self.x = 0
		self.y = 400
		self.color = green
		self.width = 800
		self.height = 50
		self.obstacles_vel = 10
		self.obstacles_list = [Rectangle(800, 360, 80, 40), Rectangle(800, 360, 120, 40), Rectangle(800, 320, 80, 80),
							   Rectangle(800, 320, 80, 80), Rectangle(800, 280, 80, 40), Rectangle(800, 280, 120, 120), 
							   Rectangle(800, 280, 80, 120), Rectangle(800, 240, 80, 40), Rectangle(800, 320, 120, 80)]
		self.obstacles_onscreen = [Rectangle(800, 360, 80, 40)]
		self.obstacle_under_box = None
		self.next_obstacle = None
		self.game_over = False

	def display(self):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

box = Player()
platform = Platform()

def create_next_obstacle():
	obstacle = random.choice(platform.obstacles_list)
	platform.next_obstacle = copy.copy(obstacle)
	if (obstacle.y - 40) == platform.obstacles_onscreen[-1].y:
		platform.next_obstacle.lower = True
	elif obstacle.y == (platform.obstacles_onscreen[-1].y - 40):
		platform.next_obstacle.lower = False
	elif obstacle.y == platform.obstacles_onscreen[-1].y:
		platform.next_obstacle.same_height = True
	else:
		create_next_obstacle()

def reset():
	platform.obstacles_onscreen = [Rectangle(800, 360, 80, 40)]
	platform.next_obstacle = None
	platform.obstacle_under_box = None
	platform.game_over = False
	box.reset()
	platform.obstacles_vel = 10

run = True
i = 0

while run:
	pygame.time.delay(20)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP and not box.acc_down:
				if not platform.game_over:
					box.init_pos = box.y
					box.acc_up = True
			if event.key == pygame.K_DOWN:
				reset()

	win.fill((0, 0, 0))
	win.blit(bg_img, (i, 0))
	win.blit(bg_img, (800+i, 0))
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
		if box.y == 360:
			box.init_pos = box.y
			box.acc_up = False
			box.acc_down = False

	if not platform.game_over:
		if i == -800:
			i = 0
		i -= 10
		if not platform.next_obstacle:
			create_next_obstacle()

		if not platform.next_obstacle.same_height:
			if platform.next_obstacle.lower:
				if platform.obstacles_onscreen[-1].x + platform.obstacles_onscreen[-1].width <= 760:
					platform.obstacles_onscreen.append(platform.next_obstacle)
					platform.next_obstacle = None
			elif not platform.next_obstacle.lower:
				if platform.obstacles_onscreen[-1].x + platform.obstacles_onscreen[-1].width <= 700:
					platform.obstacles_onscreen.append(platform.next_obstacle)
					platform.next_obstacle = None
		else:
			if platform.obstacles_onscreen[-1].x + platform.obstacles_onscreen[-1].width <= 660:
				platform.obstacles_onscreen.append(platform.next_obstacle)
				platform.next_obstacle = None

	for obst in platform.obstacles_onscreen[:]:
		obst.display()
		obst.x -= platform.obstacles_vel

	for obst in platform.obstacles_onscreen[:]:
		if obst.x + obst.width <= 0:
			platform.obstacles_onscreen.remove(obst)

	for obst in platform.obstacles_onscreen[:]:
		if box.acc_down and type(obst) == Rectangle:
			if box.y + 40 == obst.y:
				if box.x in range(obst.x, obst.x + obst.width):
					box.acc_down = False
					platform.obstacle_under_box = obst
				if obst.x in range(box.x, box.x + box.width):
					box.acc_down = False
					platform.obstacle_under_box = obst
		if box.y in range(obst.y, obst.y + obst.height) or obst.y in range(box.y, box.y + box.height):
			if box.x + box.width == obst.x:
				platform.game_over = True
				box.vel = 0
				platform.obstacles_vel = 0

	if platform.obstacle_under_box:
		if box.x not in range(platform.obstacle_under_box.x, platform.obstacle_under_box.x+platform.obstacle_under_box.width):
			box.acc_down = True
			platform.obstacle_under_box = None

	pygame.display.flip()
	clock.tick(40)
pygame.quit()
