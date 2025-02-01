import pygame
import random

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 550
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 36)
pygame.display.set_caption("Space Shooter")


HEALTH_GREEN = (0, 255, 0)
DARK_RED = (139, 0, 0)
SCORE_TEXT = (255, 255, 255)
SCORE_COLOR = (255, 255, 255)
FPS_COLOR = (255, 255, 0)

pygame.mixer.init()
pygame.mixer.music.load("sounds/bgspacemusic.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

background = pygame.image.load("images/galaxybg.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_image = pygame.image.load("images/player_ship.png")
player_width, player_height = 50, 50
player_image = pygame.transform.scale(player_image, (player_width, player_height))

enemy_image = pygame.image.load("images/enemy_ship.png")
enemy_width, enemy_height = 50, 50
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

bullet_image = pygame.image.load("images/bullet.png")
bullet_width, bullet_height = 20, 20
bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))

player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - player_height - 100
player_speed = 5

bullets = []
enemies = []
bullet_speed = 10
enemyspawn_pause = 1000
enemyspawn_time = pygame.time.get_ticks()

max_health = 100
current_health = max_health
score = 0

clock = pygame.time.Clock()

running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + (player_width // 2) - (bullet_width // 2)
                bullet_y = player_y
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_d]:
        player_x += player_speed

    

    for bullet in bullets:
        bullet.y -= bullet_speed
    bullets = [bullet for bullet in bullets if bullet.y > 0]
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    current_time = pygame.time.get_ticks()
    if current_time - enemyspawn_time > enemyspawn_pause:
        enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
        enemy_y = random.randint(0, SCREEN_HEIGHT // 2)
        enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))
        enemyspawn_time = current_time
    




    screen.blit(player_image, (player_x, player_y))
    for bullet in bullets:
        screen.blit(bullet_image, (bullet.x, bullet.y))
    for enemy in enemies:
        screen.blit(enemy_image, (enemy.x, enemy.y))

    player_x = max(0, min(player_x, SCREEN_WIDTH - player_width))
    player_y = max(0, min(player_y, SCREEN_HEIGHT - player_height))
    health_ratio = current_health / max_health
    health_bar_width = int(health_ratio * 900)
    pygame.draw.rect(screen, DARK_RED, (50, SCREEN_HEIGHT - 20, 900, 10))
    pygame.draw.rect(screen, HEALTH_GREEN, (50, SCREEN_HEIGHT - 20, health_bar_width, 10))
    score_text = font.render(f"Score: {score}", True, SCORE_COLOR)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
