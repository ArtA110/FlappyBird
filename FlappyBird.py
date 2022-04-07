import sys
from time import sleep
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
from datetime import datetime



# Attr
score = 0
HighScore = 0
fpsTick = 60
speedPermission= False
try:
    with open('resources/save/HighScore.txt','r') as f:
        HighScore = int(f.read())
except:
    pass
screen_height = 504
screen_width = 900
floor_x = 0
pipe_x =0
fps = pygame.time.Clock()
gravity = 0.2
fall_speed = 0
pipe_image_rect=[]
pipe_image_rect2=[]
PipeTime = 0
pygame.font.init()
game_font = pygame.font.Font('resources/font/Flappy.TTF', 25)
game_font_small = pygame.font.Font('resources/font/Flappy.TTF', 18)
random.seed(str(datetime.now()))
main_screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('FlappyBird!')
back_image = pygame.image.load("resources/img/BG.png")
pipe_image=pygame.image.load("resources/img/pipe_green.png")
pipe_image2=pygame.image.load("resources/img/pipe_red.png")
floor_image = pygame.transform.scale(
    pygame.image.load("resources/img/floor.png"), (900, 100))
floor_image_copy = floor_image
bird_image = pygame.image.load("resources/img/red_bird_mid_flap.png")
pygame.mixer.init()
#background_music = pygame.mixer.music.load("resources/sound/BgMusic.mp3")
#pygame.mixer.music.play(-1)
 # Get Coordinations of objects
bird_image_rect = bird_image.get_rect(center=(50, 180))


def pipeGenerator():
    pipe_length = random.randint(120,350)
    pipe_img = pygame.transform.scale(pipe_image,(52,pipe_length))
    pipe_image_rect.append (pipe_img.get_rect(bottom=504,left=900))
    pipe_length = 400 - pipe_length
    pipe_img = pipe_image
    pipe_image_rect2.append (pipe_img.get_rect(center=(926,pipe_length-190)))


def checkCollisions():
    
    if bird_image_rect.bottom >= 428 or bird_image_rect.y <= -3:
        text1 = game_font.render("Out of borders!", False, (255, 0, 0))
        text1_rect = text1.get_rect(left=50,bottom=484)
        main_screen.blit(text1, text1_rect)
        return True
    for i,j in zip(pipe_image_rect,pipe_image_rect2):
        if bird_image_rect.colliderect(i) or bird_image_rect.colliderect(j):
            text1 = game_font.render("Collision Occured!", False, (255, 0, 0))
            text1_rect = text1.get_rect(left=50,bottom=484)
            main_screen.blit(text1, text1_rect)
            return True
    return False

def scoreCal():
    global HighScore,score,speedPermission
    if score > HighScore:
        HighScore = score
    for i in pipe_image_rect:
        if i.right == bird_image_rect.left:
            pygame.mixer.music.load("resources/sound/score.mp3")
            pygame.mixer.music.play()
            score += 1
            speedPermission = True
    text1 = game_font_small.render(f"Score : {score}", False, (255, 255, 255))
    text1_rect = text1.get_rect(center=(450,455))
    text2 = game_font_small.render(f"High Score : {HighScore}", False, (255, 255, 255))
    text2_rect = text2.get_rect(center=(450,480))
    main_screen.blit(text1, text1_rect)
    main_screen.blit(text2, text2_rect)

def gameOver():
    pygame.display.update()
    pygame.mixer.music.load("resources/sound/GO.mp3")
    pygame.mixer.music.play()
    sleep(5)
    global score,gravity,fall_speed,pipe_image_rect,pipe_image_rect2,PipeTime,bird_image_rect,HighScore
    with open("resources/save/HighScore.txt",'w') as f:
        f.write(str(HighScore))
    score = 0
    gravity = 0.2
    fall_speed = 0
    pipe_image_rect=[]
    pipe_image_rect2=[]
    PipeTime = 0
    bird_image_rect = bird_image.get_rect(center=(50, 180))

  # Game runner
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # END PYGAME MODULES
            pygame.quit()
            # TERMINATE PROGRAM
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fall_speed=-4

                    

    main_screen.blit(back_image, (0, 0))
    main_screen.blit(floor_image, (floor_x, 410))
    main_screen.blit(floor_image, (floor_x+504, 410))
    main_screen.blit(bird_image, bird_image_rect)
    
    PipeTime+=.5
    if PipeTime == 90:
        PipeTime = 0 
        pipeGenerator()
    for i,j in zip(pipe_image_rect,pipe_image_rect2):
        main_screen.blit(pipe_image2,j)
        main_screen.blit(pipe_image,i)
        i.centerx -= 1
        j.centerx -= 1
        if i.centerx <= -200:
            pipe_image_rect.pop(0)
        if j.centerx <= -200:
            pipe_image_rect2.pop(0)
    main_screen.blit(floor_image, (floor_x, 410))
    main_screen.blit(floor_image, (floor_x+504, 410))
    fall_speed += gravity
    bird_image_rect.centery += fall_speed
    scoreCal()
    floor_x -= 1  # speed of ground
    if floor_x == -504:
        floor_x = 0  
    if checkCollisions():
        gameOver()
    pygame.display.update()
    if score % 10 == 0 and speedPermission:
        pygame.mixer.music.load("resources/sound/nextlevel.mp3")
        pygame.mixer.music.play()
        fpsTick += 10
        speedPermission = False
        print('HERE')
    fps.tick(fpsTick)