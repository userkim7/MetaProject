import pygame
import random
import threading


pygame.init()

Screen_size=(1100,600) #(width,height)
Screen=pygame.display.set_mode(Screen_size)

pygame.display.set_caption('AI Dino Game')

Icon=pygame.image.load('img/dino (3).png')
pygame.display.set_icon(Icon)
#크기 조정 필요!!!
def size_change(address,multiply):
    image=pygame.image.load(address).convert_alpha()
    size_x,size_y=image.get_size()
    image=pygame.transform.scale(image,(size_x*multiply,size_y*multiply))
    return image

Running=[
    size_change('img/dino (3).png',4),
    size_change('img/dino (4).png',4)
]

Jumping=size_change('img/dino (1).png',4)

Ducking=[
    size_change('img/dino (6).png',4),
    size_change('img/dino (7).png',4)
]

Cactus_small_img=[
    size_change('img/obstacle (3).png',3),
    size_change('img/obstacle (4).png',3),
    size_change('img/obstacle (5).png',3),
    size_change('img/obstacle (6).png',3),
    size_change('img/obstacle (7).png',3), #2
    size_change('img/obstacle (8).png',3) #2
]

Cactus_large_img=[
    size_change('img/obstacle (9).png',3), 
    size_change('img/obstacle (10).png',3), 
    size_change('img/obstacle (11).png',3) #2
]

Bird_img=[
    size_change('img/obstacle (1).png',3),
    size_change('img/obstacle (2).png',3)
]

Back=size_change('img/background_sheet.png',5)

font_color=(0,0,0)

class Dino:
    X_grid=80
    Y_grid=320
    Y_grid_duck=345
    Jump_V=9
    
    def __init__(self):
        self.run_img=Running
        self.jump_img=Jumping
        self.duck_img=Ducking

        self.running=True
        self.jumping=False
        self.ducking=False
        
        self.step=0
        self.jump_V=self.Jump_V
        self.image=self.run_img[0]
        self.rect=self.image.get_rect()
        self.rect.x=self.X_grid
        self.rect.y=self.Y_grid
        
    def update(self,user):
        if self.running:
            self.run()
        if self.jumping:
            self.jump()
        if self.ducking:
            self.duck()
            
        if self.step>=6:
            self.step=0

        if user[pygame.K_DOWN]and not self.jumping:
            self.ducking=True
            self.running=False
            self.jumping=False
        elif (user[pygame.K_UP]or user[pygame.K_SPACE])and not self.jumping:
            self.jumping=True
            self.running=False
            self.ducking=False            
        elif not (self.jumping or user[pygame.K_DOWN]):
            self.running=True
            self.jumping=False
            self.ducking=False

    def run(self):
        self.image=self.run_img[self.step//3]
        self.rect=self.image.get_rect()
        self.rect.x=self.X_grid
        self.rect.y=self.Y_grid
        self.step+=1
            
    def jump(self):
        self.image=self.jump_img
        if self.jumping:
            self.rect.y-=self.jump_V*4
            self.jump_V-=0.85
        if self.jump_V<-self.Jump_V:
            self.jumping=False
            self.jump_V=self.Jump_V
                
    def duck(self):
        self.image=self.duck_img[self.step//3]
        self.rect=self.image.get_rect()
        self.rect.x=self.X_grid
        self.rect.y=self.Y_grid_duck
        self.step+=1
            
    def draw(self,Screen):
        Screen.blit(self.image,(self.rect.x,self.rect.y))
            
class Obstacle:
    def __init__(self,image,type):
        self.image=image
        self.type=type
        self.rect=self.image[self.type].get_rect()
        self.rect.x=Screen_size[0]

    def update(self):
        self.rect.x-=game_speed
        if self.rect.x<-self.rect.width:
            obstacles.pop()

    def draw(self,Screen):
        Screen.blit(self.image[self.type],self.rect)

class Cactus_small(Obstacle):
    def __init__(self,image):
        self.type=random.randint(0,5)
        super().__init__(image,self.type)
        self.rect.y=325

class Cactus_large(Obstacle):
    def __init__(self,image):
        self.type=random.randint(0,2)
        super().__init__(image,self.type)
        self.rect.y=300

class Bird(Obstacle):
    Bird_height=[250,290,320]
    
    def __init__(self,image):
        self.type=0
        super().__init__(image,self.type)
        self.rect.y=random.choice(self.Bird_height)
        self.index=0

    def draw(self,Screen):
        if self.index>=9:
            self.index=0
        Screen.blit(self.image[self.index//5],self.rect)
        self.index+=1

points=0


def main():
    global game_speed,grid_back,points,obstacles
    run=True
    clock=pygame.time.Clock()
    player=Dino()
    game_speed=20
    grid_back=[0,380] #[x,y]
    points=0
    font=pygame.font.Font('freesansbold.ttf',20)
    obstacles=[]

    def score():
        global points,game_speed
        points+=1
        if points%100==0:
            game_speed+=1
        with open('score.txt','r') as f:
            score=[int(x) for x in f.read().split()]
            highscore=max(score)
            if points>highscore:
                highscore=points
            text=font.render(f'High Score: {highscore}  Points: {points}',True,font_color)

        text_rect=text.get_rect()
        text_rect.center=(900,40)
        Screen.blit(text,text_rect)

    def background():
        global grid_back
        image_width=Back.get_width()
        Screen.blit(Back,grid_back)
        Screen.blit(Back,(image_width+grid_back[0],grid_back[1]))
        if grid_back[0]<=-image_width:
            Screen.blit(Back,(image_width+grid_back[0],grid_back[1]))
            grid_back[0]=0
        grid_back[0]-=game_speed


    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                
        Screen.fill((0,0,0))
        user=pygame.key.get_pressed()
        player.draw(Screen)
        player.update(user)

        if len(obstacles)==0:
            obstacles_list=['s','l','b']
            Random=random.choice(obstacles_list)
            if Random=='s':
                obstacles.append(Cactus_small(Cactus_small_img))
            elif Random=='l':
                obstacles.append(Cactus_large(Cactus_large_img))
            elif Random=='b':
                obstacles.append(Bird(Bird_img))

        for obstacle in obstacles:
            obstacle.draw(Screen)
            obstacle.update()
            if player.rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                menu()

        background()

        score()
        
        clock.tick(10)
        pygame.display.update()

def menu():
    global points
    run=True
    while run:
        Screen.fill((128,128,128))
        font=pygame.font.Font('freesansbold.ttf',30)

        text=font.render('Press Any Key To Start',True,font_color)
        score=font.render(f'Your Score: {points}',True,font_color)

        score_rect=score.get_rect()
        score_rect.center=(Screen_size[0]//2,Screen_size[1]//2+50)
        Screen.blit(score,score_rect)
        f=open('score.txt','a')
        f.write(str(points)+'\n')
        f.close()

        with open('score.txt','r') as f:
            score=(f.read())
            score_int=[int(x) for x in score.split()]
        highscore=max(score_int)

        highscore_text=font.render(f'High Score: {highscore}',True,font_color)
        highscore_rect=highscore_text.get_rect()
        highscore_rect.center=(Screen_size[0]//2,Screen_size[1]//2+100)

        Screen.blit(highscore_text,highscore_rect)

        text_rect=text.get_rect()
        text_rect.center=[x//2 for x in Screen_size]

        Screen.blit(text,text_rect)
        Screen.blit(Running[0],(Screen_size[0]//2-20,Screen_size[1]//2-140))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type==pygame.KEYDOWN:
                main()
                run=False
menu()             
'''
t=threading.Thread(target=menu(),daemon=True)
t.start()
'''
        
