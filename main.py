import pygame
import self as self
from  pygame.locals import *
from pygame import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60





screen_width = 600
screen_height = 900
screen = pygame.display.set_mode((screen_width,screen_height)) # creating the game window
pygame.display.set_caption("Flappy Bird ")




#define font
font = pygame.font.SysFont('Bauhaus 93' , 60)

white = (255,255,255)


#define game variables
ground_scroll = 0
scroll_speed = 4  # every iteration is moved by 4 pixels
flying = False
gameOver = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe =pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False



#loading images
bg = pygame.image.load('/Users/wassef/PycharmProjects/FlappyBird/venv/img/bg.png')
ground_img = pygame.image.load("/Users/wassef/PycharmProjects/FlappyBird/venv/img/ground.png")
btn_img = pygame.image.load("/Users/wassef/PycharmProjects/FlappyBird/venv/img/restart.png")







#draw text
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height/2)
    score  =0
    return score











class Bird(pygame.sprite.Sprite):                   #pygame module with basic game object classes,Simple base class for visible game objects.
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'/Users/wassef/PycharmProjects/FlappyBird/venv/img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()           #create a rectangle for the image
        self.rect.center = [x,y]
        self.vel = 0                                #vel is for appling gravity to the bird and be always down
        self.clicked = False





    def update(self):
        if flying == True:

            #gravity
            self.vel += 0.5
            if self.vel > 8 :
                self.vel = 8
            if self.rect.bottom < 700:
                self.rect.y += int(self.vel)
        if gameOver == False:

           #jumping
            if pygame.mouse.get_pressed()[0] == False  and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == True:
                self.clicked = False

            # handle the images
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown :
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

             #rotate the bird
            self.image = pygame.transform.rotate( self.images[self.index],self.vel*-2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)









class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('venv/img/pipe.png')
        self.rect=self.image.get_rect()
        #position 1 to -1 btm
        if position == 1:
            self.image=pygame.transform.flip(self.image,False,True) #x and y axes
            self.rect.bottomleft = [x,y - int(pipe_gap)/2]
        if position ==-1:
            self.rect.topleft = [x,y + int(pipe_gap)/2]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.height<200:
            self.kill()





class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft=(x ,y)
    def draw(self):

        action = False

        pos =  pygame.mouse.get_pos()
        #check over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed( )[0] == 1:
                action = True


        #draw btn

        screen.blit(self.image,(self.rect.x,self.rect.y))

        return action










bird_group = pygame.sprite.Group()              #A container class to hold and manage multiple Sprite objects.

pipe_group = pygame.sprite.Group()





flappy = Bird(100, int(screen_height/2))
bird_group.add(flappy)                          #add instance into the group

#create restart butt
button = Button(screen_width // 2 - 50  , screen_height//2 -100 , btn_img)














run = True
while run :                                 #game loop : finishes when something happens


    clock.tick(fps)

                                            #droaw the background
    screen.blit(bg , (0,0))

    bird_group.draw(screen)                 #draw the birdGroup images into the screen
    bird_group.update()
    pipe_group.draw(screen)  # draw the birdGroup images into the screen

#draw the ground
    screen.blit( ground_img,(ground_scroll,700))
    #check score
    if len(pipe_group) > 0 :
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and  pass_pipe  == False:
            pass_pipe = True
        if pass_pipe == True :
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False


    draw_text(str(score),font,white,int(screen_width)/2,20)

    #collide groups
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top < 0 :
        gameOver = True
    #check ground
    if flappy.rect.bottom >=  700:
        gameOver = True
        flying = False

    if gameOver == False and flying == True  :

        #generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now-last_pipe> pipe_frequency:
            pipe_height = random.randint(-100,100)

            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width , int(screen_height / 2) + pipe_height , 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        #draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35 :
            ground_scroll = 0
        pipe_group.update()

    #check for gameover and reset
    if gameOver == True:
        if button.draw() == True:
            gameOver = False
            score = reset_game()

    for event in pygame.event.get():        #events list in pygame
        if event.type == pygame.QUIT:       #clicking the red button of the window ends the loop
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameOver == False:
            flying = True
    pygame.display.update()

pygame.quit()