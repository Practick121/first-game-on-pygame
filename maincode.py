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

def opred():
    global gameover
    global VOLUME
    global objects
    global started
    gameover = 0
    VOLUME = 1
    objects = []
    started = False

def restart():
    global started
    started = False

def strat():
    global started
    started = True

def eexit():
    sys.exit()

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
        eexit()

    elif i.type == pygame.KEYDOWN:
        if i.key == player.keys["right"]:
            player.motion.append("right")
        elif i.key == player.keys["left"]:
            player.motion.append("left")
        elif i.key == player.keys["up"]:
            player.motion.append('up')
        elif i.key == player.keys['down']:
            player.motion.append("down")
        elif i.key == player.keys["shoot"]:
            player.fire()
    elif i.type == pygame.KEYUP:
        if i.key == player.keys["up"]:
            player.motion.remove("up")
        if i.key == player.keys["down"]:
            player.motion.remove("down")

def vector(angle, s, otkl=1):
    if angle % 90 == 45:
        otvet = [s / (2 ** 0.5), s / (2 ** 0.5)]
        otvet[0] = int(otvet[0] * (1 * (angle > 180 and angle < 360) + -otkl * (angle < 180 and angle > 0)) * 1000) / 1000
        otvet[1] = int(otvet[1] * (1 * (angle > 90 and angle < 270) + -otkl * (angle < 90 or angle > 270)) * 1000) / 1000
    else:
        otvet = [s] * 2
        otvet[0] = int(otvet[0] * (1 * (angle > 180 and angle < 360) + -1 * (angle < 180 and angle > 0)) * 1000) / 1000
        otvet[1] = int(otvet[1] * (1 * (angle > 90 and angle < 270) + -1 * (angle < 90 or angle > 270)) * 1000) / 1000
    return otvet

def push_off():
    pass

