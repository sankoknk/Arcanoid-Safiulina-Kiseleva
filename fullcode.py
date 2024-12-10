import pygame

pygame.init()

# ПАРАМЕТРЫ ЭКРАНА
SCREEN_W = 600
SCREEN_H = 800
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Arcanoid')

CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Calibri", 16)


class Plblock:
    def __init__(self):  # ПАРАМЕТРЫ ИГРОВОГО БЛОКА
        self.plblock_w = 150
        self.plblock_h = 15
        self.rect = pygame.Rect(SCREEN_W // 2 - self.plblock_w // 2, SCREEN_H - self.plblock_h - 60, self.plblock_w,
                                self.plblock_h)
        self.plblock_speed = 6

    def update(self):  # ДВИЖЕНИЕ ИГРОВОГО БЛОКА
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.plblock_speed
        if key[pygame.K_RIGHT] and self.rect.x < SCREEN_W - self.plblock_w:
            self.rect.x += self.plblock_speed

    def render(self):  # СОЗДАНИЕ БЛОКА
        self.update()
        pygame.draw.rect(SCREEN, (139, 0, 0), self.rect)


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
        pygame.draw.rect(SCREEN, (255, 160, 122), self.rect)


class Ball:
    def __init__(self):
        self.radius = 20
        self.rect = pygame.Rect(
            (SCREEN_W // 2 - self.radius // 2, SCREEN_H - self.radius - plblock.plblock_h - 60),
            (self.radius, self.radius)
        )
        self.speed = 5
        self.dir_x = 1
        self.dir_y = -1

    def update(self):
        # шарик и экран
        self.rect.x += self.speed * self.dir_x
        self.rect.y += self.speed * self.dir_y
        if SCREEN_W - self.radius < self.rect.x or self.rect.x < 0:
            self.dir_x *= -1
        if SCREEN_H - self.radius < self.rect.y or self.rect.y < 0:
            self.dir_y *= -1
        # шарик и игровая платформа
        if self.rect.colliderect(plblock.rect) and self.dir_y > 0:
            self.dir_y *= -1
        # ВЗАИМОДЕЙСТВИЕ ШАРИКА И ПЛАТФОРМ
        for platform in platforms:
            # проверка с какой стороны платформы произошло столкновение
            if self.rect.colliderect(platform.rect):
                def lies_between(a: pygame.Vector2, b: pygame.Vector2, c: pygame.Vector2):
                    return a.cross(b) * a.cross(c) >= 0 and c.cross(b) * c.cross(a) >= 0

                # вектор от центра платформы до центра шарика
                vector = pygame.Vector2(self.rect.center) - pygame.Vector2(platform.rect.center)
                if lies_between(platform.vec_topright, vector, platform.vec_bottomright):  # справа
                    ball.dir_x = - ball.dir_x
                if lies_between(platform.vec_topright, vector, platform.vec_topleft):  # сверху
                    ball.dir_y = - ball.dir_y
                if lies_between(platform.vec_topleft, vector, platform.vec_bottomleft):  # слева
                    ball.dir_x = - ball.dir_x
                if lies_between(platform.vec_bottomleft, vector, platform.vec_bottomright):  # снизу
                    ball.dir_y = - ball.dir_y

                platforms.remove(platform)
                game.score += 1

    def render(self):
        self.update()
        pygame.draw.rect(SCREEN, (178, 34, 34), self.rect)


class Game:
    def __init__(self):
        self.lives = 3
        self.score = 0

    def draw_lives(self):
        lives_t = FONT.render(f"Lives: {self.lives}", True, (255, 255, 255))
        SCREEN.blit(lives_t, (10, 10))

    def draw_score(self):
        score_t = FONT.render(f"Score: {self.score}", True, (255, 255, 255))
        SCREEN.blit(score_t, (SCREEN_W - 80, 10))

    def process_game_over(self):
        if ball.rect.y + ball.radius >= SCREEN_H:
            self.lives -= 1
            ball.__init__()

        if self.lives <= 0:
            SCREEN.blit(game_over_text, (SCREEN_W // 2 - 100, SCREEN_H // 2))
            global GAME_STATE
            GAME_STATE = "GAME_OVER"


# состояние игры
GAME_STATE = "MENU"  # может быть MENU, GAME, GAME_OVER

# объявление переменных меню
play_button = None

# объявление переменных игры
game = Game()
plblock = Plblock()
ball = Ball()
platforms = []
for x in range(25, SCREEN_W - 65, 75):
    for y in range(30, SCREEN_H // 2, 35):
        platforms.append(Platform(x, y))
time = 400

# объявление переменных экрана окончания игры
game_over_text = FONT.render("Game Over", True, (255, 0, 0))

# ЗАДАЕМ МОМЕНТ ВЫКЛЮЧЕНИЯ ПРОГРАМЫ
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            break

    SCREEN.fill((0, 0, 0))
    if GAME_STATE == "MENU":
        pass
    elif GAME_STATE == "GAME":
        pass
    elif GAME_STATE == "MENU":
        pass

    time -= 1
    if time == 0:
        for platform in platforms:
            platform.rect.y += 35
        for x in range(25, SCREEN_W - 65, 75):
            platforms.append(Platform(x, 30))
        time = 400

    plblock.render()

    for platform in platforms:
        platform.render()

    ball.render()

    game.draw_score()
    game.draw_lives()
    game.process_game_over()

    pygame.display.flip()
    CLOCK.tick(60)
