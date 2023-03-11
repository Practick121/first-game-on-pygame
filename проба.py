from pygame import *
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
WIDTH = 1000
HEIGHT = 700
FPS = 60
window = display.set_mode((WIDTH, HEIGHT))
display.update()
cloc = time.Clock()
r = 10
x = 150
y = 150
x1 = 0
y1 = 0
motion = set()
sprites = []
ymax = 0
display.set_caption("МЕГАИГРА")
mouse.set_visible(False)
while 1:
    display.update()
    window.fill(PINK)
    for o in event.get():
        if o.type == QUIT:
            exit()
        elif o.type == KEYDOWN:
            if o.key == K_d:
                motion.add("right")
            elif o.key == K_a and x > 0:
                motion.add('left')
            elif o.key == K_w and y > 0:
                motion.add('up')
            elif o.key == K_s and y < HEIGHT:
               motion.add('down')
        elif o.type == KEYUP:
            if o.key == K_s and 'down' in motion:
                motion.remove('down')
            if o.key == K_w and 'up' in motion:
                motion.remove('up')
            if o.key == K_a and 'left' in motion:
                motion.remove('left')
            if o.key == K_d and 'right' in motion:
                motion.remove('right')
        elif o.type == MOUSEBUTTONDOWN and not ymax:
            ymax = o.pos[1]
            x1 = o.pos[0]
            y1 = 0
    draw.circle(window, GREEN, (x, y), r)
    if mouse.get_focused():
        pos = mouse.get_pos()
        draw.rect(window, (192, 192, 192), (pos[0] - 5, pos[1] - 5, 10, 10))
    for i in sprites:
        if i[4] == 'c':
            draw.circle(window, i[1], (i[2], i[3]), i[5])
        elif i[4] == 'r':
            draw.rect(window, i[1], (i[2] - i[5] // 2, i[3] - i[5] // 2, i[5], i[5]))
    if ymax:
        draw.circle(window, BLACK, (x1, y1), 5)
    if 'left' in motion:
        x -= 200 / FPS
    if 'right' in motion and x < WIDTH:
        x += 200 / FPS
    if 'up' in motion:
        y -= 200 / FPS
    if 'down' in motion:
        y += 200 / FPS
    if y1 < ymax:
        y1 += 300 / FPS
    else:
        ymax = 0
        sprites.append((window, YELLOW, x1, y1, 'r', 20))
    cloc.tick(FPS)


