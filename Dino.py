import pygame
import sys
from random import choice, randint
import pygame.freetype
import pygame_menu

X_max = 1280
Y_max = 600
jump_speed = 5
jump_max = 90
game_speed = 10
X_road = 0
score_now = 0

timer = pygame.time.Clock()

pygame.init()
background_color = (255, 255, 255)
screen = pygame.display.set_mode((X_max, Y_max))

Score_font = pygame.freetype.SysFont("Arial", 20)


class Dino(pygame.sprite.Sprite):
    sprite_run = []
    sprite_jump = []
    sprite_duck = []
    Y_dino = Y_max - 180
    X_dino = 100

    def __init__(self):
        super(Dino, self).__init__()
        self.is_Run = True
        self.is_jump = False
        self.is_duck = False
        self.jump_speed = 8.5
        self.load_image()
        self.step_index = 0
        self.image = self.sprite_run[0]
        self.rect = self.image.get_rect()
        self.rect.y = self.Y_dino
        self.rect.x = self.X_dino

    def change_move_type(self, keys):
        if self.is_Run:
            self.run()
        if self.is_jump:
            self.jump()
        if self.is_duck:
            self.duck()

        if keys[pygame.K_SPACE] and not self.is_jump:
            self.is_Run = False
            self.is_jump = True
            self.is_duck = False

        elif keys[pygame.K_DOWN] and not self.is_duck:
            self.is_Run = False
            self.is_duck = True
            self.is_jump = False

        elif not (keys[pygame.K_DOWN] or self.is_jump):
            self.is_Run = True
            self.is_duck = False
            self.is_jump = False

        if self.step_index >= 10:
            self.step_index = 0

    def run(self):
        self.image = self.sprite_run[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.y = self.Y_dino
        self.rect.x = self.X_dino
        self.step_index += 1

    def jump(self):
        self.image = self.sprite_jump[0]
        if self.is_jump:
            self.rect.y -= self.jump_speed * 3
            self.jump_speed -= 0.5
        if self.jump_speed <= -8.5:
            self.is_jump = False
            self.is_Run = True
            self.jump_speed = 8.5

    def duck(self):
        self.image = self.sprite_duck[self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.y = self.Y_dino + 35
        self.rect.x = self.X_dino
        self.step_index += 1

    def load_image(self):
        self.sprite_run.append(pygame.image.load("black_run1.png"))
        self.sprite_run.append(pygame.image.load("black_run2.png"))
        self.sprite_jump.append(pygame.image.load("black_jump.png"))
        self.sprite_duck.append(pygame.image.load("duck/DinoDuck1.png"))
        self.sprite_duck.append(pygame.image.load("duck/DinoDuck2.png"))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Cactus(pygame.sprite.Sprite):
    cactus_type = ["1", "2", "3", "4", "5", "6"]

    def __init__(self):
        super(Cactus, self).__init__()
        self.image = self.load_cactus()
        self.rect = self.image.get_rect()
        self.rect.y = Y_max - 89 - self.image.get_height()
        self.rect.x = X_max

    def update(self):
        self.rect.x -= 2 * game_speed
        if self.rect.x < 0:
            self.kill()

    def change_cactus(self):
        return choice(self.cactus_type)

    def load_cactus(self):
        return pygame.image.load(f"cactus/{self.change_cactus()}.png")

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Pter(pygame.sprite.Sprite):
    pter_fly = []

    def __init__(self):
        super(Pter, self).__init__()
        self.load_images()
        self.image = self.pter_fly[0]
        self.rect = self.image.get_rect()
        self.fly_step = 0
        self.rect.y = Y_max - self._random_height()
        self.rect.x = X_max

    def load_images(self):
        self.pter_fly.append(pygame.image.load("bird/Bird1.png"))
        self.pter_fly.append(pygame.image.load("bird/Bird2.png"))

    def update(self):
        self.rect.x -= game_speed
        self.image = self.pter_fly[self.fly_step // 15]

        if self.fly_step >= 29:
            self.fly_step = 0
        if self.rect.x <= 0:
            self.kill()
        self.fly_step += 1

    def _random_height(self):
        height = [280, 240, 150]
        return choice(height)


class Cloud(pygame.sprite.Sprite):
    cloud_images = []

    def __init__(self):
        super(Cloud, self).__init__()
        self.load_image()
        self.image = pygame.transform.scale(self.cloud_images[0].convert(), (100, 50))
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255))
        self.rect.y = randint(200, 250)
        self.rect.x = X_max

    def load_image(self):
        self.cloud_images.append(pygame.image.load("cloud.jpg"))

    def update(self):
        self.rect.x -= game_speed * 0.75
        print(self.rect.x)
        if self.rect.x < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def road():
    global X_road
    road = pygame.image.load("road.png")
    X_road -= game_speed
    screen.blit(road, (X_road, Y_max - 100))
    screen.blit(road, (X_road + road.get_width(), Y_max - 100))
    if X_road < -road.get_width():
        screen.blit(road, (X_road + road.get_width(), Y_max - 100))
        X_road = 0
    X_road -= game_speed


def score():
    global score_now, game_speed
    score_now += 1
    if score_now % 100 == 0:
        game_speed += 0.2
    Score_font.render_to(screen, (X_max / 2 - 50, 30), f"Score: {score_now}", (0, 0, 0))


def game_cycle():
    GameOn = True

    player = Dino()

    cloud = Cloud()

    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

    global score_now, game_speed
    score_now = 0
    game_speed = 10

    while GameOn:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if len(enemies) == 0:
            rand = randint(0, 2)
            if rand == 0:
                cactus = Cactus()
                enemies.add(cactus)
            elif rand == 1:
                pter = Pter()
                enemies.add(pter)

        if len(clouds) < 3:
            while len(clouds) < 3:
                cloud = Cloud()
                clouds.add(cloud)

        screen.fill(background_color)

        keys_input = pygame.key.get_pressed()
        player.change_move_type(keys_input)

        enemies.update()
        clouds.update()

        enemies.draw(screen)
        player.draw(screen)
        cloud.draw(screen)

        road()
        score()

        if pygame.sprite.spritecollide(player, enemies, False):
             game_over()
        pygame.display.update()
        timer.tick(60)
        pygame.display.flip()


def game_over():
    global score_now
    pygame.init()
    screen = pygame.display.set_mode((X_max, Y_max))
    game_over = pygame_menu.Menu("Game over", 400, 300, theme=pygame_menu.themes.THEME_DEFAULT)
    game_over.add.label(f"Score: {score_now}")

    game_over.add.button("Quit", pygame_menu.events.EXIT)
    game_over.add.button("Restart", game_cycle)
    game_over.mainloop(screen)


def menu():
    pygame.init()
    screen = pygame.display.set_mode((X_max, Y_max))

    menu = pygame_menu.Menu("Dino", 400, 300, theme=pygame_menu.themes.THEME_DEFAULT)

    menu.add.button("Play", game_cycle)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)


if __name__ == '__main__':
    menu()
