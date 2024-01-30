import random
import sys
import pygame
from pygame.locals import *

FPS=32
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUND_Y=SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='flappy/bird3.png'
BACKGROUND='flappy/background3.png'
BASE='flappy/base3.png'
PIPE='flappy/pipe3.png'

def welcomescreen():
    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    # messagex=int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    # messagey=int(SCREENHEIGHT*0.13)
    basex=0
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                # SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUND_Y))
                pygame.display.update()
                FPS_CLOCK.tick(FPS)

def maingame():
    score=0
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0

    newpipe1=getrandompipe()
    newpipe2=getrandompipe()

    upperpipes=[
        {'x':SCREENWIDTH+200,'y':newpipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newpipe2[0]['y']}
    ]
    lowerpipes=[ 
        {'x':SCREENWIDTH+200,'y':newpipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newpipe2[1]['y']}
    ]

    pipevelx=-4

    playervely=-9
    playermaxvely=10
    playerminval=-8
    playeraccy=1

    playerflapaccv=-8# velocity while flapping
    playerflapped=False # it is true only when bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playervely=playerflapaccv
                    playerflapped=True
                    GAME_SOUNDS['wing'].play()

        crashtest=iscollide(playerx,playery,upperpipes,lowerpipes)
        if crashtest:
            return
        # for checking score
        playermidpos=playerx+GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes :
            pipemidpos=pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipemidpos<=playermidpos<pipemidpos+4:
                score+=1
                print(f"Your Score is {score}")
                GAME_SOUNDS['point'].play()
                
        if playervely <playermaxvely and not playerflapped:
            playervely+=playeraccy

        if playerflapped:
            playerflapped=False
        playerheight=GAME_SPRITES['player'].get_height()
        playery=playery+min(playervely,GROUND_Y-playery -playerheight)
        
        # moves pipe to left
        for upperpipe ,lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x']+=pipevelx
            lowerpipe['x']+=pipevelx

        # for adding new pipes when the first is about to crooss the leftmost part of the screen
        if 0<upperpipes[0]['x']<5:
            newpipe=getrandompipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        # if the pipe is out of screen remove it
        if upperpipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
        #  lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperpipes, lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def iscollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUND_Y - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getrandompipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe



if __name__=='__main__':

    pygame.init()
    FPS_CLOCK=pygame.time.Clock()
    pygame.display.set_caption('FLAPPY BIRD --ADARSH')
    GAME_SPRITES['numbers']=(
        pygame.image.load('IMAGE/0.png').convert_alpha(),
        pygame.image.load('IMAGE/1.png').convert_alpha(),
        pygame.image.load('IMAGE/2.png').convert_alpha(),
        pygame.image.load('IMAGE/3.png').convert_alpha(),
        pygame.image.load('IMAGE/4.png').convert_alpha(),
        pygame.image.load('IMAGE/5.png').convert_alpha(),
        pygame.image.load('IMAGE/6.png').convert_alpha(),
        pygame.image.load('IMAGE/7.png').convert_alpha(),
        pygame.image.load('IMAGE/8.png').convert_alpha(),
        pygame.image.load('IMAGE/9.png').convert_alpha()
    )
    #GAME_SPRITES['message']=pygame.image.load('IMAGE/message.png').convert_alpha()
    GAME_SPRITES['base']=pygame.image.load(BASE).convert_alpha()
    GAME_SPRITES['pipe']=(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha())
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert_alpha()


    GAME_SOUNDS['die']=pygame.mixer.Sound('SOUND/die.mp3')
    GAME_SOUNDS['hit']=pygame.mixer.Sound('SOUND/hit.mp3')
    GAME_SOUNDS['point']=pygame.mixer.Sound('SOUND/point.mp3')
    GAME_SOUNDS['swoosh']=pygame.mixer.Sound('SOUND/swoosh.mp3')
    GAME_SOUNDS['wing']=pygame.mixer.Sound('SOUND/wing.mp3')

    while True:
        welcomescreen()
        maingame()