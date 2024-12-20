from random import randint

import pygame

pygame.init()

# ПАРАМЕТРЫ ЭКРАНА
SCREEN_W = 600
SCREEN_H = 600
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Arcanoid')

CLOCK = pygame.time.Clock()
TITLE_FONT = pygame.font.Font("font/BadeenDisplay-Regular.ttf", 100)
BUTTON_FONT = pygame.font.Font("font/Jersey10-Regular.ttf", 60)
SCOREBOARD_FONT = pygame.font.Font("font/Jersey10-Regular.ttf", 20)
GAME_OVER_FONT = pygame.font.Font("font/Jersey10-Regular.ttf", 60)


class Plblock:
    def __init__(self):  # ПАРАМЕТРЫ ИГРОВОГО БЛОКА
        self.plblock_w = 100
        self.plblock_h = 15
        self.rect = pygame.Rect(
            SCREEN_W // 2 - self.plblock_w // 2,
            SCREEN_H - self.plblock_h - 60,
            self.plblock_w,
            self.plblock_h
        )
        self.plblock_speed = 6
        self.image = pygame.image.load("img/plblock.png")

    def update(self):  # ДВИЖЕНИЕ ИГРОВОГО БЛОКА
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.plblock_speed
        if key[pygame.K_RIGHT] and self.rect.x < SCREEN_W - self.plblock_w:
            self.rect.x += self.plblock_speed

    def render(self):  # СОЗДАНИЕ БЛОКА
        self.update()
        SCREEN.blit(self.image, self.rect)


class Platform:
    def __init__(self, x, y):
        self.platform_w = 60
        self.platform_h = 20
        self.rect = pygame.Rect(x, y, self.platform_w, self.platform_h)
        self.image = pygame.image.load("img/platform.png")

        self.vec_topright = pygame.Vector2(self.rect.topright) - pygame.Vector2(self.rect.center)
        self.vec_bottomright = pygame.Vector2(self.rect.bottomright) - pygame.Vector2(self.rect.center)
        self.vec_bottomleft = pygame.Vector2(self.rect.bottomleft) - pygame.Vector2(self.rect.center)
        self.vec_topleft = pygame.Vector2(self.rect.topleft) - pygame.Vector2(self.rect.center)

    def render(self):
        SCREEN.blit(self.image, self.rect)


