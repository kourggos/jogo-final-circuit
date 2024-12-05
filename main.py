import pygame
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.collision import *
from PPlay.keyboard import *
from character import *

clock = pygame.time.Clock()

janela = Window(1360, 720)
cenario = GameImage("background2.png")
floor = GameImage("floor.png")
ceiling = GameImage("ceiling.png")
player = Character("playerinv.png", 0, 0, 1, 1)
teclado = janela.get_keyboard()
floor.y = janela.height - floor.height
player.y = floor.y - player.height
player.x = janela.width/4
jumping = False
maxheight = player.y + 3*player.height/2
gravity = 1
jumpheight = 20
yvel = jumpheight


while True:
    clock.tick(60)
    if teclado.key_pressed("space"):
        jumping = True
    if jumping:
        jumping, gravity, jumpheight, yvel = player.jump(gravity, jumpheight, yvel)
    player.move(12)
    cenario.draw()
    floor.draw()
    ceiling.draw()
    player.draw()
    janela.update()