import pygame
from fade import *
from PPlay.gameimage import *

class Background():
    def __init__(self, janela):
        self.janela = janela
        self.bg_list = [GameImage("scenery/background_city_day.png"), GameImage("scenery/background_city_day.png"), GameImage("scenery/background_city_night.png")]
        self.cenario = self.bg_list[0]
        self.bg_change = False
        self.bg_atual = 0

    def move(self, player):
        if player.x >= self.janela.width*7/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not self.bg_change:
            self.cenario.x -= 1.15 # 0.9
            player.move(-400)

        elif player.x == self.janela.width*7/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not self.bg_change:
            self.cenario.x -= 0.9 # 0.6
        else:
            player.move(700)
        if self.cenario.x + self.cenario.width <= self.janela.width:
            self.bg_change = True
        if self.bg_change and player.x > self.janela.width:
            Fade(self.janela).fade()
            player.x = self.janela.width / 4
            self.cenario = self.bg_list[self.bg_atual + 1]
            self.cenario.x = 0
            self.bg_atual += 1
            if self.bg_atual == len(self.bg_list) - 1:
                self.bg_atual = 0
            self.bg_change = False
        self.cenario.draw()

class Floor():
    def __init__(self, janela):
        self.janela = janela
        self.floor_list = [GameImage("scenery/floor.png"), GameImage("scenery/floor.png")]
        for sprite in self.floor_list:
            sprite.y = self.janela.height - sprite.height
        self.floor = self.floor_list[0]
        self.nextfloor = self.floor_list[1]
        self.floor_atual = 0

    def move(self, player, background):
        if player.x >= self.janela.width*7/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change:
            self.floor.x -= 1.15 # 0.9
        elif player.x == self.janela.width*7/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change:
            self.floor.x -= 0.9 # 0.6
        if self.floor.x + self.floor.width <= 0:
            self.floor, self.nextfloor = self.nextfloor, self.floor
        self.nextfloor.x = self.floor.x + self.floor.width
        self.floor.draw()
        self.nextfloor.draw()

class Ceiling():
    def __init__(self, janela):
        self.janela = janela
        self.ceiling_list = [GameImage("scenery/ceiling.png"), GameImage("scenery/ceiling.png")]
        self.ceiling = self.ceiling_list[0]
        self.nextceiling = self.ceiling_list[1]
        self.ceiling_atual = 0

    def move(self, player, background):
        if player.x >= self.janela.width*7/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change:
            self.ceiling.x -= 1.15 # 0.9
        elif player.x == self.janela.width*7/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change:
            self.ceiling.x -= 0.9 # 0.6
        if self.ceiling.x + self.ceiling.width <= 0:
            self.ceiling, self.nextceiling = self.nextceiling, self.ceiling
        self.nextceiling.x = self.ceiling.x + self.ceiling.width
        self.ceiling.draw()
        self.nextceiling.draw()