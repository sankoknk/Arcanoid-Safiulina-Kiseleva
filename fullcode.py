import sys
import pygame


pygame.init()

# ПАРАМЕТРЫ ЭКРАНА
screen_w = 600
screen_h = 800
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Arcanoid')

clock = pygame.time.Clock()


# ПАРАМЕТРЫ ИГРОВОГО БЛОКА
plblock_w = 150
plblock_h = 30
plblock = pygame.Rect(screen_w // 2 - plblock_w // 2, screen_h - plblock_h - 60, plblock_w, plblock_h)
plblock_speed = 8

class Platform:
    def __init__(self, x, y):
        self.platform_w = 75
        self.platform_h = 25
        self.rect = pygame.Rect(x, y, self.platform_w, self.platform_h)

    def render(self):
        pygame.draw.rect(screen, (255, 160, 122), self.rect)


platforms = []
for x in range(25, screen_w - 75, 85):
    for y in range(30, screen_h // 2, 35):
        platforms.append(Platform(x, y))

# ПАРАМЕТРЫ МЯЧИКА
ball_r = 40
ball = pygame.Rect(screen_w // 2 - ball_r // 2, screen_h - ball_r - plblock_h - 60, ball_r, ball_r)
ball_speed = 5
dir_x = 1  # НАПРАВЛЕНИЕ ДВИЖЕНИЯ
dir_y = -1  # ИЗМЕНЕНИЕ НАПРАВЛЕНИЯ ДВИЖЕНИЯ

# ЗАДАЕМ МОМЕНТ ВЫКЛЮЧЕНИЯ ПРОГРАМЫ
while True:
    for e1 in pygame.event.get():
        if e1.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ЗАДАЕМ ДВИЖЕНИЕ ИГРОВОГО БЛОКА
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and plblock.x > 0:
        plblock.centerx -= plblock_speed
    if key[pygame.K_RIGHT] and plblock.x < screen_w - plblock_w:
        plblock.centerx += plblock_speed

    # ЗАДАЕМ ДВИЖЕНИЕ ШАРИКА
    ball.x += ball_speed * dir_x
    ball.y += ball_speed * dir_y
    if screen_w - ball_r < ball.x or ball.x < 0:
        dir_x = - dir_x
    if screen_h - ball_r < ball.y or ball.y < 0:
        dir_y = - dir_y

    # ОПРЕДЕЛЯЕМ СТОЛКНОВЕНИЕ С ПЛАТФОРМОЙ
    if ball.colliderect(plblock) and dir_y > 0:
        dir_y = - dir_y

    screen.fill((0, 0, 0))
    for platform in platforms:
        pygame.draw.rect(screen, (139, 0, 0), platform)
    pygame.draw.rect(screen, (139, 0, 0), plblock)
    pygame.draw.rect(screen, (178, 34, 34), ball)
    pygame.display.flip()

    clock.tick(60)
