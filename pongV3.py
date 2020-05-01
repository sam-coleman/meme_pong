"""
SoftDes Spring 2020
Final Project: Pong

@authors: Sam Coleman and Hazel Smith
"""

import pygame
from pygame.locals import *
import random
import math

# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Define the Player object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(pygame.sprite.Sprite):
    """ Player class represents the left and right players and inherits the pygame sprite class
    """
    def __init__(self, num):
        """ Initialize a player paddle object

        Init function creates a paddle for each player and places it on the correct side of the screen
        based on the num argument. Initializes all attributes of the Player object.

        Args:
            num (int): 0 for player on left, 1 for player on right
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

        #when game starts, the minigame has not been played yet
        self.played_minigame = False
    def allen_design(self): #switch paddles to allen downey design
        """Change design of paddles to Allen Downey theme
        """

        #change paddles to Steve and Amon
        player0.surf = pygame.image.load("images/steve.png").convert()
        player1.surf = pygame.image.load("images/amon.png").convert()

        #put player on right back in the correct position on screen
        player1.rect = self.surf.get_rect(
            center = (SCREEN_WIDTH-50, SCREEN_HEIGHT/2)
        )

    def update(self, pressed_keys):
        """Updates the postion of the players

        This function updates the position of the player on the screen by incramenting
        position by 1 pixel when a key is pressed. Up and down arrows move right player up and down
        and right arrow moves the player to the right to access mini adventure, respectively.
        W and S move the left player up and down, respectively.

        Args:
            pressed_keys (pygame key object): which key is pressed

        """

        if self.num == 1:
            if pressed_keys[K_UP]:
                self.rect.y -= 1
            if pressed_keys[K_DOWN]:
                self.rect.y += 1
            if pressed_keys[K_RIGHT] and self.played_minigame == False:
                self.rect.x += 1
        elif self.num == 0:
            if pressed_keys[K_w]:
                self.rect.y -= 1
            if pressed_keys[K_s]:
                self.rect.y += 1

        # Keep player on the screen but allow right player (player 1) motion to right
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        elif self.num == 1 and self.rect.right == SCREEN_WIDTH: #will move player to minigame
            #NEED TO CHANGE TO STARTING THE MINI GAME, WHEN THE BIKE IS GOTTEN, THEN TRIGGER THE ALLEN_DESIGN FUNCTIONS
                #MAKE BALL SPEED 0
                #CALL RESET AFTER BIKE IS GOTTEN TO ALSO GET GAME GOING AGAIN
            self.played_minigame = True
            self.allen_design()
            ball.allen_design()

    def hit_paddle(self,ball):
        """ Determine if paddle was hit by ball, and update motion accordingly

        This function detects a collision between a player paddle and the ball, and updates
        the direction difference (diff) of the ball object accordingly. Bounce function is called
        with either a positive or negative diff depending on which player the ball collided with.

        Args:
            ball (Ball object): instance of Ball object (defined below)
        """
        
        if pygame.sprite.collide_rect(ball, self):

            #diff: calculate the difference in angle of the ball based on how off-center of the center of the
            #paddle the ball hits.
            diff = ((self.rect.y + self.height/2) - (ball.rect.y + ball.height/2))*70/(self.height/2)
            if self.num==0:
                ball.bounce(diff)
            if self.num==1:
                ball.bounce(-diff)


class Ball(pygame.sprite.Sprite):
    """ Ball class represents the ball and inherits the pygame sprite class
    """
    def __init__(self):
        """Initialize a ball object

        Init function creates a ball object and initializes all attributes of ball. Ball starts in center
        of playing window, moving at a random angle in incraments of 45deg.

        """
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
        self.speed = .5

    def allen_design(self):
        """Change design of ball to Allen Downey theme
        """
        self.surf = pygame.image.load("images/allen.jpg").convert()

    def reset(self):
        """Resets the ball to the center of the sceeen and makes it moves
        in an angle increamenting in 45deg

        """
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT/2

        self.direction = random.choice([45, 135, 225, 315])

    def bounce(self, diff):
        """Bounces ball off paddle

        Bounces ball of paddle flipping the direction 180deg and taking into account diff
        which is calculated in the hit_paddle function of the Player class.

        args:
            diff (float): difference in angle to deflect
        """

        self.direction = 360-self.direction
        self.direction -= diff
        self.speed *= 1.0001 #*very* slowly get faster

    def hit_wall(self):
        """ Bounces ball of the top and bottom edge of window

        Bounces ball and changes the direction when it hits the top or bottom walls
        (edge of window).
        """
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.direction = (180-self.direction)%360

    def update(self):
        """ Updates the movement of ball based on attribute values.

        Update takes into account all of the updated ball attributes calculated in the
        above functions and makes appropiate changes.
        """

        #change direction to radians
        dir_rad = math.radians(self.direction)

        #make the ball move at the needed angle
        self.x += self.speed * math.sin(dir_rad)
        self.y += self.speed * math.cos(dir_rad)

        #if ball goes off left screen (right player gets point) and resets ball
        if self.x<0:
            self.reset()
            player1.score += 1
            #send updated scores to scoreboard class function
            scoreboard.update_score(player0, player1)

        #if ball goes off right screen (left player gets point) and resets ball
        if self.x>1000:
            self.reset()
            player0.score += 1
            #send updated scores to scoreboard class function
            scoreboard.update_score(player0, player1)

        #move ball to current x and y values
        self.rect.x = self.x
        self.rect.y = self.y


class Scoreboard():
    """Scoreboard class displays the score of each player on the top of the screen
    """
    def __init__(self, font):
        """Initialize a Scoreboard

        Init function creates a scoreboard object and renders it on the screen.

        args:
            font (pygame font object): Font to use
        """

        #set random color between RGB 100-255 for each game for the scores
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.score0_surface = font.render('0', False, self.color)
        self.score1_surface = font.render('0', False, self.color)
        self.font = font

    def update_score(self, player0, player1):
        """ Update the scores of each player

        Updates the score of each player and is called in ball class update function.

        args:
            player0 (Player object): Player on left of screen
            player1 (Player object): Player on right of screen
        """
        self.score0_surface = self.font.render(str(player0.score), False, self.color)
        self.score1_surface = self.font.render(str(player1.score), False, self.color)


if __name__ == '__main__':

    # Initialize pygame and font
    pygame.init()
    pygame.font.init()

    #set the font to use in Scoreboard object
    font = pygame.font.SysFont('din', 80)

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pong')

    # Create the needed instances of classes
    player0 = Player(0)
    player1 = Player(1)
    ball=Ball()
    scoreboard = Scoreboard(font)

    # Create groups to sprites
    # balls is used for collision detection and position updates
    # playes is used for collision detection and position updates
    # all_sprites is used for rendering
    balls = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    all_sprites.add(player0)
    all_sprites.add(player1)
    all_sprites.add(ball)
    players.add(player0)
    players.add(player1)
    balls.add(ball)

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
