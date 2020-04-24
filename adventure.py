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
import numpy as np

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

class Person(pygame.sprite.Sprite):
    def __init__(self):
        """
        """
        super(Person, self).__init__()
        self.surf = pygame.image.load("standing.png").convert()
        self.rect = self.surf.get_rect(center = (25,SCREEN_HEIGHT-50))
        self.x=self.rect.x
        self.y=self.rect.y
        self.vx=0
        self.vy=0
        self.ax=0
        self.ay=0

    def jump(self):
        """
        Makes person jump
        """
        if self.is_touching_ground()==True: #or touching platform
            self.vy=-1.5

    def walk(self,direction):
        """
        Makes person walk
        """
        self.vx=direction/2

    def is_touching_ground(self):
        """
        Checks if person is standing or in free fall
        """
        if self.rect.bottom==SCREEN_HEIGHT:
            return True
        else:
            return False

    def accelerate(self):
        """
        Changes acceleration of the Person
        """
        if self.is_touching_ground()==False:
            self.ay=.005
        else:
            self.ay=0

        if self.vx!=0:
            self.ax=1*-np.sign(self.vx)
        else:
            self.ax=0


    def keep_on_screen(self):
        """
        Ensures that the person stays on screen
        """
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

    def update(self, pressed_keys):
        """Updates the postion of the player"""
        if pressed_keys[K_UP]:
            self.jump()
        if pressed_keys[K_RIGHT]:
            self.walk(1)
        if pressed_keys[K_LEFT]:
            self.walk(-1)


        self.x+=self.vx
        self.y+=self.vy
        self.vx+=self.ax
        self.vy+=self.ay

        self.accelerate()

        #move ball to current x and y values
        self.rect.x = self.x
        self.rect.y = self.y

        self.keep_on_screen()



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
