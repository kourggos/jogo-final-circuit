import pygame
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.collision import *
from PPlay.keyboard import *
from character import *
from fade import *
from movingScenery import *

janela = Window(1360, 720)
background = Background(janela)
floor = Floor(janela)
ceiling = Ceiling(janela)
player = Character("player.png", 0, 0, 1, 1, janela)
player.y = floor.floor.y - player.height
player.x = janela.width / 4
jumping = False
gravity = 9
jumpheight = 1600
yvel = 1600
frames = 0
cronometro = 0
fps = 0

while True:

    # ------- fps -------
    frames += 1
    cronometro += janela.delta_time()
    if cronometro > 1:
        fps = frames
        frames = 0
        cronometro = 0
    # --------------------
    
    if pygame.key.get_pressed()[pygame.K_SPACE] and not jumping:
        jumping = True
    if jumping:
        jumping, gravity, jumpheight, yvel = player.jump(gravity, jumpheight, yvel)

    player.dash(1400)
    #reseta quando cai no chao
    if player.y >= floor.floor.y - player.height:
        player.y = floor.floor.y - player.height
        player.touched_ground = True  # jogador ta no chão
        jumping = False
        player.can_dash = True  # pra usar o dash dnv
    
    background.move(player)
    floor.move(player, background)
    ceiling.move(player, background)
    player.draw()
    janela.draw_text("fps:" + str(fps), 0, 0, size=14, color=(255,255,255))
    janela.update()
