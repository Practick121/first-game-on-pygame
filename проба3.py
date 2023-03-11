import pygame
import sys
pygame.init()
pygame.font.init()
window = pygame.display.set_mode((500, 300))
pygame.display.set_caption('проба3')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150 ,150)
text = pygame.font.Font('fonts\micross.ttf', 20).render("хехехеехехей сейчас будет тачдаун", True, (192, 0, 100))
place = text.get_rect(center=(250, 150))
betton = pygame.Surface((100, 100))
rectb = betton.get_rect(center=(250, 50))
nakov = pygame.Surface((50, 50))
rectn = nakov.get_rect(center=(450, 300))
follow = False
xsm = 0
ysm = 0


window.fill(WHITE)
betton.fill(GRAY)
window.blit(betton, rectb)
window.blit(nakov, rectn)



pygame.display.flip()
while 1:
    window.fill(WHITE)

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        if i.type == pygame.MOUSEBUTTONDOWN and rectn.collidepoint(pygame.mouse.get_pos()):
            follow = True
            pos = pygame.mouse.get_pos()
            xsm = pos[0] - rectn.topleft[0]
            ysm = pos[1] - rectn.topleft[1]
        if i.type == pygame.MOUSEBUTTONUP:
            follow = False

    if follow:
        if pygame.mouse.get_focused():
            pos = pygame.mouse.get_pos()
            pygame.draw.rect(nakov, (110, 110, 110), (0, 0, 50, 50), 3)
            rectn.x, rectn.y = pos[0] - xsm, pos[1] - ysm

    else:
        nakov.fill(BLACK)





    if rectb.colliderect(rectn):
        post = pygame.mouse.get_pos()
        place.x, place.y = pos[0] - place.width / 2, pos[1] - place.height / 2
        window.blit(text, place)
    window.blit(betton, rectb)
    window.blit(nakov, rectn)
    if rectb.colliderect(rectn):
        post = pygame.mouse.get_pos()
        place.x, place.y = pos[0] - place.width / 2, pos[1] - place.height / 2
        window.blit(text, place)


    pygame.display.flip()




    pygame.time.delay(10)