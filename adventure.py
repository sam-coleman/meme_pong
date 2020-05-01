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

MAP_HEIGHT = 2400
MAP_WIDTH = 1000

SCREEN_WIDTH = MAP_WIDTH
SCREEN_HEIGHT = 600


class Person(pygame.sprite.Sprite):
    def __init__(self,x,y):
        """
        """
        super(Person, self).__init__()
        self.surf = pygame.image.load("images/standing.png").convert()
        self.rect = self.surf.get_rect(center = (x,y))
        self.x=self.rect.x
        self.y=self.rect.y
        self.vx=0
        self.vy=0
        self.ax=0
        self.ay=0
        self.on_platform = False

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
        self.x+=direction

    def is_touching_ground(self):
        """
        Checks if person is standing or in free fall
        """
        if self.rect.bottom==MAP_HEIGHT:
            return True
        elif self.on_platform == True:
            return True
        else:
            return False

    def accelerate(self):
        """
        Changes acceleration of the Person
        """
        if self.is_touching_ground()==True:
            self.ay=0
        else:
            self.ay=.005

    def keep_on_map(self):
        """
        Ensures that the person stays on screen
        """
        # if self.rect.top <= 0:
        #     self.rect.top = 0

        if self.rect.bottom >= MAP_HEIGHT:#stops person faling through floor
            self.vy=0
            self.rect.bottom=MAP_HEIGHT

        if self.rect.left <= 0:
            self.rect.left = 0

        elif self.rect.right >= MAP_WIDTH:
            self.rect.right = MAP_WIDTH

    def is_on_platform(self,platform,):
        """
        Checks if Person is on platform
        """
        if self.rect.bottom == platform.rect.top and self.rect.right<=platform.rect.right and self.rect.left>=platform.rect.left:
            self.vy=0
            self.on_platform=True

    def update(self, pressed_keys):
        """Updates the postion of the player"""
        if pressed_keys[K_UP]:
            self.jump()
        if pressed_keys[K_RIGHT]:
            self.walk(1)
        if pressed_keys[K_LEFT]:
            self.walk(-1)

        self.vy+=self.ay
        self.y+=self.vy
        self.accelerate()

        #move ball to current x and y values
        self.rect.x = self.x
        self.rect.y = self.y

        #move ball to current x and y values
        self.rect.x = self.x
        self.rect.y = self.y

        self.keep_on_map()
        self.on_platform=False #reset on_platform


class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Platform, self).__init__()
        self.width = 100
        self.height = 25
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = (x,y))


class Map():
    def __init__(self,platforms):
        self.width=MAP_WIDTH
        self.height=MAP_HEIGHT
        self.platforms=platforms
        self.screen_top=MAP_HEIGHT-SCREEN_HEIGHT
        self.screen_left=0
        self.screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self):
        for platform in self.platforms:
            r = Rect(platform.rect.left, platform.rect.top-self.screen_top, platform.rect.width, platform.rect.height)
            screen.blit(platform.surf, r)

if __name__ == '__main__':

    # Initialize pygame
    pygame.init()
    print("running")
    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    person= Person(25,MAP_HEIGHT-50)

    platform_group = pygame.sprite.Group()

    i=1
    j=1
    for x in range(9):
        platform=Platform(i*MAP_WIDTH/4,MAP_HEIGHT-150*(x+1))
        platform_group.add(platform)
        i+=j
        if i==3 or i==1:
            j=-j

    map=Map(platform_group)

    running = True
    while running:
        #screen.bottom=person.rect.bottom
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

        for platform in map.platforms:
            person.is_on_platform(platform)


        # Fill the screen with black
        screen.fill((0, 0, 0))

        #draws the map and the person
        map.draw()
        r=Rect(person.rect.left, person.rect.top-map.screen_top, person.rect.width, person.rect.height)
        map.screen.blit(person.surf, r)


        #Changes screen top based on person's position
        # if person.on_platform==True:
        #     map.screen_top=min(MAP_HEIGHT-SCREEN_HEIGHT,person.rect.bottom-SCREEN_HEIGHT/2)
        map.screen_top=min(MAP_HEIGHT-SCREEN_HEIGHT,person.rect.bottom-SCREEN_HEIGHT/2)


        # for entity in all_sprites:
        #     screen.blit(entity.surf, entity.rect)

        time.sleep(.001)
        pygame.display.update()
