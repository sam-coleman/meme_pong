"""
SoftDes Spring 2020
Micro-Project 4
Pong Micro View Controller

@authors: Sam Coleman and Hazel Smith
"""

import pygame
from pygame.locals import *
import time
import math


class PyGameWindowView:
    def __init__(self, model, size):
        """
        Set up and create a new pygame window

        Size is represented as a tuple with a width and height"""
        self.model = model
        self.screen = pygame.display.set_mode(size)

    def draw(self):
        """ Draw the current game state to the screen """
        self.screen.fill(pygame.Color(0,0,0))
        #add code to draw paddles and ball
        #puts the new visuals on the screen
        pygame.display.update()


class PyGameKeyboardController:
    """ Handles keyboard input for moving player's paddles """
    def __init__(self,model):
        """ Initialize keyboard controller"""

        self.model = model

    def handle_event(self,event,player1,player2):
        """
        Takes J,L,A, and D keys and moves the player's paddles

        J,L are for player 1
        D,A are for player 2
        """
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_l:
            player1.amount+=1
        if event.key == pygame.K_j:
            player1.amount-=1
        if event.key == pygame.K_d:
            player2.amount+=1
        if event.key == pygame.K_a:
            player2.amount-=1


class GameModel:
    """ Encodes a model of the game state """
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]

    def update(player1,player2,ball):
        """
        Updates the postions of the player's paddles and the Ball
        player1= a Player object
        player2= a Player object
        ball= a Ball object
        """
        pass


class Player:
    def __init__(self,number):
        """
        Create a set up a new player object

        Args: number (1 or 2) represents which player it is"""

        self.number=number
        self.score=0
        self.positionx=400
        self.amount=0

        # Placement for the paddles
        if self.number==1:
            self.positiony=1150
        if self.number==2:
            self.positiony=50

    def move(self,amount):
        """
        Move the paddle for each user """
        self.positionx=self.positionx+self.amount
        return self.positionx


class Ball:
    """
    A class to reprsent the ball """
    def __init__(self):
        """
        Create and set up a new ball object """
        self.positionx = 400
        self.positiony = 600
        # direction goes from [0,360)
        self.direction = (45)

    def hit_wall(self):
        """
        Change the direction of the ball if it hits a wall"""

        #Need to implement if a collision with a wall is detected

        if self.direction < 0:
            self.direction+=360
        if self.direction >= 360:
            self.direction-=360
        return self.direction

    def hit_paddle(self):
        """
        Change the direction of the ball if it hits a paddle"""
        pass

        #Implement if collision with paddle is detected

        #Add randomness to how ball direction will change and return value

    def move(self,amount):
        """
        Move the ball by specified amount"""
        angle=self.dirction/180*math.pi
        self.postionx += amount*math.cos(angle)
        self.postiony += amount*math.sin(angle)


if __name__ == '__main__':
    pass
