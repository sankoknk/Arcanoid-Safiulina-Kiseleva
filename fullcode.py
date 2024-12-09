import random
import pygame
import sys
import math

pygame.init()

# ПАРАМЕТРЫ ЭКРАНА
screen_w = 600
screen_h = 800
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Arcanoid')

clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 16)


# image = pygame.image.load("image1.jpg")
# image = pygame.transform.scale(image, (screen_w, screen_h))


class Plblock:
    def __init__(self):  # ПАРАМЕТРЫ ИГРОВОГО БЛОКА
        self.plblock_w = 150
        self.plblock_h = 15
        self.rect = pygame.Rect(screen_w // 2 - self.plblock_w // 2, screen_h - self.plblock_h - 60, self.plblock_w,
                                self.plblock_h)
        self.plblock_speed = 6

    def update(self):  # ДВИЖЕНИЕ ИГРОВОГО БЛОКА
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.plblock_speed
        if key[pygame.K_RIGHT] and self.rect.x < screen_w - self.plblock_w:
            self.rect.x += self.plblock_speed

    def render(self):  # СОЗДАНИЕ БЛОКА
        pygame.draw.rect(screen, (139, 0, 0), self.rect)


plblock = Plblock()


class Platform:
    def __init__(self, x, y):
        self.platform_w = 60
        self.platform_h = 20
        self.rect = pygame.Rect(x, y, self.platform_w, self.platform_h)
        self.vec_topright = pygame.Vector2(self.rect.topright) - pygame.Vector2(self.rect.center)
        self.vec_bottomright = pygame.Vector2(self.rect.bottomright) - pygame.Vector2(self.rect.center)
        self.vec_bottomleft = pygame.Vector2(self.rect.bottomleft) - pygame.Vector2(self.rect.center)
        self.vec_topleft = pygame.Vector2(self.rect.topleft) - pygame.Vector2(self.rect.center)

    def render(self):
        pygame.draw.rect(screen, (255, 160, 122), self.rect)


platforms = []
for x in range(25, screen_w - 65, 75):
    for y in range(30, screen_h // 2, 35):
        platforms.append(Platform(x, y))


def liesbetween(a: pygame.Vector2, b: pygame.Vector2, c: pygame.Vector2):
    return a.cross(b) * a.cross(c) >= 0 and c.cross(b) * c.cross(a) >= 0


class Ball:
    def __init__(self):
        self.ball_r = 20
        self.rect = pygame.Rect(screen_w // 2 - self.ball_r // 2, screen_h - self.ball_r - plblock.plblock_h - 60,
                                self.ball_r, self.ball_r)
        self.speed = 5
        self.dir_x = 1
        self.dir_y = -1

    def update(self):
        # шарик и экран
        self.rect.x += self.speed * self.dir_x
        self.rect.y += self.speed * self.dir_y
        if screen_w - self.ball_r < self.rect.x or self.rect.x < 0:
            self.dir_x = - self.dir_x
        if screen_h - self.ball_r < self.rect.y or self.rect.y < 0:
            self.dir_y = - self.dir_y
        # шарик и игровая платформа
        if self.rect.colliderect(plblock.rect) and self.dir_y > 0:
            self.dir_y = - self.dir_y
        # ВЗАИМОДЕЙСТВИЕ ШАРИКА И ПЛАТФОРМ
        for platform in platforms:
            # вектор от центра платформы до центра шарика
            vector = pygame.Vector2(self.rect.center) - pygame.Vector2(platform.rect.center)
            # проверка с какой стороны платформы произошло столкновение
            if self.rect.colliderect(platform.rect):
                if liesbetween(platform.vec_topright, vector, platform.vec_bottomright):  # справа
                    ball.dir_x = - ball.dir_x
                if liesbetween(platform.vec_topright, vector, platform.vec_topleft):  # сверху
                    ball.dir_y = - ball.dir_y
                if liesbetween(platform.vec_topleft, vector, platform.vec_bottomleft):  # слева
                    ball.dir_x = - ball.dir_x
                if liesbetween(platform.vec_bottomleft, vector, platform.vec_bottomright):  # снизу
                    ball.dir_y = - ball.dir_y

                platforms.remove(platform)
                game.score += 1

    def render(self):
        pygame.draw.rect(screen, (178, 34, 34), self.rect)


ball = Ball()

class Game:
    def __init__(self):
        self.lives = 3
        self.score = 0

    def draw_lives(self):
        lives_t = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(lives_t, (10, 10))

    def draw_score(self):
        score_t = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_t, (screen_w - 80, 10))

    def gameover(self) :
        if ball.rect.y + ball.ball_r >= screen_h:
            self.lives -= 1
            ball.__init__()

        if self.lives <= 0:
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (screen_w // 2 - 100, screen_h // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.quit()
game = Game()


time = 400

# ЗАДАЕМ МОМЕНТ ВЫКЛЮЧЕНИЯ ПРОГРАМЫ
while True:
    for e1 in pygame.event.get():
        if e1.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    time = time - 1
    if time == 0:
        for platform in platforms:
            platform.rect.y = platform.rect.y + 35
        for x in range(25, screen_w - 65, 75):
            platforms.append(Platform(x, 30))
        time = 400

    # screen.blit(image, (0,0))
    screen.fill((0, 0, 0))

    plblock.update()
    plblock.render()

    for platform in platforms:
        platform.render()

    ball.update()
    ball.render()

    game.draw_score()
    game.draw_lives()
    game.gameover()

    pygame.display.flip()

    clock.tick(60)
