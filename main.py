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
import subprocess

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
all_platforms_list = [("platforms/1x3box.png", minHeight - 384),
                      ("platforms/1x3box.png", minHeight - 192),   # nome do arquivo e posição Y
                ("platforms/2x2box.png", minHeight - 192),
                ("platforms/1x3tube.png", minHeight - 128),
                ("platforms/3x4hollowbox.png", maxheight),
                #("platforms/3x4hollowbox.png", minHeight - 192),
                ("platforms/3x05shallowplatform.png", minHeight - 320),
                ("platforms/5x1pillar.png", maxheight),
                ("platforms/5x1pillar.png", minHeight - 64*5),
                ("platforms/3x1tube.png", minHeight - 192),
                ("platforms/1x5pillar.png", minHeight - 256)]
game_platforms = []
# -------------
game_explosions = []
explo_sprite = Explosion(0,0, janela)
# -------------
game_enemies = []
jumping = False
gravity = 14
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
cddash = 1
dictdash = {"left":False, "up":False, "down":False, "right":False}
bipedalenemy = BipedalUnit(0, 0, janela)
carguyenemy = CarGuy(0, 0, janela)
inwall = 0
c = 0
velx = 750

timer_seconds = 10 #muda aqui o timer do jogo.
timer_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 30)
pygame.mixer.music.load("songs/TRON_legacy.mp3")
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(-1)
timer_running = True

pontos = 0

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return str(int(minutes)) + ":" + str(int(seconds)) + ":" +  str("%.2f" % seconds)[3:]

def save_to_ranking(player_name, score):
    try:
        with open("ranking.txt", "r") as file:
            rankings = file.readlines()
    except FileNotFoundError:
        rankings = []

    rankings.append(f"{player_name} - {int(score)} segundos\n")
    #ordem decrescente
    rankings.sort(key=lambda x: int(x.split(" - ")[1].split(" ")[0]), reverse=True)
    #salvando
    with open("ranking.txt", "w") as file:
        file.writelines(rankings)

def game_over():
    global timer_running
    timer_running = False

    game_over_surface = timer_font.render("VOCÊ PERDEU!", True, (255, 0, 0))
    janela.get_screen().blit(game_over_surface, (janela.width / 2 - 200, janela.height / 2 - 50))

    janela.update()
    print("Digite seu nome para salvar no ranking: ")
    player_name = input().strip()
    if player_name:
        save_to_ranking(player_name, pontos)

    pygame.quit()
    subprocess.run(["python", "menu.py"])
    exit()  # Sai do jogo


