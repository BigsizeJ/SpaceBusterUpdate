#import module
import pygame
import random
import math

from pygame.constants import K_SPACE

#-------------

#init--------
pygame.init()
#------------

#important variable--------------------------------------------
screen_width = 500
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
title = pygame.display.set_caption("Space Buster")
iconImg = pygame.image.load("Assets/icon.png")
icon = pygame.display.set_icon(iconImg)
#--------------------------------------------------------------

#img variable--------------------------------------
backgroundImg = pygame.image.load("Assets/bg.jpg")
playerImg = pygame.image.load("Assets/player.png")
bulletImg = pygame.image.load("Assets/bullet.png")
powerupImg = pygame.image.load("Assets/powerup.png")
#--------------------------------------------------

def text_format(message, textFont, textSize, textColor):
        
        createFont=pygame.font.Font(textFont, textSize)
        createText = createFont.render(message, 0, textColor)

        return createText

def main_menu():
    
    #color variable--------
    black = (0, 0 , 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    #----------------------

    #menu variable----
    menu = True
    selected = "start"
    #-----------------

    #text variable------------
    font = "JetBrainsMono.ttf"
    #-------------------------

    def background():
            screen.blit(backgroundImg, (0, 0))

    while menu:

        background()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                if event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_SPACE:
                    if selected is "start":
                        mainloop()
                    if selected is "quit":
                        quit()

        title = text_format("SPACE BUSTER", font, 65, red)
        if selected == "start":
            text_start = text_format("START", font, 50, red)
        else:
            text_start = text_format("START", font, 50, black)
        if selected == "quit":
            text_quit = text_format("QUIT", font, 50, red)
        else:
            text_quit = text_format("QUIT", font, 50, black)
            
        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        quit_rect = text_quit.get_rect()

        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 360))

        pygame.display.update()
            


def mainloop():

    #player variable--
    playerX = 186
    playerY = 580
    playerX_change = 0
    #------------------

    #bullet variable------
    bulletX = 0
    bulletY = 572
    bulletY_change = 1
    global bullet_state
    bullet_state = "ready"
    bulletimage = [bulletImg, bulletImg]
    #---------------------

    #powerup variable----------------
    powerupX = random.randint(0, 436)
    powerupY = -10
    powerupY_change = .1
    #--------------------------------

    global Upgraded
    Upgraded = False

    def background():
        screen.blit(backgroundImg, (0, 0))

    def player():
        screen.blit(playerImg, (playerX, playerY))

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletimage[1], (x + 16, y + 10))
    
    def upgraded_bullet(x, y):
        global bullet_state
        bullet_state = "upgraded"
        screen.blit(bulletimage[1], (x + 16, y + 10))

    def powerup(x, y):
        screen.blit(powerupImg, (x, y))

    def CollisionChecker(x1, y1, x2, y2):
        distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2,2)))
        if distance < 27:
            return True
        else:
            return False

    global running 
    running = True

    while running:
        background()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_RIGHT:
                    playerX_change = .5
                if event.key == pygame.K_LEFT:
                    playerX_change = -.5
                if event.key == pygame.K_SPACE:
                    if Upgraded is True and bullet_state is "ready":
                        bulletX = playerX
                        upgraded_bullet(bulletX, bulletY)
                    elif Upgraded is False and bullet_state is "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                        
                if event.key == pygame.K_ESCAPE:
                    main_menu()
            
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    playerX_change = 0
        

        #player fucntion variable
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 436:
            playerX = 436
        #------------------------
        
        #keepshooting------------------------------------------
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            if Upgraded is True and bullet_state is "ready":
                bulletX = playerX
                upgraded_bullet(bulletX, bulletY)
            elif Upgraded is False and bullet_state is "ready":
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
        #------------------------------------------------------

        #bullet function variable-----------------        
        if bulletY <= -20:
            bulletY = 572
            bullet_state = "ready"
    
        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
            
        if bullet_state is "upgraded":
            upgraded_bullet(bulletX + 32, bulletY)
            upgraded_bullet(bulletX - 32, bulletY)
            bulletY -= bulletY_change
        #-----------------------------------------
        
        #powerup variable---------------------------------------------------------
        powerupY += powerupY_change
        powerup(powerupX, powerupY)
        player()
        powerup_collision = CollisionChecker(powerupX, powerupY, playerX, playerY)
        if powerup_collision:
            Upgraded = True
            powerupY_change = 5000
        #-------------------------------------------------------------------------

        pygame.display.update()
    

main_menu()


