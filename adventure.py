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
        """Initialize a Person

        Init function creates a person object.

        args:
            x=person's starting x position
            y=person's starting y position
        """
        super(Person, self).__init__()
        self.surf = pygame.image.load("images/Person.png").convert()
        self.rect = self.surf.get_rect(center = (x,y))
        self.x=self.rect.x
        self.y=self.rect.y
        self.vx=0
        self.vy=0
        self.ax=0
        self.ay=0
        self.on_platform = False
        self.has_bike=False

    def jump(self):
        """Makes person jump

        Makes person jump by checking if a person in on a surface
        and then changing the y velocity
        """
        if self.is_touching_ground()==True: #or touching platform
            self.vy=-1.5

    def walk(self,direction):
        """
        Makes person walk by changing x position
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
        Changes acceleration of the Person based on if person is touching the gorund or not
        """
        if self.is_touching_ground()==True:
            self.ay=0
        else:
            self.ay=.005

    def keep_on_map(self):
        """
        Ensures that the person stays in the map
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

    def is_on_platform(self,platform):
        """
        Checks if Person is on platform and if so stops the person from falling
        """
        if self.rect.bottom == platform.rect.top and self.rect.right<=platform.rect.right and self.rect.left>=platform.rect.left:
            self.vy=0
            self.on_platform=True

    def collides_with_bike(self,bike):
        """
        Checks if Person is touching bike and if so changes the person's aperance

        args:
            bike=bike object to check if the person has collided with

        """
        if self.rect.colliderect(bike.rect):
            self.surf = pygame.image.load("images/Person_on_Bike.png").convert()
            self.rect = self.surf.get_rect(center = (self.x,self.y))
            bike.surf.fill((0, 0, 0))
            self.has_bike=True

    def update(self, pressed_keys):
        """Updates the postion of the person

        Updates the position of the person based on what keys were pressed_keys
        """
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
        self.on_platform=False

    def draw(self,map):
        """Draws person on screen

        Draws person on screen by calculating screen position based on map position.
        """
        r=Rect(self.rect.left, self.rect.top-map.screen_top, self.rect.width, self.rect.height)
        map.screen.blit(self.surf, r)


class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y):
        """Initialize a Platform

        Init function creates a platform object.

        args:
            x=platform's starting x position
            y=platform's starting y position
        """
        super(Platform, self).__init__()
        self.width = 100
        self.height = 25
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center = (x,y))


class Map():
    def __init__(self,platforms,bike):
        """Initialize a Map

        Init function creates a map object.

        args:
            platform=pygame group of platforms in map
            bike=a bike object
        """
        self.width=MAP_WIDTH
        self.height=MAP_HEIGHT
        self.platforms=platforms
        self.screen_top=MAP_HEIGHT-SCREEN_HEIGHT
        self.screen_left=0
        self.screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bike=bike

    def draw(self):
        """Draws map on screen

        Draws map on screen by calculating screen position of platforms and bike
        based on their map position.
        """
        for platform in self.platforms:
            r = Rect(platform.rect.left, platform.rect.top-self.screen_top, platform.rect.width, platform.rect.height)
            screen.blit(platform.surf, r)

        r = Rect(self.bike.rect.left, self.bike.rect.top-self.screen_top, self.bike.rect.width, self.bike.rect.height)
        screen.blit(self.bike.surf, r)


class Bike(pygame.sprite.Sprite):
    def __init__(self,platform):
        """Initialize a Bike

        Init function creates a bike object.

        args:
            platform=platform object that bike should be on
        """
        super(Bike, self).__init__()
        self.surf = pygame.image.load("images/Bike.png").convert()
        self.rect = self.surf.get_rect(center = (platform.rect.left+platform.rect.width/2,platform.rect.top-50))


# if __name__ == '__main__':

# Initialize pygame
pygame.init()
print("running")
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT

platform_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
person= Person(25,MAP_HEIGHT-50)
all_sprites.add(person)

#makes platforms and puts them into a group
x=1
direction=1
for y in range(9):
    platform=Platform(x*MAP_WIDTH/4,MAP_HEIGHT-150*(y+1))
    platform_group.add(platform)
    all_sprites.add(platform)
    x+=direction
    if x==3 or x==1:
        direction=-direction

#fins the height of the highest platform
max_platform_height=0
for platform in platform_group:
    if platform.rect.top>max_platform_height:
        max_platform=platform

bike=Bike(max_platform)
all_sprites.add(bike)

map=Map(platform_group,bike)

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

    person.collides_with_bike(bike)

    # Fill the screen with black
    screen.fill((0, 0, 0))
    #draws the map and the person
    map.draw()
    person.draw(map)


    #Changes screen top based on person's position
    map.screen_top=min(MAP_HEIGHT-SCREEN_HEIGHT,person.rect.bottom-SCREEN_HEIGHT/2)


    # for entity in all_sprites:
    #     screen.blit(entity.surf, entity.rect)

    time.sleep(.001)
    pygame.display.update()
    
    if person.has_bike==True:
        running = False
