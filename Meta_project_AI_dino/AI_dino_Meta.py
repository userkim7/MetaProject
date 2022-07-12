import datetime
import random
import threading
import os
import pygame
import sys
from numpy import *
from random import choice as ch


W=array([[25.3979584 ],
 [41.47631906],
 [42.18309259]])
b=array(8.78731788)

def predict(x):
    y=dot(x,W)+b

    return y

oblist=[14, 10, 29]

while round(predict(oblist)[0],-1)!=2000:
    xl=ri(10,40)
    yl=ri(10,40)
    zl=53-(xl+yl)
    oblist=[xl,yl,zl]

randomob=[0 for x in range(oblist[0])]+[1 for x in range(oblist[1])]+[2 for x in range(oblist[2])]


pygame.init()


SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chrome Dino Runner")

Icon = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Icon)

def size_change(address,multiply):
    image=pygame.image.load(address).convert_alpha()
    size_x,size_y=image.get_size()
    image=pygame.transform.scale(image,(round(size_x*multiply),round(size_y*multiply)))
    return image

RUNNING = [
    size_change('img/dino (3).png',4),
    size_change('img/dino (4).png',4)
]
JUMPING = size_change('img/dino (1).png',4)
DUCKING = [
    size_change('img/dino (6).png',4),
    size_change('img/dino (7).png',4)
]

SMALL_CACTUS = [
    size_change('img/obstacle (3).png',3),
    size_change('img/obstacle (4).png',3),
    size_change('img/obstacle (5).png',3),
    size_change('img/obstacle (6).png',3),
    size_change('img/obstacle (7).png',3), #2
    size_change('img/obstacle (8).png',3) #2
]
LARGE_CACTUS = [
    size_change('img/obstacle (9).png',3), 
    size_change('img/obstacle (10).png',3), 
    size_change('img/obstacle (11).png',2.5) #2
]

BIRD = [
    size_change('img/obstacle (1).png',3),
    size_change('img/obstacle (2).png',3)
]

CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))

FONT_COLOR=(0,0,0)

points=0
countob=[0,0,0]
'''
wb=openpyxl.load_workbook('data.xlsx')
ws=wb.active
'''
class Dinosaur:

    X_POS = 80
    Y_POS = 310+350
    Y_POS_DUCK = 340+350
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.dino_rect[2]-=20
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect[2]-=20
        self.dino_rect[3]-=30
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4.3
            self.jump_vel -= 0.9
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)+350
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)+350

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 5)
        super().__init__(image, self.type)
        self.rect.y = 310+350


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 280+350
        if self.type==2:
            self.rect.y = 300+350


class Bird(Obstacle):
    BIRD_HEIGHTS = [250+350, 290+350, 320+350]
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, countob
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380+350
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    pause = False

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        current_time = datetime.datetime.now().hour
        with open("score.txt", "r") as f:
            score_ints = [int(x) for x in f.read().split()]  
            highscore = max(score_ints)
            if points > highscore:
                highscore=points 
            text = font.render("High Score: "+ str(highscore) + "  Points: " + str(points), True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (900+400, 40+350)
        SCREEN.blit(text, textRect)

        
        Font=pygame.font.SysFont("궁서",150)
        logo=Font.render("Meta         AI DINO",True,(0,100,100))
        logoRect=logo.get_rect()
        logoRect.center=(850,180)
        SCREEN.blit(logo,logoRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def unpause():
        nonlocal pause, run
        pause = False
        run = True

    def paused():
        nonlocal pause
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused, Press 'u' to Unpause", True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT  // 3)
        SCREEN.blit(text, textRect)
        pygame.display.update()

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    unpause()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                run = False
                paused()

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            obnum=ch(randomob)
            if obnum == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
                countob[0]+=1
            elif obnum == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
                countob[1]+=1
            elif obnum == 2:
                obstacles.append(Bird(BIRD))
                countob[2]+=1

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                menu()

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu():
    global points, countob
    global FONT_COLOR
    run = True
    t=True
    c=[1]
    while run:
        FONT_COLOR=(0,0,0)
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font("freesansbold.ttf", 30)

        text = font.render("Press any Key to Start", True, FONT_COLOR)
        if points>=300 and t:
            f = open("score.txt", "a")
            f.write(str(points) + "\n")
            f.close()
            t=False
        
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                countob=[0,0,0]
                main()


t1 = threading.Thread(target=menu(), daemon=True)
t1.start()
