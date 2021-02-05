#! /usr/bin/python3

import pygame
import math
from playsound import playsound
from pygame import mixer,mixer_music
from random import randint
pygame.mixer.pre_init(44100,16,2,4096)
# mixer.init()
pygame.init()

SCREEN_HEIGHT = 500 
SCREEN_WIDTH = 700
size = (SCREEN_WIDTH,SCREEN_HEIGHT)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Corona vaccination by Raahil")
clock = pygame.time.Clock()

# spaceship image
spaceship = pygame.image.load('spaceship.png')
playerX = 350
dX = 3
playerY = 450
dY = 3

# enemy
corona = []
coronaX = []
coronaY = []
coronaDX = []
num_of_corona = 10 

for i in range(num_of_corona):
    corona.append(pygame.image.load('corona.png'))
    coronaX.append(randint(0,668))
    coronaY.append(randint(5,30))
    coronaDX.append(6)

coronaDY = 15


# bullet
bullet = pygame.image.load('injection.png')
bulletX = 50
bulletY = 430
bulletDX = 0
bulletDY = -7
bullet_state = "ready" # ready = ready to fire, fire = firing currently on sccreen


bg_image = pygame.image.load('newbg.jpg')
bg_sound = mixer.Sound('tenet_bgm.ogg')
bg_sound.play(-1)
# mixer.init()
# bg_sound = mixer.music.load('kgf3.ogg')
# mixer.music.play(-1)

flag = True
playerX_change = 0

score = 0
font = pygame.font.Font(None,32)
textX = 10
textY = 10

def show_score(x,y):
    score_s = font.render("Score: "+str(score),True,(255,255,255))
    screen.blit(score_s,(x,y))


def player(x,y):
    screen.blit(spaceship,(x,y))

def enemy(x,y,i):
    screen.blit(corona[i],(x,y))

def bullet_f(x,y):
    global bullet_state
    bullet_state = "fire"

    screen.blit(bullet,(x,y+10))

def isCollision(cX,cY,bX,bY):
    dist = math.sqrt((cX-bX)**2+(cY-bY)**2)
    return dist<27
    



while flag:
    screen.fill((0,0,0))
    screen.blit(bg_image,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag=False
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_x:
                flag=False
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state=="ready":
                bullet_f(playerX,bulletY)
                bulletX = playerX
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # movement of spaceship
    playerX += playerX_change
    # boundary collisions of spaceship
    if playerX<0 :
        playerX = 0
    if playerX>668 :
        playerX = 668
    
    for i in range(num_of_corona):
        # movement of corona
        coronaX[i] += coronaDX[i]
        # boundary collisions of corona
        if coronaX[i] <0 :
            coronaX[i] = 0
            coronaY[i] += coronaDY
            coronaDX[i] *= -1
        if coronaX[i] >668 :
            coronaX[i] = 668
            coronaY[i] += coronaDY
            coronaDX[i] *= -1
        
        collision = isCollision(coronaX[i],coronaY[i],bulletX,bulletY)
        if collision:
            bulletY = 450
            bullet_state = "ready"
            coronaX[i] = randint(0,668)
            coronaY[i] = randint(5,30)
            score += 1
            
        enemy(coronaX[i],coronaY[i],i)

    if bulletY <= 0 :
        bullet_state = "ready"
        bulletY = 450
    # bullet movement 
    if bullet_state == "fire":
        bullet_f(bulletX,bulletY)
        bulletY += bulletDY
    show_score(textX,textY)
    player(playerX,playerY)
    pygame.display.update()
    clock.tick(60)

pygame.QUIT
