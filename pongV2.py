
# Import the pygame module
import pygame

# Import random for random numbers
import random
import math
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_w,
    K_s,
    KEYDOWN,
    QUIT,
)

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
        self.height = 75
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((255, 255, 255))

        if num == 0:
            self.rect = self.surf.get_rect(
                center = (25, random.randint(0, SCREEN_HEIGHT))
            )
        elif num == 1:
            self.rect = self.surf.get_rect(
                center = (SCREEN_WIDTH-25, random.randint(0, SCREEN_HEIGHT))
            )
        self.x = self.rect.x
        self.y = self.rect.y
        #self.rect = self.surf.get_rect()
    # Move the sprite based on keypresses
    def update(self, pressed_keys):

        if self.num == 1:
            if pressed_keys[K_UP]:
                #self.rect.move_ip(0, -2)
                self.rect.y -= 1
            if pressed_keys[K_DOWN]:
                #self.rect.move_ip(0, 2)
                self.rect.y += 1
        elif self.num == 0:
            if pressed_keys[K_w]:
                #self.rect.move_ip(0, -2)
                self.rect.y -= 1
            if pressed_keys[K_s]:
                #self.rect.move_ip(0, 2)
                self.rect.y += 1

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the Ball object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'Ball'
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.height = 10
        self.width = 10
        self.surf = pygame.Surface((self.height, self.width))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        )
        self.direction = 45
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT/2
        self.speed = .5
        #self.count=0
        #self.max_count=5

    def reset(self, speed=.5):
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT/2
        self.speed = speed

        self.direction = random.choice([-45, 45, 135, -135, 225, -225])

        #have ball go in other direction
        if random.randint(0, 1) == 0:
            self.direction += 180
    def bounce(self, diff=0):
        """ Bounce off horizontal surface
        """

        self.direction = (180-self.direction)%360
        self.direction -= diff

            #self.speed *= 1.1
    # Move the sprite based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        dir_rad = math.radians(self.direction)
        self.x += self.speed * math.sin(dir_rad)
        self.y += self.speed * math.cos(dir_rad)

        if self.x<0:
            self.reset()
        if self.x>1000:
            self.reset()

        #move ball to current x and y values
        self.rect.x = self.x
        self.rect.y = self.y
        #self.rect.move_ip(-self.speed, 0)

        #pygame.time.wait(.01)
        # if self.count < self.max_count:
        #     self.count+=1
        # else:
        #     self.rect.move_ip(-self.speed, 0)
        #     self.count=0

        if self.rect.right < 0:
            self.kill()


# Initialize pygame
pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new Ball.
# ADDBall = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDBall, 250)

# Create our 'player'
player0 = Player(0)
player1 = Player(1)
ball=Ball()

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

        # Should we add a new Ball?
        # elif event.type == ADDBall:
        #     # Create the new Ball, and add it to our sprite groups
        #     new_Ball = Ball()
        #     balls.add(new_Ball)
        #     all_sprites.add(new_Ball)

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player0.update(pressed_keys)
    player1.update(pressed_keys)

    # Update the position of our balls
    if ball.y < 0 or ball.y > SCREEN_HEIGHT:
        ball.bounce()

    ball.update()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    #Draw all our sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any balls have collided with either player
    if pygame.sprite.collide_rect(ball, player0):
        diff = (player0.rect.y + player0.width/2) - (ball.rect.y + ball.width/2)

        ball.x = 40
        ball.bounce(diff)

    if pygame.sprite.collide_rect(ball, player1):
        diff = (player1.rect.y + player1.width/2) - (ball.rect.y + ball.width/2)

        ball.x = SCREEN_WIDTH-40
        ball.bounce(diff)
        #ball.speed=-ball.speed
    # Flip everything to the display
    pygame.display.flip()
pygame.quit()
