import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('bg.png')

# Sounds
mixer.music.load('background.wav')

# Fonts
font = pygame.font.Font('freesansbold.ttf', 32)
button_font = pygame.font.Font('freesansbold.ttf', 24)
over_font = pygame.font.Font('freesansbold.ttf', 65)

# Score
score_value = 0

# Game states
game_started = False
game_paused = False
game_over = False
difficulty_threshold = 50

# Player
playerImg = pygame.transform.scale(pygame.image.load('player.png'), (50, 50))
playerX = 370
playerY = 480
playerX_change = 0

# Bullet
bulletImg = pygame.transform.scale(pygame.image.load('bullet.png'), (32, 32))
bullets = []

# Enemies
enemyImg_base = pygame.transform.scale(pygame.image.load('enemy1.png'), (45, 45))
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_speed = 4

def add_more_enemies(count, speed):
    for _ in range(count):
        enemyImg.append(enemyImg_base)
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(speed)
        enemyY_change.append(40)

add_more_enemies(6, enemy_speed)

# Utility Functions
def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect)
        if click[0] == 1 and action:
            pygame.time.delay(200)
            action()
    else:
        pygame.draw.rect(screen, color, rect)

    text_surf = button_font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surf, text_rect)

def show_score(x, y):
    score_display = font.render(f"Score: {score_value}", True, (255, 255, 0))
    screen.blit(score_display, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    bullets.append([x + 10, y])
    mixer.Sound("laser.wav").play()

def isCollision(enemyX, enemyY, bulletX, bulletY):
    return math.hypot(enemyX - bulletX, enemyY - bulletY) < 27

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

def start_game():
    global game_started
    game_started = True
    mixer.music.play(-1)

def pause_game():
    global game_paused
    game_paused = True
    mixer.music.pause()

def resume_game():
    global game_paused
    game_paused = False
    mixer.music.unpause()

def restart_game():
    global score_value, bullets, playerX, playerX_change, game_paused, game_over, enemy_speed, difficulty_threshold
    bullets.clear()
    enemyImg.clear()
    enemyX.clear()
    enemyY.clear()
    enemyX_change.clear()
    enemyY_change.clear()
    score_value = 0
    difficulty_threshold = 50
    playerX = 370
    playerX_change = 0
    game_paused = False
    game_over = False
    enemy_speed = 4
    add_more_enemies(6, enemy_speed)
    mixer.music.play(-1)

def exit_game():
    pygame.quit()
    exit()

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_started and not game_over and not game_paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -6
                if event.key == pygame.K_RIGHT:
                    playerX_change = 6
                if event.key == pygame.K_SPACE:
                    if len(bullets) < 5:
                        fire_bullet(playerX, playerY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

    if not game_started:
        draw_button("START GAME", 280, 250, 240, 70, (0, 255, 0), (0, 200, 0), start_game)

    elif game_over:
        game_over_text()
        draw_button(" RESTART", 300, 350, 200, 60, (255, 255, 0), (200, 200, 0), restart_game)
        draw_button(" EXIT", 300, 430, 200, 60, (255, 100, 100), (200, 50, 50), exit_game)

    else:
        if game_paused:
            draw_button(" RESUME", 300, 230, 200, 60, (100, 255, 100), (80, 230, 80), resume_game)
            draw_button(" RESTART", 300, 310, 200, 60, (255, 255, 0), (200, 200, 0), restart_game)
            draw_button(" EXIT", 300, 390, 200, 60, (255, 100, 100), (200, 50, 50), exit_game)
        else:
            draw_button("||", 740, 10, 40, 40, (180, 180, 180), (150, 150, 150), pause_game)

            playerX += playerX_change
            playerX = max(0, min(playerX, 750))

            if score_value >= difficulty_threshold:
                difficulty_threshold += 50
                enemy_speed += 1
                add_more_enemies(2, enemy_speed)

            for i in range(len(enemyX)):
                if enemyY[i] > 440:
                    game_over = True
                    mixer.music.stop()
                    break

                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0 or enemyX[i] >= 735:
                    enemyX_change[i] *= -1
                    enemyY[i] += enemyY_change[i]

                enemy(enemyX[i], enemyY[i], i)

            for b in bullets[:]:
                screen.blit(bulletImg, (b[0], b[1]))
                b[1] -= 10
                if b[1] < 0:
                    bullets.remove(b)
                else:
                    for i in range(len(enemyX)):
                        if isCollision(enemyX[i], enemyY[i], b[0], b[1]):
                            mixer.Sound("explosion.wav").play()
                            bullets.remove(b)
                            score_value += 1
                            enemyX[i] = random.randint(0, 735)
                            enemyY[i] = random.randint(50, 150)
                            break

            player(playerX, playerY)
            show_score(10, 10)

    pygame.display.update()

