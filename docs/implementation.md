---
title: Implementation
layout: template
filename: implementation
--- 

# Implementation
###Pong Game
Our pong game contains three classes
1) Player class which is user controlled using keyboard inputs. Each instance of the Player class also has a score. A function inside this class changes the apperance of the player once the easter egg game is completed.
2) Ball class which movement is automated but affected by player's actions. A ball object has the ability to change a player's score. This class also has a function to change its appearance upon completion of the adventure game
3) Scoreboard displays the player's score
###Adventure Game
1) Person class which is also user controlled but moves in different ways from the player class and was differently named to avoid confusion 
2) Platform class is a class of object that can interact with the player
3) Map class which holds the positions of all the platforms and handles displaying them onto the screen
