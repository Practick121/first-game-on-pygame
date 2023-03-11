import pygame
from random import randint
pygame.init()

HEIGHT = 600
WIDTH = 1200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
class Rocket:
     rocket_width = 20
     rocket_height = 50
     def __init__(self, surf, color):
         self.surf = surf
         self.color = color
         self.x = self.surf.get_width() // 2 - Rocket.rocket_width // 2
         self.y = self.surf.get_height()
     def output(self, b, rocket):
         pygame.draw.rect(self.surf, self.color, (self.x, self.y, Rocket.rocket_width, Rocket.rocket_height))
         if b:
             rocket.fly()
     def fly(self):
         self.y -= 3
         if self.y < -Rocket.rocket_height:
             self.y = self.surf.get_height()
window = pygame.display.set_mode((WIDTH, HEIGHT))
rect1 = pygame.Rect(0, 0, WIDTH / 2, HEIGHT)
rect2 = pygame.Rect(WIDTH / 2, 0, WIDTH / 2, HEIGHT)
surf1 = pygame.Surface((rect1.width, rect1.height))
surf1.fill(WHITE)
surf2 = pygame.Surface((rect2.width, rect2.height))
surf2.fill(BLACK)
window.blit(surf1, rect1)
window.blit(surf2, rect2)
rocket1 = Rocket(surf1, BLACK)
rocket2 = Rocket(surf2, WHITE)
activeleft = True
activeright = True
pygame.mouse.set_visible(False)
mouse = pygame.Surface((10, 10))
while 1:
    pygame.display.flip()
    surf1.fill(WHITE)
    surf2.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect1.collidepoint(event.pos):
                if activeleft:
                    activeleft = False
                else:
                    activeleft = True
            elif rect2.collidepoint(event.pos):
                if activeright:
                    activeright = False
                else:
                    activeright = True
    if activeright:
        rocket2.output(True, rocket2)
    else:
        rocket2.output(False, rocket2)
    window.blit(surf2, rect2)
    if activeleft:
        rocket1.output(True, rocket1)
    else:
        rocket1.output(False, rocket1)
    window.blit(surf1, rect1)
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        mouse.fill((169, 169, 169))
        window.blit(mouse, (pos[0] - 5, pos[1] - 5))


    pygame.time.delay(30)