while True:
    # ------- fps -------
    frames += 1
    cronometro += janela.delta_time()
    if cronometro > 1:
        fps = frames
        frames = 0
        cronometro = 0

        # Atualizando o timer
    if timer_running:
        timer_seconds -= janela.delta_time()
        pontos += janela.delta_time()  #+1 ponto todo segundo
        if timer_seconds <= 0:
            result = game_over()
            if result == "menu":
                break
    # --------------------

    background.move(player, coli["esquerda"], coli["direita"])
    floor.move(player, background, coli["esquerda"])
    ceiling.move(player, background, coli["esquerda"])

    p_up_wall.y = player.image.y
    p_up_wall.x = player.image.x + player.image.width/2 - p_up_wall.width/2

    p_down_wall.y = player.image.y + player.image.height - p_down_wall.height
    p_down_wall.x = player.image.x + player.image.width/2 - p_down_wall.width/2

    p_left_wall.y = player.image.y
    p_left_wall.x = player.image.x + 10

    p_right_wall.y = player.image.y
    p_right_wall.x = player.image.x + player.image.width - p_right_wall.width - 10

    # ---------------------
    

    if pygame.key.get_pressed()[pygame.K_SPACE] and not jumping and coli["baixo"] and not player.inside_wall and not player.dead:
        jumping = True
        coli["baixo"] = False
    if jumping:
        jumping, gravity, jumpheight, yvel = player.jump(coli["baixo"], coli["cima"], gravity, jumpheight, yvel)

    # ----------- colisões player-plataformas -------------
    
    inwall = 0

    esq = False
    dire = False
    cima = False
    baixo = False   

    for platform in game_platforms:
        if (Collision.collided(player.image, platform.body) and p_right_wall.x < platform.body.x) or player.inside_wall: #and (player.y + player.height >= platform.body.y or player.y < platform.body.y + platform.body.height):
            coli["esquerda"] = True
            esq = True
        elif not esq:
            coli["esquerda"] = False
        
        if (Collision.collided(player.image, platform.body) and p_left_wall.x + p_left_wall.width > platform.body.x + platform.body.width) or player.inside_wall:  #and (player.y + player.height >= platform.body.y or player.y < platform.body.y + platform.body.height):
            coli["direita"] = True
            dire = True
        elif not dire:
            coli["direita"] = False
    	
        if (Collision.collided(p_up_wall, platform.body) and p_down_wall.y > platform.body.y + platform.body.height) or player.inside_wall: #and (player.y + player.height >= platform.body.y or player.y < platform.body.y + platform.body.height):
            coli["cima"] = True
            cima = True
        elif not cima:
            coli["cima"] = False

        if (Collision.collided(p_down_wall, platform.body) and p_up_wall.y < platform.body.y) or player.inside_wall: #and (player.y + player.height >= platform.body.y or player.y < platform.body.y + platform.body.height):
            coli["baixo"] = True
            player.touched_ground = True
            baixo = True
        elif not baixo:
            coli["baixo"] = False

        if Collision.collided(p_left_wall, platform.body) and Collision.collided(p_right_wall, platform.body) and player.image.y + player.image.height/2 > platform.body.y and player.image.y + player.image.height/2 < platform.body.y + platform.body.height:
            inwall += 1

    if player.dashing:
        for i in coli:
            i = True

    if inwall > 0:
        player.inside_wall = True
    else:
        player.inside_wall = False
 
    if player.inside_wall:
        player.in_wall_timer += janela.delta_time()
    else:
        player.in_wall_timer = 0

    if player.in_wall_timer > 3:
        player.dead = True

    # movimento das plataformas
    
    for platform in game_platforms:
        if platform.move(player, background, coli["esquerda"]) or background.fading:
            game_platforms.remove(platform)
            del platform
        else:
            platform.draw()


    # ----------- gerar plataformas, precisa melhorar
    r = randint(0, len(all_platforms_list)-1)
    p = Platform(all_platforms_list[r][0], janela, y=all_platforms_list[r][1])
    for platform in game_platforms:
        #if (platform.body.y < p.body.y + p.body.height and platform.body.y + platform.body.height > p.body.y):
        if platform.body.x > 2*janela.width/3 or e == r or (carguyatual.body.x < janela.width and carguyatual.body.x + carguyatual.body.width > janela.width):
            del p
            break
    try:
        if p:
            game_platforms.append(p)
            e = r
    except:
        pass

    # -------------- spawnar inimigos

    for platform in game_platforms:
        if not platform.enemy and platform.body.width > bipedalenemy.body.width and platform.body.y - bipedalenemy.body.height > maxheight:
            if randint(1,2) == 1:
                game_enemies.append(BipedalUnit(platform.body.x + platform.body.width/2 - bipedalenemy.body.width/2, platform.body.y - bipedalenemy.body.height, janela))
            platform.enemy = True
    carguy = False
    for enemy in game_enemies:
        if enemy.type == "carguy":
            carguy = True
    if not carguy:
        carguyatual = CarGuy(janela.width*randint(2,5), minHeight - carguyenemy.body.height, janela)
        game_enemies.append(carguyatual)


    for enemy in game_enemies:
        if enemy.move(player, background, coli["esquerda"]) or background.fading:
            game_enemies.remove(enemy)
            del enemy
        elif Collision.collided(player.dashsprite, enemy.body):
            explo = Explosion(enemy.body.x + enemy.body.width/2 - explo_sprite.body.width/2, enemy.body.y + enemy.body.height - explo_sprite.body.height, janela)
            game_explosions.append([explo, 0])
            game_enemies.remove(enemy)
            del enemy
            timer_seconds += randint(0, 3)
        elif Collision.collided(player.image, enemy.body):
                if player.postdash:
                    explo = Explosion(enemy.body.x + enemy.body.width/2 - explo_sprite.body.width/2, enemy.body.y + enemy.body.height - explo_sprite.body.height, janela)
                    game_explosions.append([explo, 0])
                    game_enemies.remove(enemy)
                    del enemy
                    timer_seconds += randint(3, 5)
                else:
                    player.dead = True
                    enemy.draw()
        else:
            enemy.draw()

    for duo in game_explosions:
        duo[1] += 280*janela.delta_time()
        if duo[1] >= 61*7/2 or duo[0].move(player, background, coli["esquerda"]):
            game_explosions.remove(duo)
            del duo[0]
        else:
           duo[0].draw()

    # ---------------

    if not coli["baixo"] and player.image.y + player.image.height < floor.floor.y and not jumping:
        if player.image.y - yvel*janela.delta_time() > ceiling.ceiling.height:
            player.image.y -= yvel*janela.delta_time()

    # ------------------------

    dictdash["left"] = pygame.key.get_pressed()[pygame.K_LEFT]
    dictdash["up"] = pygame.key.get_pressed()[pygame.K_UP]
    dictdash["down"] = pygame.key.get_pressed()[pygame.K_DOWN]
    dictdash["right"] = pygame.key.get_pressed()[pygame.K_RIGHT]

    if dictdash["left"] and dictdash["right"]:
        dictdash["left"] = False
        dictdash["right"] = False
    if dictdash["up"] and dictdash["down"]:
        dictdash["up"] = False
        dictdash["down"] = False

    d = 0
    li = [dictdash["left"],dictdash["up"],dictdash["down"],dictdash["right"]]
    for i in li:
        if i:
            d += 1
    
    if dictdash["down"] and d == 1:
        if player.image.y + player.image.height + player.dashsprite_down.height >= minHeight:
            dictdash["down"] = False
    elif dictdash["down"] and d == 2:
        if player.image.y + player.image.height + player.dashsprite_ld.height >= minHeight:
            dictdash["down"] = False
    if dictdash["up"] and d == 1:
        if player.image.y - player.dashsprite_up.height - player.image.height <= maxheight:
            dictdash["up"] = "ceil"
    elif dictdash["up"] and d == 2:
        if player.image.y - player.dashsprite_lu.height - player.image.height <= maxheight:
            dictdash["up"] = "ceil"

    if cddash > 1:
        if (pygame.key.get_pressed()[pygame.K_LSHIFT] or player.dashing) and not player.dead:
            player.dashing = True
            player.dash(dictdash)
            if not player.dashing:
                cddash = 0
    else:
        cddash += janela.delta_time()
    if cddash < 0.2:
        player.postdash = True
        yvel = -100
    elif not jumping:
        yvel -= gravity
    else:
        player.postdash = False
    
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

    #print(coli["cima"], cima)

    if player.dead and player.current_frame + 1 == len(player.active_frames):
        result = game_over()

    if not player.dashing:
        player.draw()
    for wall in l:
        wall.draw()

    #desenhando o temporizador
    if timer_running:
        timer_text = format_time(timer_seconds)
        timer_surface = timer_font.render(timer_text, True, (255, 255, 255))
        janela.get_screen().blit(timer_surface, (janela.width - timer_surface.get_width(), 10))

    janela.draw_text("fps:" + str(fps), 0, 0, size=14, color=(255,255,255))
    janela.update()
