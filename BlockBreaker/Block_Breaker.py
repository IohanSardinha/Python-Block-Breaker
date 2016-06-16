import pygame, sys, math
from pygame.locals import *
from random import randint

class Ball(pygame.sprite.Sprite):
	def __init__(self,x ,y , image, velocity):
		self.big = False
		self.magnetic = False
		pygame.sprite.Sprite.__init__(self)
		self.moving = False
		self.image = image
		self.rect = pygame.Rect(image.get_rect())
		self.width = image.get_rect().width
		self.height = image.get_rect().height 
		self.velocity = velocity
		self.rect = self.rect.move(x-self.width/2, y)

	def move(self):
		if self.moving:
			dx = clock.get_time()*self.velocity[0]
			dy = clock.get_time()*self.velocity[1]
			self.rect = self.rect.move(dx, dy)
		else:
			self.rect.x = platform.rect.x + platform.width/2 - self.width/2
			self.rect.y = platform.rect.y-self.height


	def bouncing(self):

		if  pygame.sprite.collide_rect(self, platform):
			if self.magnetic:
				self.moving = False
			playSound(bounceSound)
			k = 0.008
			dx = (self.rect.x + self.width/2) - (platform.rect.x+platform.width/2)
			speed = modulus(self.velocity)
			new_velocity = [self.velocity[0] + k*dx, self.velocity[1]]
			self.velocity = normalize(new_velocity, speed)
			self.velocity[1] = -abs(self.velocity[1])

		if self.rect.x + self.width >  screen_width:
			self.velocity[0] = -abs(self.velocity[0])
			playSound(bounceSound)
		elif self.rect.x < 0:
			self.velocity[0] = abs(self.velocity[0])
			playSound(bounceSound)
		elif self.rect.y < 0:
			self.velocity[1] = abs(self.velocity[1])
			playSound(bounceSound)
	
	def draw(self):
			screen.blit(self.image,(self.rect.x,self.rect.y))

	def update(self):
		self.move()
		self.bouncing()
		self.draw()
		if self.big:
			self.image = pygame.image.load("ballBig.png")
		else:
			self.image = pygame.image.load("ball.png")
		if pygame.sprite.spritecollideany(self, blockGroup):
			if not self.big:
				self.velocity[1] *= -1
			pygame.sprite.spritecollideany(self, blockGroup).die()

def modulus(velocity):
	return math.sqrt(velocity[0]**2 + velocity[1]**2)

def normalize(velocity, desired_speed):
	speed = modulus(velocity)
	velocity[0]*= desired_speed/speed
	velocity[1]*= desired_speed/speed 
	return velocity

class Platform(pygame.sprite.Sprite):
	def __init__(self,x,image,velocity):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = image.get_rect()
		self.width = image.get_rect().width
		self.height = image.get_rect().height 
		self.velocity = velocity
		self.rect = self.rect.move(x - self.width/2,screen_height-50)
	
	def move(self,direction):
		if self.rect.x >= 0 and direction == -1 :
			self.velocity = -abs(self.velocity)
			dx = clock.get_time()*self.velocity
			self.rect = self.rect.move(dx,0)
		elif self.rect.x + self.width <= screen_width and direction == 1:
			self.velocity = abs(self.velocity)
			dx = clock.get_time()*self.velocity
			self.rect = self.rect.move(dx,0)

	def draw(self):
		screen.blit(self.image,(self.rect.x,screen_height-50))

	def update(self):
		if pygame.sprite.spritecollideany(self, itemGroup):
			global time
			item = pygame.sprite.spritecollideany(self, itemGroup)
			time = 0
			if item.name == "big":
				ball.big = True
				pygame.sprite.spritecollideany(self, itemGroup).die()
			if item.name == "magnetic":
				ball.magnetic = True
				pygame.sprite.spritecollideany(self, itemGroup).die()

		if not ball.magnetic:
			self.image = pygame.image.load("platform.png")
		else:
			self.image = pygame.image.load("platformMagnetic.png")
		self.draw()

class Block(pygame.sprite.Sprite):
	def __init__(self,image,x,y,life):
		pygame.sprite.Sprite.__init__(self)
		self.life = life
		self.image = image
		self.rect =  image.get_rect()
		self.width = image.get_rect().width
		self.height = image.get_rect().height
		self.rect = self.rect.move(x,y)
	def die(self):
		global score
		if self.life <= 1:
			blockGroup.remove(self)
			score += 10
			playSound(breakSound)
		else:
			self.life -= 1
			playSound(bounceSound)
			score += 5

	def update(self):
		if self.life == 4:
			self.image = pygame.image.load("block3.png")
		elif self.life == 3:
			self.image = pygame.image.load("block2.png")
		elif self.life == 2:
			self.image = pygame.image.load("block1.png")
		elif self.life == 1:
			self.image = pygame.image.load("block.png")