class Ball:
    def __init__(self):
        self.radius = 10
        self.rect = pygame.Rect(
            (SCREEN_W // 2 - self.radius // 2, SCREEN_H - self.radius - plblock.plblock_h - 60),
            (self.radius, self.radius)
        )
        self.speed = 8
        self.dir = pygame.Vector2(randint(-100, 100), randint(-125, -75)).normalize() * self.speed
        self.image = pygame.image.load("img/ball.png")

        self.plblock_bounce_sound = pygame.mixer.Sound("sounds/bounce_plblock.wav")
        self.break_block_sound = pygame.mixer.Sound("sounds/break_block.mp3")

    def update(self):
        # шарик и экран
        self.rect.move_ip(self.dir.x, self.dir.y)
        if SCREEN_W - self.radius < self.rect.x or self.rect.x < 0:
            self.dir.x *= -1
            pygame.mixer.find_channel().play(self.plblock_bounce_sound)
        if SCREEN_H - self.radius < self.rect.y or self.rect.y < 0:
            self.dir.y *= -1
            pygame.mixer.find_channel().play(self.plblock_bounce_sound)
        # шарик и игровая платформа
        if self.rect.colliderect(plblock.rect) and self.dir.y > 0:
            self.rect.bottom = plblock.rect.top + 1  # чуть-чуть поможем игроку, плюс чтобы не застревало
            if abs(ball.rect.centerx - plblock.rect.centerx) < plblock.rect.width * 0.3:  # попали не в край платформы?
                self.dir.y *= -1
            else:
                relative_vector = (
                      pygame.Vector2(
                          plblock.rect.centerx,
                          plblock.rect.centery - 50
                      ) - pygame.Vector2(self.rect.center)
                ).normalize() * self.speed
                relative_vector.x *= -1
                self.dir = relative_vector
            pygame.mixer.find_channel().play(self.plblock_bounce_sound)
        # ВЗАИМОДЕЙСТВИЕ ШАРИКА И ПЛАТФОРМ
        for platform in platforms:
            # проверка с какой стороны платформы произошло столкновение
            if self.rect.colliderect(platform.rect):
                def lies_between(a: pygame.Vector2, b: pygame.Vector2, c: pygame.Vector2):
                    return a.cross(b) * a.cross(c) >= 0 and c.cross(b) * c.cross(a) >= 0

                # вектор от центра платформы до центра шарика
                vector = pygame.Vector2(self.rect.center) - pygame.Vector2(platform.rect.center)
                if lies_between(platform.vec_topright, vector, platform.vec_bottomright):  # справа
                    ball.rect.left = platform.rect.right
                    ball.dir.x = -ball.dir.x
                if lies_between(platform.vec_topright, vector, platform.vec_topleft):  # сверху
                    ball.rect.bottom = platform.rect.top
                    ball.dir.y = -ball.dir.y
                if lies_between(platform.vec_topleft, vector, platform.vec_bottomleft):  # слева
                    ball.rect.right = platform.rect.left
                    ball.dir.x = -ball.dir.x
                if lies_between(platform.vec_bottomleft, vector, platform.vec_bottomright):  # снизу
                    ball.rect.top = platform.rect.bottom
                    ball.dir.y = -ball.dir.y

                platforms.remove(platform)
                pygame.mixer.find_channel().play(self.break_block_sound)
                game.score += 1

    def render(self):
        self.update()
        SCREEN.blit(self.image, ball.rect)


class Game:
    def __init__(self):
        self.lives = 3
        self.score = 0
        self.losing_life_sound = pygame.mixer.Sound("sounds/losing_life.mp3")

    def draw_lives(self):
        lives_t = SCOREBOARD_FONT.render(f"Lives: {self.lives}", True, (255, 255, 255))
        SCREEN.blit(lives_t, (10, 5))

    def draw_score(self):
        score_t = SCOREBOARD_FONT.render(f"Score: {self.score}", True, (255, 255, 255))
        SCREEN.blit(score_t, (SCREEN_W - 80, 5))

    def process_game_over(self):
        if ball.rect.y + ball.radius >= SCREEN_H:
            self.lives -= 1
            pygame.mixer.find_channel().play(self.losing_life_sound)
            ball.__init__()

        if self.lives <= 0:
            SCREEN.blit(game_over_text, (SCREEN_W // 2 - 100, SCREEN_H // 2))
            global high_score
            high_score = max(high_score, self.score)
            set_game_state_game_over()


class Button:
    def __init__(self, x, y, text, callback):
        self.rect = pygame.Rect((0, 0), (300, 100))
        self.rect.center = (x, y)
        self.text = text
        self.callback = callback
        self.pressed = False

    def render(self):
        self.update()
        text = BUTTON_FONT.render(self.text, True, (255, 255, 255))
        pygame.draw.rect(SCREEN, (129, 13, 161) if self.pressed else (203, 13, 255), self.rect)
        SCREEN.blit(text, text.get_rect(center=self.rect.center))

    def update(self):
        cursor = pygame.mouse.get_pos()
        if self.rect.collidepoint(cursor):
            if any(pygame.mouse.get_pressed()):
                self.pressed = True
            elif self.pressed:
                self.callback()
                self.__init__(self.rect.centerx, self.rect.centery, self.text, self.callback)
                return
        else:
            self.pressed = False


# состояние игры
GAME_STATE = "MENU"  # может быть MENU, GAME, GAME_OVER


# объявление переменных меню
def set_game_state_menu():  # костыль, но что поделать, в лямбдах присваивание не работает
    global GAME_STATE
    GAME_STATE = "MENU"
    pygame.mixer.music.unload()
    pygame.mixer.music.load("sounds/menu_background.mp3")
    pygame.mixer.music.play(loops=-1)


def set_game_state_game():
    global GAME_STATE
    reset_game()
    GAME_STATE = "GAME"
    pygame.mixer.music.unload()
    pygame.mixer.music.load("sounds/game_background.mp3")
    pygame.mixer.music.play(loops=-1)


def set_game_state_game_over():
    global GAME_STATE
    GAME_STATE = "GAME_OVER"
    pygame.mixer.music.unload()
    pygame.mixer.music.load("sounds/game_over.mp3")
    pygame.mixer.music.play(loops=1)


play_button = Button(SCREEN_W // 2, SCREEN_H // 2 - 60, "Play", set_game_state_game)
menu_background = pygame.image.load("img/menu_background.png")
quit_button = Button(
    SCREEN_W // 2,
    SCREEN_H // 2 + 60,
    "Quit",
    lambda: pygame.event.post(pygame.event.Event(pygame.QUIT))
)
title_text = TITLE_FONT.render("Arcanoid", True, (219, 33, 179))
high_score = 0
# объявление переменных игры
game = Game()
plblock = Plblock()
ball = Ball()
platforms = []
time = 400
game_background = pygame.image.load("img/game_background.png")


def reset_game():
    global game, plblock, ball, platforms
    game.__init__(), plblock.__init__(), ball.__init__()
    platforms = []
    for x in range(30, SCREEN_W - 65, 60):
        for y in range(30, SCREEN_H // 4, 20):
            platforms.append(Platform(x, y))


# объявление переменных экрана окончания игры
game_over_text = GAME_OVER_FONT.render("Game Over", True, (255, 0, 0))
to_menu_button = Button(SCREEN_W // 2, SCREEN_H // 2, "To menu", set_game_state_menu)
game_over_background = pygame.image.load("img/game_over_background.png")

set_game_state_menu()
# ЗАДАЕМ МОМЕНТ ВЫКЛЮЧЕНИЯ ПРОГРАМЫ
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            break

    SCREEN.fill((0, 0, 0))

    if GAME_STATE == "MENU":
        SCREEN.blit(menu_background, (0, 0))
        play_button.render()
        quit_button.render()
        SCREEN.blit(title_text, title_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 200)))
        if high_score:
            high_score_text = GAME_OVER_FONT.render("High score: " + str(high_score), True, (255, 0, 0))
            SCREEN.blit(high_score_text, high_score_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 200)))

    elif GAME_STATE == "GAME":
        SCREEN.blit(game_background, (0, 0))
        time -= 1
        if time == 0:
            for platform in platforms:
                platform.rect.y += 20
            for x in range(30, SCREEN_W - 65, 60):
                platforms.append(Platform(x, 30))
            time = 1200

        plblock.render()

        for platform in platforms:
            platform.render()

        ball.render()

        game.draw_score()
        game.draw_lives()
        game.process_game_over()

    elif GAME_STATE == "GAME_OVER":
        SCREEN.blit(game_over_background, (0, 0))
        to_menu_button.render()
        SCREEN.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 100)))
        score_text = GAME_OVER_FONT.render("Score: " + str(game.score), True, (255, 0, 0))
        SCREEN.blit(score_text, score_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 100)))

    pygame.display.flip()
    CLOCK.tick(60)
