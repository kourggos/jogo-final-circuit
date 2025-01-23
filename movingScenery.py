import pygame
from fade import *
from PPlay.gameimage import *

class Background():
    def __init__(self, janela):
        self.janela = janela
        self.bg_list = [GameImage("scenery/background_city_day_big.png"), 
                        GameImage("scenery/background_city_night_big.png"), 
                        GameImage("scenery/bulkhead_background.png"),
                        GameImage("scenery/sewers_background.png"),
                        GameImage("scenery/lab_background.png")]
        self.cenario = self.bg_list[0]
        self.bg_change = False
        self.bg_atual = 0
        self.fading = False

    def move(self, player, esq, dire):
        if not player.dead:
            if player.image.x >= self.janela.width*7.5/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not self.bg_change and not esq and not player.dashing:
                self.cenario.x -= 1200*self.janela.delta_time() # 0.9
                if not dire:
                    player.move(-500, esq, dire)

            elif player.image.x >= self.janela.width*7/21 and player.image.x < self.janela.width*7.5/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not self.bg_change and not esq and not player.dashing:
                self.cenario.x -= 750*self.janela.delta_time() # 0.6
                self.fading = False
            elif not player.dashing:
                player.move(1200, esq, dire)
            if self.cenario.x + self.cenario.width <= self.janela.width:
                self.bg_change = True
            if self.bg_change and player.image.x > self.janela.width:
                self.fading = True
                Fade(self.janela).fade()
                player.image.x = self.janela.width / 4
                self.bg_atual += 1
                if self.bg_atual == len(self.bg_list):
                    self.bg_atual = 0
                self.cenario = self.bg_list[self.bg_atual]
                self.cenario.x = 0
            #if self.bg_atual == len(self.bg_list) - 1:
            #    self.bg_atual = 0
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

    def move(self, player, background, esq):
        if not player.dead:
            if player.image.x >= self.janela.width*7.5/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
                self.floor.x -= 1200*self.janela.delta_time() # 0.9
            elif player.image.x >= self.janela.width*7/21 and player.image.x < self.janela.width*7.5/21  and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
                self.floor.x -= 750*self.janela.delta_time() # 0.6
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

    def move(self, player, background, esq):
        if not player.dead:
            if player.image.x >= self.janela.width*7.5/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
                self.ceiling.x -= 1200*self.janela.delta_time() # 0.9
            elif player.image.x >= self.janela.width*7/21 and player.image.x < self.janela.width*7.5/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
                self.ceiling.x -= 720*self.janela.delta_time() # 0.6
            if self.ceiling.x + self.ceiling.width <= 0:
                self.ceiling, self.nextceiling = self.nextceiling, self.ceiling
        self.nextceiling.x = self.ceiling.x + self.ceiling.width
        self.ceiling.draw()
        self.nextceiling.draw()
