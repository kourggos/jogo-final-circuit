import pygame
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.collision import *
from PPlay.keyboard import *
from character import *
from fade import *
from movingScenery import *
from objects import *
from random import randint

janela = Window(1360, 720)
background = Background(janela)
floor = Floor(janela)
ceiling = Ceiling(janela)
minHeight = floor.floor.y
maxheight = ceiling.ceiling.y + ceiling.ceiling.height
player = Character("playerrect.png", 0, 0, 1, 1, janela)
player.image.y = floor.floor.y - player.height
player.image.x = janela.width / 4
# -----------
p_up_wall = GameImage("playervertwall.png")
p_up_wall.y = player.image.y
p_up_wall.x = player.image.x + player.image.width/2
p_down_wall = GameImage("playervertwall.png")
p_down_wall.y = player.image.y + player.image.height - p_down_wall.height
p_down_wall.x = player.image.x + player.image.width/2
p_left_wall = GameImage("playersidewall.png")
p_left_wall.y = player.image.y
p_left_wall.x = player.image.x
p_right_wall = GameImage("playersidewall.png")
p_right_wall.y = player.image.y
p_right_wall.x = player.image.x + player.image.width - p_right_wall.width

l = [p_up_wall,p_down_wall,p_left_wall,p_right_wall]
# -----------
all_platforms_list = [("platforms/1x3box.png", minHeight - 448),
                      ("platforms/1x3box.png", minHeight - 64),   # nome do arquivo e posição Y
                ("platforms/2x2box.png", minHeight - 128),
                ("platforms/1x3tube.png", minHeight - 128),
                ("platforms/3x4hollowbox.png", maxheight),
                ("platforms/3x4hollowbox.png", minHeight - 192),
                ("platforms/3x05shallowplatform.png", minHeight - 320),
                ("platforms/5x1pillar.png", maxheight),
                ("platforms/3x1tube.png", minHeight - 192)]
game_platforms = []
jumping = False
gravity = 9
jumpheight = 1600
yvel = 1600
frames = 0
cronometro = 0
fps = 0
coli = {"cima":False, "baixo":False, "direita":False, "esquerda":False}
esq = False
dire = False
cima = False
baixo = False

while True:
    # ------- fps -------
    frames += 1
    cronometro += janela.delta_time()
    if cronometro > 1:
        fps = frames
        frames = 0
        cronometro = 0
    # --------------------

    background.move(player, coli["esquerda"], coli["direita"])
    floor.move(player, background, coli["esquerda"])
    ceiling.move(player, background, coli["esquerda"])

    p_up_wall.y = player.image.y
    p_up_wall.x = player.image.x + player.image.width/2 - p_up_wall.width/2

    p_down_wall.y = player.image.y + player.image.height - p_down_wall.height
    p_down_wall.x = player.image.x + player.image.width/2 - p_down_wall.width/2

    p_left_wall.y = player.image.y
    p_left_wall.x = player.image.x

    p_right_wall.y = player.image.y
    p_right_wall.x = player.image.x + player.image.width - p_right_wall.width

    # ---------------------
    
    if pygame.key.get_pressed()[pygame.K_SPACE] and not jumping and coli["baixo"]:
        jumping = True
        coli["baixo"] = False
        yvel = 1600
    if jumping:
        jumping, gravity, jumpheight, yvel = player.jump(coli["baixo"], coli["cima"], gravity, jumpheight, yvel)

    # ----------- colisões player-plataformas -------------
    
    for platform in game_platforms:
        if (Collision.collided(player.image, platform.body) and p_right_wall.x < platform.body.x): #and (player.y + player.height >= platform.body.y or player.y < platform.body.y + platform.body.height):
            coli["esquerda"] = True
            esq = True
        elif not esq:
            coli["esquerda"] = False
        
        if (Collision.collided(player.image, platform.body) and p_left_wall.x + p_left_wall.width > platform.body.x + platform.body.width):  #and (player.y + player.height >= platform.body.y or player.y < platform.body.y + platform.body.height):
            coli["direita"] = True
            dire = True
        elif not dire:
            coli["direita"] = False
    	
        if (Collision.collided(p_up_wall, platform.body) and p_down_wall.y > platform.body.y + platform.body.height): #and (player.y + player.height >= platform.body.y or player.y < platform.body.y + platform.body.height):
            coli["cima"] = True
            cima = True
        elif not cima:
            coli["cima"] = False

        if (Collision.collided(p_down_wall, platform.body) and p_up_wall.y < platform.body.y): #and (player.y + player.height >= platform.body.y or player.y < platform.body.y + platform.body.height):
            coli["baixo"] = True
            player.touched_ground = True
            baixo = True
        elif not baixo:
            coli["baixo"] = False
    
    esq = False
    dire = False
    cima = False
    baixo = False   
 
    # movimento das plataformas
    
    for platform in game_platforms:
        if platform.move(player, background, coli["esquerda"]):
            game_platforms.remove(platform)
            del platform
        else:
            platform.draw()

    #print(coli["esquerda"], coli["direita"], coli["cima"], coli["baixo"])


    # ----------- gerar plataformas, precisa melhorar
    r = randint(0, len(all_platforms_list)-1)
    p = Platform(all_platforms_list[r][0], janela, y=all_platforms_list[r][1])
    for platform in game_platforms:
        if (platform.body.y < p.body.y + p.body.height and platform.body.y + platform.body.height > p.body.y):
            del p
            break
    try:
        if p:
            game_platforms.append(p)
    except:
        pass
    # --------------

    if not coli["baixo"] and player.image.y + player.image.height < floor.floor.y and not jumping:
        player.image.y += 1600*janela.delta_time()

    # ------------------------



    player.dash(1400)
    #reseta quando cai no chao
    if player.image.y >= floor.floor.y - player.image.height:
        player.image.y = floor.floor.y - player.image.height
        player.touched_ground = True  # jogador ta no chão
        coli["baixo"] = True
        baixo = True
        jumping = False
        player.can_dash = True  # pra usar o dash dnv
    if player.image.y <= ceiling.ceiling.height:
        coli["cima"] = True
        cima = True

    player.draw()
    for wall in l:
        wall.draw()
    janela.draw_text("fps:" + str(fps), 0, 0, size=14, color=(255,255,255))
    janela.update()
