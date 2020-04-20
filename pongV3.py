"""
SoftDes Spring 2020
Final Project: Pong

@authors: Sam Coleman and Hazel Smith
"""

import pygame
from pygame.locals import *
import random
import math
import time

# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Define the Player object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self, num):
        """
        Num: 0 for left player, 1 for right player
        """
        super(Player, self).__init__()
        self.num = num
        self.width = 25
        self.height = 100
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))

        if num == 0:
            self.rect = self.surf.get_rect(
                center = (50, SCREEN_HEIGHT/2)
            )
        elif num == 1:
            self.rect = self.surf.get_rect(
                center = (SCREEN_WIDTH-50, SCREEN_HEIGHT/2)
            )
        self.x = self.rect.x
        self.y = self.rect.y
        self.score = 0
    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        """Updates the postion of the player"""
        if self.num == 1:
            if pressed_keys[K_UP]:
                self.rect.y -= 1
            if pressed_keys[K_DOWN]:
                self.rect.y += 1
        elif self.num == 0:
            if pressed_keys[K_w]:
                self.rect.y -= 1
            if pressed_keys[K_s]:
                self.rect.y += 1

        # Keep player on the screen
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def hit_paddle(self,ball):
        if pygame.sprite.collide_rect(ball, self):
            diff = ((self.rect.y + self.height/2) - (ball.rect.y + ball.height/2))*20/(self.height/2)
            if self.num==0:
                ball.bounce(diff)
            if self.num==1:
                ball.bounce(-diff)

# Define the Ball object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'Ball'
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.height = 25
        self.width = 25
        self.surf = pygame.Surface((self.height, self.width))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        )
        self.direction = random.choice([45, 135, 225, 315])
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT/2
        self.speed = .75

    def reset(self):
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT/2

        self.direction = random.choice([45, 135, 225, 315])

    def bounce(self, diff=0):
        """ Bounce off a paddle
        """

        self.direction = 360-self.direction
        self.direction -= diff
        self.speed *= 1.0001 #*very* slowly get faster

    def hit_wall(self):
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.direction = (180-self.direction)%360

    def update(self):
        dir_rad = math.radians(self.direction)
        self.x += self.speed * math.sin(dir_rad)
        self.y += self.speed * math.cos(dir_rad)

        if self.x<0:
            self.reset()
            player1.score += 1
        if self.x>1000:
            self.reset()
            player0.score += 1
        scoreboard.update_score(player0, player1)
        #move ball to current x and y values
        self.rect.x = self.x
        self.rect.y = self.y

class Scoreboard():
    def __init__(self, font):
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.score0_surface = font.render('0', False, self.color)
        self.score1_surface = font.render('0', False, self.color)
        self.font = font
    def update_score(self, player0, player1):
        self.score0_surface = self.font.render(str(player0.score), False, self.color)
        self.score1_surface = self.font.render(str(player1.score), False, self.color)


if __name__ == '__main__':
    # Initialize pygame
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('din', 80)
    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pong')
    # Create a custom event for adding a new Ball.
    # ADDBall = pygame.USEREVENT + 1
    # pygame.time.set_timer(ADDBall, 250)

    # Create our 'players'
    player0 = Player(0)
    player1 = Player(1)
    ball=Ball()
    scoreboard = Scoreboard(font)
    # Create groups to hold Ball sprites, and every sprite
    # - balls is used for collision detection and position updates
    # - all_sprites is used for rendering
    balls = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    all_sprites.add(player0)
    all_sprites.add(player1)
    all_sprites.add(ball)
    players.add(player0)
    players.add(player1)
    balls.add(ball)

    clock = pygame.time.Clock()
    # Variable to keep our main loop running
    running = True

    # Our main loop
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

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        player0.update(pressed_keys)
        player1.update(pressed_keys)

        # Check if ball have collided with either player
        for player in players:
            player.hit_paddle(ball)

        # Check if any balls have collided with either horzontal wall
        ball.hit_wall()

        # Update the position of our balls
        ball.update()

        # Fill the screen with black
        screen.fill((0, 0, 0))

        #Draw all our sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        screen.blit(scoreboard.score0_surface, (SCREEN_WIDTH/4, 25))
        screen.blit(scoreboard.score1_surface, (SCREEN_WIDTH - SCREEN_WIDTH/4, 25))
        # Flip everything to the display
        pygame.display.flip()
