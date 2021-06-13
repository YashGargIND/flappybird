import pygame
import random

pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer= 512)
pygame.init()

screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
gameFont = pygame.font.Font('04B_19.ttf',20)

        # Game specific variables
exitGame = False
gameOver = 2
gravity = 0.25
birdMovement = 0
score = 0
high_score = 0

            # GAME ASSETS
# background
bgSurface = pygame.image.load('img/background-day.png').convert()

# score
def score_display():
        score_surface = gameFont.render(f'score : {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)

        highscore_surface = gameFont.render(f'Highscore : {int(high_score)}', True, (255, 255, 255))
        highscore_rect = highscore_surface.get_rect(center=(144, 475))
        screen.blit(highscore_surface, highscore_rect)


# floor
floorSurface = pygame.image.load('img/base.png').convert()
floorXPos = 0
def draw_floor():
    screen.blit(floorSurface, (floorXPos, 400))
    screen.blit(floorSurface, (floorXPos + 288, 400))

# bird
birdUpflap = pygame.image.load('img/bluebird-upflap.png').convert_alpha()
birdMidflap = pygame.image.load('img/bluebird-midflap.png').convert_alpha()
birdDownflap = pygame.image.load('img/bluebird-downflap.png').convert_alpha()
birdframe = [birdDownflap, birdMidflap, birdUpflap]
birdIndex = 0
birdSurface = birdframe[birdIndex]
birdRect = birdSurface.get_rect(center = (100, 256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 300)
def bird_animation():
    new_bird = birdframe[birdIndex]
    new_bird_rect = new_bird.get_rect(center = (100, birdRect.centery))
    return new_bird,new_bird_rect
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-birdMovement*3,1)
    return new_bird


# game over
gameOverSurface = pygame.image.load('img/gameover.png').convert_alpha()
startMessage = pygame.image.load('img/message.png').convert_alpha()
startMessage = pygame.transform.scale(startMessage, (138, 123))
startMessageRect = startMessage.get_rect(center = (144, 150))

# audio files
flapSound = pygame.mixer.Sound('audio/wing.wav')
dieSound = pygame.mixer.Sound('audio/hit.ogg')

# pipe
pipeSurface = pygame.image.load('img/pipe-green.png').convert()
pipeList=[]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1000 )
pipeHeight = 256
def create_pipe():
    new_pipe_top = pipeSurface.get_rect(midtop=(340, pipeHeight))
    new_pipe_bottom = pipeSurface.get_rect(midbottom=(340, (pipeHeight - 120 )))

    return new_pipe_top, new_pipe_bottom

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def draw_pipe():
    for pipe in pipeList:
        if pipe.bottom > 400:
            screen.blit(pipeSurface, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipeSurface,False, True)
            screen.blit(flipped_pipe, pipe)

def collision_check(pipes):
    rval = 0
    if (birdRect.top > 400) or (birdRect.bottom < 0):
        dieSound.play()
        return 1
    for pipe in pipes:
        if birdRect.colliderect(pipe):
            dieSound.play()
            return 1
    return 0


while not exitGame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitGame = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameOver == 0:
                birdMovement = -5
                flapSound.play()
            if event.key == pygame.K_SPACE  and gameOver == 1:
                gameOver = 2
                birdMovement = 0
                birdRect = birdSurface.get_rect(center = (100, 256))
                pipeList.clear()
                score = 0
                continue;
            if event.key == pygame.K_SPACE  and gameOver == 2:
                gameOver = 0
                birdMovement = 0
                birdMovement = -5
                birdRect = birdSurface.get_rect(center = (100, 256))
                pipeList.clear()
                score = 0
                flapSound.play()
        if event.type == SPAWNPIPE:
            pipeList.extend(create_pipe())
            pipeHeight = (random.randint(5, 11)) * 30
        if event.type == BIRDFLAP:
            if birdIndex < 2:
                birdIndex += 1
            else:
                birdIndex = 0
            birdSurface,birdRect = bird_animation()


    # background
    screen.blit(bgSurface, (0, 0))
    if gameOver ==0 :
        gameOver = collision_check(pipeList)

    if gameOver == 0:
        # bird
        rotated_bird = rotate_bird(birdSurface)
        screen.blit(rotated_bird, birdRect)
        birdMovement += gravity
        birdRect.centery += birdMovement

        # pipes
        pipeList = move_pipe(pipeList)
        draw_pipe()
        score_display()
        score += 0.0075
        # floor
        draw_floor()
        floorXPos -= 1
        if floorXPos < -288:
            floorXPos = 0
        score_display()
    if gameOver == 1:
        draw_pipe()
        draw_floor()
        score_display()
        screen.blit(rotated_bird, birdRect)
        screen.blit(gameOverSurface, (50,200))
    if gameOver == 2:
        draw_pipe()
        draw_floor()
        score_display()
        screen.blit(birdSurface , birdRect)
        screen.blit(startMessage, startMessageRect)
    if score > high_score:
        high_score = score

    pygame.display.update()
    clock.tick(120)

pygame.quit()
quit()