class Button(pygame.sprite.Sprite):
	def __init__(self,image,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = image.get_rect()
		self.rect = self.rect.move(x,y)
	def draw(self):
		screen.blit(self.image,(self.rect.x,self.rect.y))

class Item(pygame.sprite.Sprite):
	def __init__(self,name,image,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.name = name
		self.image = image
		self.rect = image.get_rect()
		self.rect = self.rect.move(x,y)
	def draw(self):
		screen.blit(self.image,(self.rect.x,self.rect.y))
	def die(self):
		global itemGroup
		itemGroup.remove(self)
	def update(self):
		dy = clock.get_time()*0.15
		self.rect = self.rect.move(0, dy)
		if self.rect.y > screen_height:
			self.die()

def print_text(text,x,y,size,color,fonte):
    font = pygame.font.SysFont(fonte, size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

def buildLevel():
	global ball, platform,blockGroup
	ball = Ball(screen_width/2,screen_height-70,pygame.image.load("ball.png"),[0,-0.40])
	platform = Platform(screen_width/2, pygame.image.load("platform.png"),0.4)

	blockGroup = pygame.sprite.Group()
	
	for i in range(8):#8
		for j in range(11):#11
			if i == 0 or i == 1:
				life = 4
			elif i == 2 or i == 3:
				life = 3
			elif i == 4 or i == 5:
				life = 2
			elif i == 6 or i == 7:
				life = 1
			tempBlock = Block(pygame.image.load("block.png"),pygame.image.load("block.png").get_rect().width*j+2*j+27.5
															,pygame.image.load("block.png").get_rect().height*i+2*i+10,life)
			blockGroup.add(tempBlock)

def playSound(sound):
	if music:
		sound.play()

def playLevel():
	if music:
		playMusic.play(loops=-1)
	buildLevel()

	global itemGroup, music, time, powerUpTime
	
	started = False
	paused = False
	pauseButton = Button(pygame.image.load("Pause_Button.png"),screen_width - pygame.image.load("Pause_Button.png").get_rect().width - 10,screen_height - pygame.image.load("Pause_Button.png").get_rect().height - 10 )
	musicButton = Button(pygame.image.load("music{}.png".format(int(music))),screen_width - pygame.image.load("music{}.png".format(int(music))).get_rect().width - 50,screen_height - pygame.image.load("music{}.png".format(int(music))).get_rect().height - 10 )
	
	while True:
	    for event in pygame.event.get():
	        if event.type == QUIT:
	            pygame.quit()
	            sys.exit() 
	        if event.type == MOUSEBUTTONUP:
				x,y = event.pos
				if pauseButton.rect.collidepoint(x,y) and not paused and ball.moving:
					paused = True
				elif pauseButton.rect.collidepoint(x,y) and  paused:
					paused = False
				if musicButton.rect.collidepoint(x,y) and  music:
					global sounds
					music = False
					musicButton.image = pygame.image.load("music{}.png".format(int(music)))
					sounds.pause()
				elif musicButton.rect.collidepoint(x,y) and  not music:
					global sounds
					music = True
					musicButton.image = pygame.image.load("music{}.png".format(int(music)))
					sounds.unpause()

	    clock.tick(30)
	    if started and not paused:
	    	time += 1
	    	powerUpTime += 1
	    if ball.big and time >= 60:
	    	ball.big = False
	    if ball.magnetic and time >= 60:
	    	ball.magnetic = False

	    if len(blockGroup.sprites()) == 0:
	    	buildLevel()
	    	playSound(winSound)
	    	ball.velocity[1] -= 0.05*score/1540 #maximum score per level

	    keys = pygame.key.get_pressed()
	    if keys[K_SPACE] and not ball.moving:
	    	ball.moving = True
	    	playSound(bounceSound)
	    	started = True
	    if keys[K_SPACE] and paused:
	    	paused = False

	    elif ball.rect.y - ball.height/2 > screen_height:
	    	playSound(loseSound)
	    	playMusic.stop()
	    	break
	    if paused:
	    	print_text('[  P R E S S  S P A C E  T O  C O N T I N U E  ]',screen_width* 0.3, screen_height*0.7, 15, colors["White"],'Arial' )
	    else:
		    screen.fill(colors["Blue"])
		    blockGroup.draw(screen)
		    blockGroup.update()
		    ball.update()
		    platform.update()
		    pauseButton.draw()
		    itemGroup.draw(screen)
		    itemGroup.update()
		    if keys[K_LEFT]:
	    		platform.move(-1)
		    if keys[K_RIGHT]:
		    	platform.move(1)
		    if powerUpTime >= 100:
		    	powerUpTime = 0
	    		rnd = randint(0,2)
	    		if rnd == 0:
	    			itemGroup.add(Item("big",pygame.image.load("bigBallItem.png"),randint(pygame.image.load("bigBallItem.png").get_rect().width,screen_width)-pygame.image.load("bigBallItem.png").get_rect().width,pygame.image.load("bigBallItem.png").get_rect().height))
	    		elif rnd == 1:
	    			itemGroup.add(Item("magnetic",pygame.image.load("magneticItem.png"),randint(pygame.image.load("magneticItem.png").get_rect().width,screen_width)-pygame.image.load("magneticItem.png").get_rect().width,pygame.image.load("bigBallItem.png").get_rect().height))

	    print_text("Score: "+str(score),20,screen_height - 30,20,colors["Red"],'Arial')
	    if not started:
	    	print_text('Block Breaker',screen_width* 0.2, screen_height*0.15, 80, colors["Red"],'comicsansms' )
	    	print_text('[  P R E S S  S P A C E  T O  S T A R T  ]',screen_width* 0.335, screen_height*0.7, 15, colors["White"],'Arial' )
	    	print_text('[  M O V E  W I T H  L E F T / R I G H T  A R R O W S  ]',screen_width* 0.28, screen_height*0.75, 15, colors["White"],'Arial' )

	    musicButton.draw()
	    pygame.display.flip()

def gameOver():
	record = 0
	recordFile = open("record.txt","r+")
	for line in recordFile:
		record = int(line)
	recordFile.close()
	recordFile = open("record.txt","w")
	if score > record:
		record = score
		recordFile.writelines(str(record))
	else:
		recordFile.writelines(str(record))
	recordFile.close()

	if music:
		gameOverMusic.play(loops=-1)
	play_again_button = Button(pygame.image.load("Play_again_Button.png"),screen_width/2 - pygame.image.load("Play_again_Button.png").get_rect().width/2, screen_height*0.5)
	quit_button = Button(pygame.image.load("Quit_Button.png"),screen_width/2 - pygame.image.load("Quit_Button.png").get_rect().width/2, screen_height*0.65)
	screen.fill(colors["Black"])
	play_again_button.draw()
	quit_button.draw()
	print_text("Game Over",screen_width/2-200,screen_height/7,80,colors["White"],'Arial')
	print_text("Score : " + str(score),screen_width*0.4,screen_height*0.35,25,colors["White"],'Arial')
	print_text("Best Score : " + str(record),screen_width*0.4,screen_height*0.4,25,colors["White"],'Arial')
	pygame.display.flip()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONUP:
				x,y = event.pos
				if quit_button.rect.collidepoint(x,y):
					playSound(clickSound)
					pygame.quit()
					sys.exit()
				elif play_again_button.rect.collidepoint(x,y):
					playSound(clickSound)
					gameOverMusic.stop()
					global score
					score = 0
					return

pygame.init()

sounds = pygame.mixer
sounds.init()

music = True
time = 0
powerUpTime = 0

pygame.display.set_caption('Block Breaker')
pygame.display.set_icon(pygame.image.load("ballIcon.png"))

gameOverMusic = sounds.Sound("gameOver.wav")
playMusic = sounds.Sound("PingPong.wav") 
breakSound = sounds.Sound("break.wav")
bounceSound = sounds.Sound("bounce.wav")
winSound = sounds.Sound("win.wav")
loseSound = sounds.Sound("lose.wav")
clickSound = sounds.Sound("click.wav")
playMusic.set_volume(0.5)

screen_width = 800
screen_height = 600

itemGroup =  pygame.sprite.Group()

score = 0

colors = {"Black" : (0,0,0), "White" : (255,255,255), "Red" : (255,0,0), "Blue" : (0,0,100), "Yellow" : (255,255,0), 
"Green" : (0,255,0), "Orange" : (255,128,0), "Purple" : (127,0,255)}

clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width,screen_height))

while True:
    playLevel()
    gameOver()