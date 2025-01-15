import pygame
from PPlay.gameimage import *

class Platform():
    def __init__(self, arq, janela, y):
        self.janela = janela
        self.body = GameImage(arq)
        self.body.x = janela.width
        self.body.y = y

    def move(self, player, background, esq, velx=0, vely=0):
        if player.image.x >= self.janela.width*7.5/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq:
            self.body.x -= 1.15 # 0.9
        elif player.image.x >= self.janela.width*7/21 and player.image.x < self.janela.width*7.5/21  and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq:
            self.body.x -= 0.9 # 0.6
        if self.body.x + self.body.width < 0:
            return True
        return False

    def draw(self):
        self.body.draw()
