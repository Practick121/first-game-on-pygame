# подключение модулей
import pygame
import sys
import os
import random

# определение констант, классов, функций
FPS = 100
WIDTH = 1200
HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
name = "Какая-то игра"
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
path = resource_path(os.path.join('images'))
def events(player, i):

    if i.type == pygame.QUIT:
        sys.exit()
            
    elif i.type == pygame.KEYDOWN:
        if i.key == player.right:
            player.motion.add("right")
        elif i.key == player.left:
            player.motion.add('left')
        elif i.key == player.straight:
            player.motion.add('up')
        elif i.key == player.back:
            player.motion.add('down')
    elif i.type == pygame.KEYUP:
        if i.key == player.back and 'down' in player.motion:
            player.motion.remove('down')
        if i.key == player.straight and 'up' in player.motion:
            player.motion.remove('up')
        if i.key == player.left and 'left' in player.motion:
            player.motion.remove('left')
        if i.key == player.right and 'right' in player.motion:
            player.motion.remove('right')
class Player(pygame.sprite.Sprite):
    # инициализация
    def __init__(self, screen, path, keys = (), *args):
        self.screen = screen
        self.original_image = pygame.image.load(path).convert_alpha()
        self.original_image = pygame.transform.scale(\
            self.original_image, (self.original_image.get_width() * 2, self.original_image.get_height() * 2))
        self.image = self.original_image
        self.screen_rect = screen.get_rect()
        self.rect = self.image.get_rect(centerx=random.randint(50, 1000), centery=random.randint(50, 700))
        self.pos = pygame.Vector2((self.rect.centerx, self.rect.centery))
        self.direction = pygame.Vector2((0, -1))
        self.motion = set()  # направления, в которых движется игрок
        self.right = keys[2]  # клавиша для движения направо
        self.left = keys[3]  # клавиша для движения налево
        self.straight = keys[0]  # клавиша для движения прямо
        self.back = keys[1]  # клавиша для движения назад

    def output(self):
        # отрисовка танка
        self.image = pygame.transform.rotate(self.original_image, self.direction.angle_to((0, -1)) + 90)
        self.rect = self.image.get_rect(center=self.pos)
        self.screen.blit(self.image, self.rect)

    def update_pos(self):
        if 'left' in self.motion:
            self.direction.rotate_ip(-1)
        if 'right' in self.motion:
            self.direction.rotate_ip(1)
        if 'up' in self.motion:
            v = self.direction
            v.normalize_ip()
            self.pos += v
        if 'down' in self.motion:
            v = self.direction
            if v.length() > 0:
                v.normalize_ip()
            self.pos -= v



# инициализация, создание объектов
clock = pygame.time.Clock()
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(name)
player1 = Player(window, 'images\зеленый танк.png', (pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a))
player2 = Player(window, 'images\красный танк.png', (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT))
pygame.display.flip()


# главный цикл
while True:
    # обновление экрана
    pygame.display.flip()

    window.fill(GREEN)
    # цикл обработки событий

    for i in pygame.event.get():
        events(player1, i)
        events(player2, i)

    player1.update_pos()
    player2.update_pos()

    player2.output()
    player1.output()
    # задержка
    clock.tick(FPS)