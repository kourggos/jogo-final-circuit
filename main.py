import pygame
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.collision import *
from PPlay.keyboard import *
from character import *

clock = pygame.time.Clock()

janela = Window(1360, 720)
cenario = GameImage("PPlay/scenary/background2.png")
floor = GameImage("PPlay/scenary/floor.png")
ceiling = GameImage("PPlay/scenary/ceiling.png")
player = Character("playerinv.png", 0, 0, 1, 1)
floor.y = janela.height - floor.height
player.y = floor.y - player.height
player.x = janela.width / 4
jumping = False
gravity = 1
jumpheight = 20
yvel = jumpheight

while True:
    clock.tick(60)

    if pygame.key.get_pressed()[pygame.K_SPACE] and not jumping:
        jumping = True
    if jumping:
        jumping, gravity, jumpheight, yvel = player.jump(gravity, jumpheight, yvel)

    player.dash(20)

    #reseta quando cai no chao
    if player.y >= floor.y - player.height:
        player.y = floor.y - player.height
        player.touched_ground = True  # jogador ta no chão
        jumping = False
        player.can_dash = True  # pra usar o dash dnv

    player.move(12)
    cenario.draw()
    floor.draw()
    ceiling.draw()
    player.draw()
    janela.update()
