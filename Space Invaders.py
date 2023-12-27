# importing the modules
import pygame
import math
import random
from pygame import mixer

# initializing pygame
pygame.init()

# setting the dimensions of the screen
screen = pygame.display.set_mode((800, 600))

# loading images
icn = pygame.image.load("imgs/s.png")
background = pygame.image.load("imgs/b.png")
player = pygame.image.load("imgs/player.png")

# default score
score_val = 0

# player locations
playerX = 370
playerY = 480
playerX_change = 0

# an array of enemies
enemy = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

# number of enemies to face
num_of_enemies = 6

# enemy defaults
for i in range(num_of_enemies):
    enemy.append(pygame.image.load("imgs/enemy.png"))
    enemyX.append(random.randint(6, 735))
    enemyY.append(random.randint(50, 150))
    #start moving for x-axis
    enemyX_change.append(0.5)
    enemyY_change.append(35)

# setting the icon and caption
pygame.display.set_icon(icn)
pygame.display.set_caption("Space Invaders")

# bullet defaults
bullet = pygame.image.load("imgs/bulleta.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.8
bullet_state = "invisible"


# function to fire bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "visible"
    screen.blit(bullet, (x + 16, y + 10))


# collision detection
def collide(enemyX, enemyY, bulletX, bulletY):
    # to find distance between two objects we use root of (x2 -x1)^2 - (y2 -y1)^2
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# run state
run = True

# the main while loop
while run:
    # displaying the background throughout the game
    screen.blit(background, (0, 0))

    # basic quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # keyboard inputs checking if pressed
        if event.type == pygame.KEYDOWN:

            # if left arrow is pressed the move to the negative direction of x
            if event.key == pygame.K_LEFT:
                playerX_change = -1

            # if right then move to the positive direction of x
            if event.key == pygame.K_RIGHT:
                playerX_change = 1

            # if space then fire bullet
            if event.key == pygame.K_SPACE:
                mixer.music.load("sfx/laser.wav")
                mixer.music.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        # if key released stop changing the player x
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # if player goes on 0 value on x then re blit the player on 0 and same for 736 x value
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # add the total x change to move the player
    playerX += playerX_change

    # after that blit the player
    screen.blit(player, (playerX, playerY))
    for i in range(num_of_enemies):
        #check if enemy is at the end if yes then add  x-change and also move a bit in y-axis
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.8
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.8
            enemyY[i] += enemyY_change[i]

        # if enemy reaches the 440 y-axis then display GAME OVER
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            font1 = pygame.font.Font("fonts/Oswald-Medium.ttf", 76)
            font2 = pygame.font.Font("fonts/Oswald-Medium.ttf", 56)
            game_over_text = font1.render("GAME OVER", True, (255, 0, 0))
            ur_score = font2.render("Your Score: "+str(score_val), True, (0, 255, 0))
            screen.blit(game_over_text, (235, 235))
            screen.blit(ur_score, (240, 335))

        # check the collision of enemy and bullet
        collision = collide(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            mixer.music.load("sfx/explosion.wav")
            mixer.music.play()
            bulletY = 480
            bullet_state = "invisible"
            score_val += 1
            a = score_val
            enemyX[i] = random.randint(6, 735)
            enemyY[i] = random.randint(50, 150)
        enemyX[i] += enemyX_change[i]
        screen.blit(enemy[i], (enemyX[i], enemyY[i]))

    # if bullet state is visible then fire_bullet(function)
    # Bullet X = Player X when space is pressed
    # this make new position for bullet to follow the path rather than moving in front of player always
    if bullet_state == "visible":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # if the bullet reaches 0
    # at y position then set
    # the bullet_state back to
    # invisible and the bullet Y 480
    if bulletY < 0:
        bullet_state = "invisible"
        bulletY = 480

    #after all the score changes blit the score
    font = pygame.font.Font("fonts/Oswald-Medium.ttf", 28)
    text = font.render("Score: " + str(score_val), True, (255, 255, 255))
    screen.blit(text, (0, 0))
    pygame.display.update()