class Player(pygame.sprite.Sprite):
    players = []
    # инициализация
    def __init__(self, x, y, screen, part_path, rechar, yron, keys=(), *args):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.original_image_part1 = pygame.image.load(resource_path(r'images/tank' + part_path + "_part1.png")).convert_alpha()
        self.original_image_part1 = pygame.transform.scale(self.original_image_part1, (self.original_image_part1.get_width() / 2, \
                                                                                       self.original_image_part1.get_height() / 2))
        self.original_image_part2 = pygame.image.load(resource_path(r'images/tank' + part_path + "_part2.png")).convert_alpha()
        self.original_image_part2 = pygame.transform.scale(self.original_image_part2,
                                                           (self.original_image_part2.get_width() / 2.2, \
                                                            self.original_image_part2.get_height() / 2.2))
        self.image_part1 = self.original_image_part1
        self.image_part2 = self.original_image_part2

        self.rect_part1 = self.image_part1.get_rect(center=(x, y))
        self.rect_part2 = self.image_part2.get_rect(center=(x, y))
        self.direction_part1 = 0 # угол игрока
        self.direction_part2 = 0
        self.motion = []  # направления, в которых движется игрок
        self.keys = {"right": keys[2], "left": keys[3], "up": keys[0], "down": keys[1],\
                     "shoot": keys[4]} # словарь констант кнопок, на которые будет реагировать спрайт
        self.bullets = []
        Player.players.append(self) #добавление спрайта в список
        self.health = Health()
        self.past_x = self.rect_part1.centerx
        self.past_y = self.rect_part1.centery
        self.time_rechar = rechar * 1000
        self.last_gen = -self.time_rechar
        self.yron = yron

    def enemy(self):
        # метод, возвращающий противника этого танка
        enemy = Player.players.copy()
        enemy.remove(self)
        return enemy[0]

    def output(self):
        # отрисовка танка
        self.image_part1 = pygame.transform.rotate(self.original_image_part1, self.direction_part1)
        self.rect_part1 = self.image_part1.get_rect(center=(self.rect_part1.centerx, self.rect_part1.centery))
        self.screen.blit(self.image_part1, self.rect_part1)

        v = vector(self.direction_part2, 10)
        self.image_part2 = pygame.transform.rotate(self.original_image_part2, self.direction_part2)
        self.rect_part2 = self.image_part2.get_rect(center=(self.rect_part2.centerx, self.rect_part2.centery))
        self.screen.blit(self.image_part2, (self.rect_part2.x + v[0], self.rect_part2.y + v[1]))

        self.health.output(self.rect_part1.centerx - 30, self.rect_part1.bottom + 10)

    def update_pos(self): # передвижение танка
        if len(self.motion):
            if self.motion[-1] == 'left':
                self.direction_part2 += 45
                if self.direction_part2 % 90 == 0:
                    # если при повороте танк коснется другого, стены или препятствия
                    #if not\
                         #   pygame.transform.rotate(self.image_part1, self.direction_part2).get_rect(center=(self.rect_part1.centerx, self.rect_part1.centery)).colliderect(self.enemy().rect_part1)\
                        #    or pygame.transform.rotate(self.image_part1, self.direction_part2).get_rect(center=(self.rect_part1.centerx, self.rect_part1.centery)).collidelist([i.rect for i in Block.sprites]) == -1:
                    self.direction_part1 = self.direction_part2
                  #  else:
                     #   self.direction_part2 -= 45
                self.motion.remove("left")
            elif self.motion[-1] == 'right':
                self.direction_part2 -= 45
                if self.direction_part2 % 90 == 0:
                    # если при повороте танк коснется другого, стены или препятствия
                    #if not\
                           # pygame.transform.rotate(self.image_part1, self.direction_part2).get_rect(center=(self.rect_part1.centerx, self.rect_part1.centery)).colliderect(self.enemy().rect_part1)\
                          #  and pygame.transform.rotate(self.image_part1, self.direction_part2).get_rect(center=(self.rect_part1.centerx, self.rect_part1.centery)).collidelist([i.rect for i in Block.sprites]) == -1:
                    self.direction_part1 = self.direction_part2
                   # else:
                     #   self.direction_part2 += 45
                self.motion.remove("right")
            elif self.motion[-1] == 'up' or self.motion[-1] == "down":
                if self.direction_part1 % 90 == 0:
                    v = vector(self.direction_part1, SPEED)
                    self.past_x = self.rect_part1.centerx
                    self.past_y = self.rect_part1.centery
                    if self.motion[-1] == 'up':
                        self.rect_part1.centerx += v[0]
                        self.rect_part1.centery += v[1]
                        self.rect_part2.centerx += v[0]
                        self.rect_part2.centery += v[1]
                    else:
                        self.rect_part1.centerx -= v[0] * 0.5
                        self.rect_part1.centery -= v[1] * 0.5
                        self.rect_part2.centerx -= v[0] * 0.5
                        self.rect_part2.centery -= v[1] * 0.5
            if self.direction_part1 >= 360:
                self.direction_part1 -= 360
            elif self.direction_part1 < 0:
                self.direction_part1 += 360
            if self.direction_part2 >= 360:
                self.direction_part2 -= 360
            elif self.direction_part2 < 0:
                self.direction_part2 += 360
        if self.rect_part1.colliderect(self.enemy().rect_part1) or self.rect_part1.x + self.rect_part1.width > WIDTH or\
                self.rect_part1.x < 0 or self.rect_part1.y + self.rect_part1.height > HEIGHT or\
                self.rect_part1.y < 0 or self.rect_part1.collidelistall([i.rect for i in Constr.sprites]):  # если танки столкнулись или танк коснулся края или танк коснулся стены
            self.rect_part1.centerx = self.past_x
            self.rect_part1.centery = self.past_y
            v = [0, 0]
            if self.direction_part2 % 90 == 0:
                v = vector(self.direction_part2, 1)
            self.rect_part2.centerx = self.past_x + v[0]
            self.rect_part2.centery = self.past_y + v[1]


    def fire(self):
        if pygame.time.get_ticks() > self.last_gen + self.time_rechar:
            bullet = Bullet(self)
            self.last_gen = pygame.time.get_ticks()

class Bullet:
    def __init__(self, player): # определение пули
        self.belong = player
        self.original_surf = pygame.Surface((3, 6), pygame.SRCALPHA)
        self.original_surf.fill((255, 0, 0))
        self.direction = self.belong.direction_part2
        self.surf = pygame.transform.rotate(self.original_surf, self.direction)
        self.belong.bullets.append(self)
        self.rect = self.surf.get_rect()
        self.enemy = Player.players.copy()
        self.enemy.remove(self.belong)
        self.enemy = self.enemy[0] # определение противника для этой пули
        v = vector(self.direction, 50)
        self.rect.centerx = player.rect_part1.centerx + v[0]
        self.rect.centery = player.rect_part1.centery + v[1]

    def fly(self): # перемещение пули по экрану
        global gameover
        global win
        v = vector(self.direction, SPEEDBUL, 0.8) # движение пули взависимости от направления
        self.rect.x += v[0]
        self.rect.y += v[1]
        window.blit(self.surf, self.rect)
        # пуля удаляется если коснулась края или противника
        if self.rect.centerx > WIDTH or self.rect.centerx < 0 or self.rect.centery > HEIGHT or self.rect.centery < 0\
                or self.rect.collidelistall([i.rect for i in Constr.sprites]):
            self.belong.bullets.remove(self)
            del self

        elif self.enemy.rect_part1.colliderect(self.rect):
            print("попал!")
            self.enemy.health.number -= self.belong.yron
            if player1.health.number <= 0 or player2.health.number <= 0 and not gameover:
                gameover = pygame.time.get_ticks()
                win = 1 * (player1.health.number > 0) + 0
            bam = Boom(self.rect.centerx, self.rect.centery)
            self.belong.bullets.remove(self)
            del self


