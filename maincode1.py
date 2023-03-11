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
SPEED = 2
SPEEDBUL = 7
name = "Какая-то игра"
def get_key(slovar, item):
    for i, j in slovar.items():
        if j == item:
            return i
    return False
def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)
path = resource_path(os.path.join('images'))
def events(player, i):

    if i.type == pygame.QUIT:
        sys.exit()
            
    elif i.type == pygame.KEYDOWN:
        if i.key == player.keys["right"]:
            player.motion.append("right")
        elif i.key == player.keys["left"]:
            player.motion.append("left")
        elif i.key == player.keys["up"]:
            player.motion.append('up')
        elif i.key == player.keys["down"]:
            player.motion.append("down")
        elif i.key == player.keys["shoot"]:
            if len(player.bullets) < 2:
                bullet = Bullet(player)
            else:
                print("Перезарядка!")
    elif i.type == pygame.KEYUP:
        if i.key == player.keys["up"]:
            player.motion.remove("up")


class Player(pygame.sprite.Sprite):
    players = []
    # инициализация
    def __init__(self, x, y, screen, path, keys=(), *args):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.original_image = pygame.image.load(path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (self.original_image.get_width() / 2,\
                                                                           self.original_image.get_height() / 2))
        self.image = self.original_image
        self.rect = pygame.Rect(\
            x - self.image.get_width() / 2, y - self.image.get_height() / 2, self.image.get_width() - 10, self.image.get_height() - 10)
        self.direction = 0 # угол игрока
        self.motion = []  # направления, в которых движется игрок
        self.keys = {"right": keys[2], "left": keys[3], "up": keys[0],\
                     "down": keys[1] , "shoot": keys[4]} # словарь констант кнопок, на которые будет реагировать спрайт
        self.bullets = []
        Player.players.append(self) #добавление спрайта в список
        self.health = 100 #

    def output(self):
        # отрисовка танка
        self.image = pygame.transform.rotate(self.original_image, self.direction)
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.screen.blit(self.image, self.rect)

    def update_pos(self): # передвижение танка
        if len(self.motion):
            if self.motion[-1] == 'left':
                self.direction += 45
                self.motion.remove("left")
            elif self.motion[-1] == 'right':
                self.direction -= 45
                self.motion.remove("right")
            elif self.motion[-1] == 'up':
                if self.direction == 90:
                    self.rect.centerx -= SPEED
                elif self.direction == 270:
                    self.rect.centerx += SPEED
                elif self.direction == 360:
                    self.rect.centery -= SPEED
                elif self.direction == 180:
                    self.rect.centery += SPEED
            if self.direction > 360:
                self.direction -= 360
            elif self.direction <= 0:
                self.direction += 360


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player): # определение пули
        pygame.sprite.Sprite.__init__(self)
        self.belong = player
        self.surf = pygame.Surface((3, 6))
        self.surf.fill(BLACK)
        self.direction = self.belong.direction
        self.surf = pygame.transform.rotate(self.surf, self.direction)
        self.belong.bullets.append(self)
        self.rect = self.surf.get_rect()
        self.enemy = Player.players.copy()
        self.enemy.remove(self.belong)
        self.enemy = self.enemy[0] # определение противника для этой пули
        if self.direction == 90:
            self.rect.centerx = self.belong.rect.centerx - 50
            self.rect.centery = self.belong.rect.centery
        elif self.direction == 180:
            self.rect.centerx = self.belong.rect.centerx
            self.rect.centery = self.belong.rect.centery + 50
        elif self.direction == 270:
            self.rect.centerx = self.belong.rect.centerx + 50
            self.rect.centery = self.belong.rect.centery
        elif self.direction == 0:
            self.rect.centerx = self.belong.rect.centerx
            self.rect.centery = self.belong.rect.centery - 50

    def fly(self): # перемещение пули по экрану
        if self.direction == 90:
            self.rect.centerx -= SPEEDBUL
        elif self.direction == 180:
            self.rect.centery += SPEEDBUL
        elif self.direction == 360:
            self.rect.centery -= SPEEDBUL
        elif self.direction == 270:
            self.rect.centerx += SPEEDBUL # движени пули взависимости от направления
        window.blit(self.surf, self.rect)
        pygame.display.update(self.rect)
        if self.rect.centerx > WIDTH or self.rect.centerx < 0 or self.rect.centery > HEIGHT or self.rect.centery < 0:
            self.belong.bullets.remove(self) # пуля удаляется если коснулась края или противника
            del self

        elif self.rect.colliderect(self.enemy.rect):
            print("попал!")
            self.enemy.health -= 50
            bam = Boom(self.rect.centerx, self.rect.centery)
            self.belong.bullets.remove(self)
            del self



class Boom:
    sprites = []
    def __init__(self, x, y):
        self.surface = pygame.Surface((5, 5))
        self.rect = self.surface.get_rect(center=(x, y))
        self.surface.fill((255, 0, 0))
        Boom.sprites.append(self)
    def blit(self):
        window.blit(self.surface, self.rect)


# инициализация, создание объектов
clock = pygame.time.Clock()
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(name)
pygame.display.set_icon(pygame.image.load(resource_path(r"images\tank1.png")))
player1 = Player(WIDTH * 0.1, HEIGHT * 0.8, window,  r'images\tank1.png', (pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_SPACE))
player2 = Player(WIDTH * 0.8, HEIGHT * 0.1, window, r'images\tank2.png', (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_p))
pygame.display.flip()


# главный цикл
while player1.health > 0 and player2.health > 0:
    # обновление экрана
    pygame.display.flip()

    window.fill(GREEN)
    # цикл обработки событий

    for i in pygame.event.get():
        events(player1, i)
        events(player2, i)

    for elem in Boom.sprites:
        elem.blit()
    player1.update_pos()
    player2.update_pos()

    for player in Player.players:
        for bul in player.bullets:
            bul.fly()
    player2.output()
    player1.output()
    # задержка
    clock.tick(FPS)

if player1.health <= 0:
    print("игрок 2 победил!")
else:
    print("игрок 1 победил!")
