"""
SoftDes Spring 2020
Micro-Project 4
Pong Micro View Controller

@authors: Sam Coleman and Hazel Smith
"""

import pygame
from pygame.locals import *
import random
import math
import time

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

class Person(pygame.sprite.Sprite):
    def __init__(self):
        """
        Num: 0 for left player, 1 for right player
        """
        super(Person, self).__init__()
        self.surf = pygame.image.load("images/standing.png").convert()
        self.rect = self.surf.get_rect(center = (25,SCREEN_HEIGHT-50))
        self.vertical=0
        self.horzontal=0

    def update(self, pressed_keys):
        """Updates the postion of the player"""
        if pressed_keys[K_UP]:
            self.vertical=1
        if pressed_keys[K_DOWN]:
            self.vertical=-1
        if pressed_keys[K_RIGHT]:
            self.horzontal=1
        if pressed_keys[K_LEFT]:
            self.horzontal=-1

        if self.vertical==1:
            self.rect.y -= 2
        if self.vertical==-1:
            self.rect.y += 2
        if self.horzontal==1:
            self.rect.x += 2
        if self.horzontal==-1:
            self.rect.x -= 2

        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.y += 1
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        self.vertical=0
        self.horzontal=0


if __name__ == '__main__':

    # Initialize pygame
    pygame.init()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    person= Person()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(person)

    running = True
    while running:

        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop
            elif event.type == QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()
        person.update(pressed_keys)

        # Fill the screen with black
        screen.fill((0, 0, 0))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        pygame.display.flip()
