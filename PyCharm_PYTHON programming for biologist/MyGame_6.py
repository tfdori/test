
import pygame

pygame.init()
pygame.display.set_caption('My Smurf Game')

# =====
# TIME
# =====
clock = pygame.time.Clock()

# =======
# SCREEN
# =======

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Defining variables
tile_size = 50
game_over = False
azrael_exist = True
gargamel_exist = True
winning = False
start = False

# Uploading background images
cave_img = pygame.image.load('Cave.png')
cave_img = pygame.transform.scale(cave_img, (600, 600))

# Drawing background
def draw_bg():
	screen.fill((120, 200, 227))
	screen.blit(cave_img, (50, 50))

# Drawing grid to edit
def draw_grid():
	for line in range(0,15):
		pygame.draw.line(screen,(255,255,255), (0,50*line), (SCREEN_WIDTH,50*line))
		pygame.draw.line(screen, (255, 255, 255), (50 * line,0), (50 * line,SCREEN_HEIGHT))

# =======
# OBJECTS
# =======

class Cave():
	def __init__(self, data):
		self.tile_list = []

		#uplodaing the images of the tiles
		ground_img = pygame.image.load('ground4.jpg')
		water_img = pygame.image.load('water2.png')

		# going through the cave_data line by line
		# if there is a 1 -> ground image
		# if there is a 2 -> water image
		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(ground_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect, "ground")
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(water_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect,"water")
					self.tile_list.append(tile)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])

