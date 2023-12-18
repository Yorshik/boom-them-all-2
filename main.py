import os
import sys
from random import randint

import pygame

SIZE = 500, 500
screen = pygame.display.set_mode(SIZE)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bomb(pygame.sprite.Sprite):
    bomb = pygame.transform.scale(load_image('bomb2.png'), [50, 50])
    boom = load_image('boom.png')

    def __init__(self, *group, size=(500, 500)):
        super().__init__(*group)
        self.image = Bomb.bomb
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = randint(0, size[0] - self.rect.w), randint(0, size[1] - self.rect.h)

    def update_image(self, ev: pygame.event.Event):
        if self.image != Bomb.boom and self.rect.x <= ev.pos[0] <= self.rect.x + self.rect.w and self.rect.y <= ev.pos[
            1] <= self.rect.y + self.rect.h:
            self.image = Bomb.boom


class MyGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update_images(self, e):
        for sprite in self.sprites():
            sprite.update_image(e)


running = True
my_group = MyGroup()
num = 20
while num:
    bomb = Bomb(size=SIZE)
    if pygame.sprite.spritecollideany(bomb, my_group):
        continue
    num -= 1
    my_group.add(bomb)
clock = pygame.time.Clock()
FPS = 60
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            my_group.update_images(event)
    my_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
