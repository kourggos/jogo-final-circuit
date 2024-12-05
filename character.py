import pygame, time, math, random, sys
from pygame.locals import *
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.collision import *
from PPlay.keyboard import *

pressed_keys = pygame.key.get_pressed()

class Character():
    def __init__(self, imagefilename, x, y, hp, speed):
        self.image = GameImage(imagefilename)
        self.width = self.image.width
        self.height = self.image.height
        self.image.x = x
        self.image.y = y
        self.x = self.image.x
        self.y = self.image.y
        self.hp = hp
        self.speed = speed

    def draw(self):
        self.image.x = self.x
        self.image.y = self.y
        self.x = self.image.x
        self.x = self.image.x
        self.image.draw()

    def dash(self, direction):
        self.image = GameImage("dash"+direction+".png")
        self.image.x = self.x
        self.image.y = self.y
        self.x = self.image.x
        self.y = self.image.y

    def jump(self, gravity=1, jumpheight=20, yvel = 20):
        self.y -= yvel
        yvel -= gravity
        if yvel < -jumpheight:
            yvel = jumpheight
            return False, gravity, jumpheight, yvel
        return True, gravity, jumpheight, yvel
    
    def move(self, velx):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.x -= velx
            self.image.x = self.x
        if pressed_keys[K_RIGHT]:
            self.x += velx
            self.image.x = self.x