class Health:
    sprites = []
    SIZE = [60, 15]
    def __init__(self):
        self.surf = pygame.Surface(Health.SIZE, pygame.SRCALPHA)
        Health.sprites.append(self)
        self.number = 100


    def output(self, x, y):
        self.surf.fill(BLACK)
        pygame.draw.rect(self.surf, WHITE, (2, 2, Health.SIZE[0] - 4, Health.SIZE[1] - 4))
        pygame.draw.rect(self.surf, (192, 57, 43), (2, 2, (Health.SIZE[0] - 4) * self.number / 100, Health.SIZE[1] - 4))
        window.blit(self.surf, (x, y))

class Boom:
    sprites = []
    def __init__(self, x, y):
        self.surface = pygame.Surface((15, 15))
        self.subsurf = pygame.Surface((7, 7))
        self.subsurf.fill((255, 0, 0))
        self.rect = self.surface.get_rect(center=(x, y))
        self.surface.fill((255, 255, 0))
        self.surface.blit(self.subsurf, (4, 4))
        Boom.sprites.append(self)
    def blit(self):
        window.blit(self.surface, self.rect)


class Block: # конструктор одного блока стены
    sprites = []

    def __init__(self, x, y, width, height):
        self.surf = pygame.transform.scale(pygame.image.load(resource_path(r'images/wall.png')).convert(), (width, height))
        self.rect = self.surf.get_rect(center=(x, y))
        Block.sprites.append(self)

    def output(self):
        window.blit(self.surf, self.rect)
        pygame.display.update(self.rect)

class Constr: # конструктор стен
    sprites = []

    def __init__(self, x, y, width, height, width_one, height_one, zalit=True):
        self.wall = []
        self.number_x = width // width_one
        self.number_y = height // height_one
        print(f"строка из {self.number_x}, столбец из {self.number_y}")
        self.spisok = []
        self.rect = pygame.Rect(x, y, 0, 0)
        self.width_one = width_one
        self.height_one = height_one
        if zalit:
            for i in range(self.number_x):
                for j in range(self.number_y):
                    block = Block(x + (self.width_one) * i, y + (self.height_one) * j, self.width_one, self.height_one)
                    self.spisok.append(block)
                    self.rect.union_ip(block)
        else:
            for i in range(self.number_x):
                for j in range(self.number_y):
                    if j == 0 or j == self.number_y - 1:
                        block = Block(x + (self.width_one) * i, y + (self.height_one) * j, self.width_one, self.height_one)
                        self.spisok.append(block)
                        self.rect.union_ip(block)
                    elif i == 0 or i == self.number_x - 1:
                        block = Block(x + (self.width_one) * i, y + (self.height_one) * j, self.width_one, self.height_one)
                        self.spisok.append(block)
                        self.rect.union_ip(block)
        Constr.sprites.append(self)

    def output(self):
        for i in self.spisok:
            window.blit(i.surf, i.rect)



class Button:

    def __init__(self, width, height, x, y, color, text_s="Button", func=None): # конструктор класса, который принимает размеры и расположение левого правого угла
        # кнопки,ее текст, цвет и функция при нажатии
        global sprite_gr
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.func = func
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_s = text_s #сохранение всех переданных аргументов, а также первичное создание кнопки как поверхности
        if self.text_s[0] == '@': # отдельный случай для кнопок, хранящих не текст, а изображение
            if text_s == "@звук":
                sprite_gr = [pygame.transform.scale(i, (self.width, self.height)) for i in sprite_gr]
                self.text = sprite_gr[1 - VOLUME]
                self.fillcolors = {"normal": self.color, "hover": self.color, "pressed": self.color}
        else:
            self.text = font.render(self.text_s, True, (20, 20, 20))
            self.fillcolors = {"normal": self.color, "hover": (102, 102, 102), "pressed": (51, 51, 51)}
            # определение всех цветов кнопки при разных обстоятельствах
        self.press = False
        objects.append(self)


    def process(self, text_but=''): # метод, вызывающий функцию кнопки при соблюдении всех условий
        self.fillcolors["normal"] = self.color
        pos = pygame.mouse.get_pos()
        touch = pygame.mouse.get_pressed()[0] # True, если лкм нажата
        self.surface.fill(self.fillcolors["normal"])  # установка обычного цвета, пока кнопки не коснулись или не нажали
        if self.rect.collidepoint(pos):
            self.surface.fill(self.fillcolors["hover"])# если на кнопку навели мышь, но не нажали
            if touch:
                self.surface.fill(self.fillcolors["pressed"])
                self.press = True
            elif self.press:
                if len(self.text_s) == 1:
                    self.func(text_but) # функцияя кнопки срабатывает, если пользовтель отжал лкм на этой кнопке
                else:
                    self.func()
                self.press = False
        else:
            self.press = False
        self.surface.blit(self.text, (self.rect.width / 2 - self.text.get_rect().width / 2,\
                                      self.rect.height / 2 - self.text.get_rect().height / 2))
        window.blit(self.surface, self.rect) # отображение кнопки на экране