# Drawing the platform of the game
# one number refers to one rectangle in the grid drawing out by the draw_grid()
cave_data = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,1,1,1,1,0,0,0,0,0,1],
[1,0,0,0,0,0,0,1,1,1,1,2,1,1],
[1,1,0,0,0,0,0,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,1,0,0,0,0,0,0,0,0,1],
[1,2,2,2,1,1,1,0,0,0,0,0,0,1],
[1,1,1,1,1,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,1,1,1,1,1],
[1,0,0,0,0,0,0,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Exit_table():
	def __init__(self, x, y):

		exit_img = pygame.image.load('exit.png')
		self.image = pygame.transform.scale(exit_img, (50, 50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def drawing (self):
		screen.blit(self.image, self.rect)

class Gargamel():
	def __init__(self,x,y):

		gargamel_img = pygame.image.load('hokuszpok.png')
		self.image = pygame.transform.scale(gargamel_img, (55, 90))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.move_pix = 3
		self.move_counter = 0

	def update(self):

		self.rect.x -= self.move_pix
		self.move_counter += 1
		if self.move_counter > 40:
			self.move_pix *= -1
			self.move_counter = 0

	def drawing(self):
		# draw enemy onto screen
		screen.blit(self.image, self.rect)

class Azrael():
	def __init__(self,x,y):

		azrael_img = pygame.image.load('Azrael_cat.png')
		self.image = pygame.transform.scale(azrael_img, (70, 75))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.move_pix = 1
		self.move_counter = 0

	def update(self):

		self.rect.x -= self.move_pix
		self.move_counter += 1
		if self.move_counter > 110:
			self.move_pix *= -1
			self.move_counter = 0

	def drawing(self):
		# draw enemy onto screen
		screen.blit(self.image, self.rect)


# Creating the smurf player
class Smurf():
	def __init__(self, x, y):

		img_right = pygame.image.load('smurf_01.png')
		img_right = pygame.transform.scale(img_right, (50, 70))
		img_left = pygame.transform.flip(img_right, True, False)

		self.images = [img_right, img_left]
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False

	def update(self, game_over, gargamel_exist, azrael_exist, winning):
		# game_over variable is a global variable,
		# but I can bring it in, with this argument,
		# than "return" it at the end -> into the global variable
		# as the gargamel_esxist, azrael_exist variables

		# coordinates to detect its displacements
		dx = 0
		dy = 0

		if game_over == False:

			# Moving by pressing keys
			key = pygame.key.get_pressed()
			if key[pygame.K_UP] and self.jumped == False:
				self.vel_y = -15
				self.jumped = True
				# when the player jumping, it go back on the y-axe -> = go up on the screen
			if key[pygame.K_UP] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 3
				self.image = self.images[1]
			if key[pygame.K_RIGHT]:
				dx += 3
				self.image = self.images[0]

			# Gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			# Collision with tiles
			for tile in cave.tile_list:
				# x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				# y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
					if tile[2] == "water":
						# stop the game if it step into water
						game_over = True

			# Interactions with "enemies"
			# Gargamel
			if gargamel.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				# Jumping on Gargamel
				if self.vel_y > 0:
					gargamel_exist = False
					game_over = False
				# Collision with Gargamel -> game over
				if gargamel_exist == True:
					game_over = True
			# Azrael
			if azrael.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				# Jumping on Azrael
				if self.vel_y > 0:
					azrael_exist = False
					game_over = False
				# Collision with Azrael -> game over
				if azrael_exist == True:
					game_over = True

			# Exiting
			if exit_table.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				print ("Exiting true")
				winning = True

			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy

		#draw player onto screen
		screen.blit(self.image, self.rect)
		#pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

		return (game_over, gargamel_exist, azrael_exist, winning)

# ======
# TEXTS
# ======
def draw_text(text, font, text_col, x, y):
	# converting the text into an image
	text_img = font.render(text, True, text_col)
	screen.blit(text_img,(x,y))

# =======
# BUTTONS
# =======

def QUIT_BUTTON(run):
	pos = pygame.mouse.get_pos()

	# QUIT BUTTON
	quit_rect = pygame.draw.rect(screen, (140, 160, 255), (300, 385, 100, 60), width=3)
	if quit_rect.collidepoint(pos):
		if pygame.mouse.get_pressed()[0] == True:
			run = False

	return run

def START_BUTTON(start):
	pos = pygame.mouse.get_pos()
	start_rect = pygame.draw.rect(screen, (50, 65, 152), (250, 300, 200, 100))
	pygame.draw.rect(screen, (0,0,0), (250, 300, 200, 100), width = 3)

	text_font_start = pygame.font.SysFont(None, 70, bold=True)
	draw_text("START", text_font_start, (140, 160, 255), 270, 327)
	if start_rect.collidepoint(pos):
		if pygame.mouse.get_pressed()[0] == True:
			start = True

	return start

# =========
# VARIABLES
# =========

cave = Cave(cave_data)
smurf = Smurf(50, 570)
azrael = Azrael(505,177)
gargamel = Gargamel(590,465)
exit_table = Exit_table(590,200)

# =========
# GAME LOOP
# =========

run = True
while run:

	clock.tick(40)
	draw_grid()
	draw_bg()
	cave.draw()
	exit_table.drawing()

	if start == False:
		start = START_BUTTON(start)

	if game_over == False and winning == False and start == True:
		if gargamel_exist == True:
			gargamel.drawing()
			gargamel.update()
			gargamel_exist = smurf.update(game_over, gargamel_exist, azrael_exist, winning)[1]
		if azrael_exist == True:
			azrael.drawing()
			azrael.update()
			azrael_exist = smurf.update(game_over, gargamel_exist, azrael_exist,winning)[2]

		winning = smurf.update(game_over, gargamel_exist, azrael_exist, winning)[3]
		game_over = smurf.update(game_over, gargamel_exist, azrael_exist, winning)[0]

	elif game_over == True and winning == False:
		pygame.draw.rect(screen, (0,0,0), (100,270,500,200))

		text_font_gameover = pygame.font.SysFont(None, 100, bold=True, italic=True)
		draw_text("Game over!", text_font_gameover, (166,26,26), 150, 300)

		text_font_quit = pygame.font.SysFont(None, 50, bold=True)
		draw_text("Quit", text_font_quit, (140, 160, 255), 310, 400)

		run = QUIT_BUTTON(run)

	elif game_over == False and winning == True:
		pygame.draw.rect(screen, (0,0,0), (100,270,500,210))

		text_font = pygame.font.SysFont(None, 100, bold=True, italic=True)
		draw_text("You won!", text_font, (166,26,26), 190, 300)

		text_font_quit = pygame.font.SysFont(None, 50, bold=True)
		draw_text("Quit", text_font_quit, (140, 160, 255), 310, 400)

		run = QUIT_BUTTON(run)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()