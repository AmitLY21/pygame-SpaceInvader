import random
import math

import pygame

# Init the pygame
pygame.init()

# Title & Icon
icon = pygame.image.load("img/space-game.png")
pygame.display.set_caption("Space Invader")
pygame.display.set_icon(icon)

# Create the Screen aka boundary
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
background = pygame.image.load('img/bg1.jpg')

# Background music
pygame.mixer.music.load('sound/spaceinvaders1.wav')
pygame.mixer.music.play(-1)


# RGB - Red , Green , Blue - Changing background color
def change_bg_color(color):
    screen.fill('#' + color)
    pygame.display.update()


# --------------------Player------------------------
# Player Details
player_img = pygame.image.load('img/player2.png')
player_height = 64
player_width = 64
# Start point
playerX = width / 2 - 32
playerY = height - height / 3
# Movement
playerX_change = 0
playerY_change = 0
player_movement_speed = 0.3

# --------------------Enemy------------------------
# Enemy Details
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
enemy_height = 64
enemy_width = 64
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('img/alien' + str(random.randint(1, 3)) + '.png'))
    # Enemy Movement & Start Point
    enemyX.append(random.randint(0, width - enemy_width - 1))
    enemyY.append(random.randint(50, int(height / 3 - enemy_height)))
    enemyX_change.append(0.15)
    enemyY_change.append(40)

# --------------------Bullet------------------------
bullet_img = pygame.image.load('img/bullet.png')
# Bullet Movement & Start Point
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
# Ready - you cant see the bullet on the screen
# Fire - the bullet is currently moving
bullet_state = "ready"

# --------------------Score------------------------
score_value = 0
font = pygame.font.Font('font/ARCADECLASSIC.TTF', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('font/ARCADECLASSIC.TTF', 64)

# --------------------Sound------------------------
player_death = pygame.mixer.Sound('sound/explosion.wav')
shoot_sound = pygame.mixer.Sound('sound/shoot.wav')
invader_killed_sound = pygame.mixer.Sound('sound/invaderkilled.wav')
game_over_sound = pygame.mixer.Sound('sound/gameover.wav')


def show_score(x, y):
    score = font.render("Score  " + str(score_value), True, [232, 232, 232])
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER!", True, [232, 232, 232])
    screen.blit(over_text, (250, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y - 52))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < 27:
        return True
    return False

# Game Loop
running = True
while running:
    # bg-color
    screen.fill('#151515')
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Movement
        # Player
        # Key down: when the key had been pressed changing the values of X & Y
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change += player_movement_speed
            if event.key == pygame.K_LEFT:
                playerX_change -= player_movement_speed
            if event.key == pygame.K_UP:
                playerY_change -= player_movement_speed
            if event.key == pygame.K_DOWN:
                playerY_change += player_movement_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    # Get current x coordinate of the player
                    shoot_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # Key up: the keys unpressed and reset the change values to 0 both for up&down or right&left
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Setting player boundary's for x (whole screen width) and y (half of screen height)
    if 0 <= playerX + playerX_change <= width - player_width:
        playerX += playerX_change
    if height / 2 <= playerY + playerY_change <= height - player_height:
        playerY += playerY_change

    # Enemy Movement -  Setting enemies boundary's moving from side to side
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            pygame.mixer.music.stop()
            game_over_sound.play(maxtime=1)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = abs(enemyX_change[i])
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= width - enemy_width:
            enemyX_change[i] = abs(enemyX_change[i]) * -1
            enemyY[i] += enemyY_change[i]

        # Collision
        if is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            invader_killed_sound.play()
            enemyX[i] = random.randint(0, width - enemy_width - 1)
            enemyY[i] = random.randint(50, int(height / 3 - enemy_height))

        if is_collision(enemyX[i], enemyY[i], playerX, playerY):
            player_death.play()
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            pygame.mixer.music.stop()

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