# инициализация, создание объектов
clock = pygame.time.Clock()
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(name)
pygame.display.set_icon(pygame.transform.rotate(pygame.image.load(resource_path(r"images/tank1.png")), 270))
back_ground_gameplay = pygame.transform.scale(pygame.image.load(resource_path(r'images/back_ground.png')).convert(), (WIDTH, HEIGHT))
back_ground_menu = pygame.transform.scale(pygame.image.load(resource_path(r'images/back_ground_menu.png')).convert(), (WIDTH, HEIGHT))
back_ground_final = pygame.transform.scale(pygame.image.load(resource_path(r'images/final.png')), (WIDTH, HEIGHT))
font = pygame.font.Font(None, 30)
pygame.display.flip()


# главный цикл
def gameplay():
    global player1
    global player2
    Boom.sprites = []
    Bullet.Constr = []
    Health.sprites = []
    Player.players = []
    player1 = Player(WIDTH * 0.1, HEIGHT * 0.8, window,  "1", 0.5, yron=10, keys=(pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_SPACE))
    player2 = Player(WIDTH * 0.8, HEIGHT * 0.1, window, "2", 0.5 , yron=10, keys=(pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_p))
    window.blit(pygame.transform.scale(pygame.image.load(resource_path(r'images/screen_loading.png')), (WIDTH, HEIGHT)), (0, 0))
    pygame.display.flip()
    wall2 = Constr(30, 30, 500, 200, 50, 50, False)
    wall3 = Constr(WIDTH - 480, HEIGHT - 180, 500, 200, 50, 50, False)
    while 1:

        # обновление экрана
        pygame.display.flip()
        window.blit(back_ground_gameplay, (0, 0))
        pygame.draw.rect(window, BLACK, (0, 0, WIDTH, HEIGHT), 5)



        wall2.output()
        wall3.output()

        # цикл обработки событий
        for i in pygame.event.get():
            events(player1, i)
            events(player2, i)


        for player in Player.players:
            for bul in player.bullets:
                bul.fly()


        for elem in Boom.sprites:
            elem.blit()




        player1.update_pos()
        player2.update_pos()




        player2.output()
        player1.output()
        if gameover:
            window.blit(pygame.font.Font(None, 200).render("GAME OVER", True, (255, 0, 0)), (WIDTH / 2 - 400, HEIGHT / 2 - 100))
            if pygame.time.get_ticks() > gameover + 2000:
                break
        # задержка


        clock.tick(FPS)

    final()



def mainmenu():
    exitt = Button(200, 50, WIDTH / 2 - 100, HEIGHT * 0.8, (255, 0, 155), "EXIT", eexit)
    start = Button(200, 50, WIDTH / 2 - 100, HEIGHT * 0.7, (255, 255, 155), "START", strat)
    print(started)
    while not started:

        window.blit(back_ground_menu, (0, 0))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                eexit()
        for i in objects:
            i.process()
        pygame.display.flip()
        clock.tick(FPS)

    objects.remove(start)
    objects.remove(exitt)
    gameplay()

def final():
    restartt = Button(200, 50, WIDTH / 2 - 100, HEIGHT * 0.6, (255, 100, 50), "RESTART(((", restart)
    while started:
        window.blit(back_ground_final, (0, 0))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                eexit()

        for i in objects:
            i.process()

        pygame.display.flip()
        clock.tick(FPS)
    objects.remove(restartt)
    main()




def main():
    opred()
    mainmenu()
    if win:
        print("игрок 1 победил!")

    else:
        print("игрок 2 победил!")

if __name__ == "__main__":
    main()