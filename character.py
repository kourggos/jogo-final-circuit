import pygame
from PPlay.window import *
from PPlay.gameimage import *
from PPlay.collision import *
from PPlay.keyboard import *


class Character():
    def __init__(self, imagefilename, x, y, hp, speed, janela):
        self.image = GameImage(imagefilename)
        self.janela = janela
        self.width = self.image.width
        self.height = self.image.height
        self.image.x = x
        self.image.y = y
        self.x = self.image.x
        self.y = self.image.y
        self.hp = hp
        self.speed = speed
        self.can_dash = True
        self.dash_active = False
        self.dash_start_time = 0
        self.last_dash_time = 0
        self.touched_ground = True
        self.direction = 1
        self.dash_key_released = True

        self.dash_sound = pygame.mixer.Sound("songs/player_dash.mp3")
        self.dash_sound.set_volume(0.2)

        self.explosion_sound = pygame.mixer.Sound("songs/machine_explosion.mp3")
        self.explosion_sound.set_volume(0.4)
        
        # --------------
        self.point = GameImage("dashsprites/point.png")
        self.dashsprite_right = GameImage("dashsprites/dashspriteright.png")
        self.dashsprite_left = GameImage("dashsprites/dashspriteleft.png")
        self.dashsprite_up = GameImage("dashsprites/dashspriteup.png")
        self.dashsprite_down = GameImage("dashsprites/dashspritedown.png")
        self.dashsprite_ru = GameImage("dashsprites/dashspriteru.png")
        self.dashsprite_rd = GameImage("dashsprites/dashspriterd.png")
        self.dashsprite_lu = GameImage("dashsprites/dashspritelu.png")
        self.dashsprite_ld = GameImage("dashsprites/dashspriteld.png")
        self.dashsprite = self.point
        # ---------------
        self.dashduration = 0
        self.dashing = False
        self.dashes = [False, False, False, False]
        self.inside_wall = False
        self.in_wall_timer = 0
        # ---------------
        self.dead = False
        self.postdash = False


        # caminho das animacoes
        self.idle_spritesheet = pygame.image.load(
            "player_animation/Cyborg_idle.png")
        self.run_spritesheet = pygame.image.load(
            "player_animation/Cyborg_run.png")
        self.jump_spritesheet = pygame.image.load(
            "player_animation/Cyborg_jump.png")
        self.dash_spritesheet = pygame.image.load(
            "player_animation/Cyborg_dash.png")
        self.idle_wall_blue_spritesheet = pygame.image.load(
            "player_animation/Cyborg_idle_wall_blue.png")
        self.idle_wall_yellow_spritesheet = pygame.image.load(
            "player_animation/Cyborg_idle_wall_yellow.png")
        self.idle_wall_red_spritesheet = pygame.image.load(
            "player_animation/Cyborg_idle_wall_red.png")
        self.run_wall_blue_spritesheet = pygame.image.load(
            "player_animation/Cyborg_run_wall_blue.png")
        self.run_wall_yellow_spritesheet = pygame.image.load(
            "player_animation/Cyborg_run_wall_yellow.png")
        self.run_wall_red_spritesheet = pygame.image.load(
            "player_animation/Cyborg_run_wall_red.png")
        self.death_spritesheet = pygame.image.load(
            "player_animation/cyborg_death_explosion.png"
        )

        self.idle_frames = []
        self.run_frames = []
        self.jump_frames = []
        self.dash_frames = []
        self.idle_wall_blue_frames = []
        self.idle_wall_yellow_frames = []
        self.idle_wall_red_frames = []
        self.run_wall_blue_frames = []
        self.run_wall_yellow_frames = []
        self.run_wall_red_frames = []
        self.death_frames = []

        self.current_frame = 0
        self.animation_speed = 100  # Tempo entre frames
        self.last_animation_update = pygame.time.get_ticks()

        #carregando os frames
        self.load_animation_frames(self.idle_spritesheet, self.idle_frames, self.idle_spritesheet.get_width() // 4,
                                   self.idle_spritesheet.get_height(), 4)
        self.load_animation_frames(self.run_spritesheet, self.run_frames, self.run_spritesheet.get_width() // 6,
                                   self.run_spritesheet.get_height(), 6)
        self.load_animation_frames(self.jump_spritesheet, self.jump_frames, self.jump_spritesheet.get_width() // 4,
                                   self.jump_spritesheet.get_height(), 4)
        self.load_animation_frames(self.dash_spritesheet, self.dash_frames, 128, 48, 3)
        self.load_animation_frames(self.idle_wall_blue_spritesheet, self.idle_wall_blue_frames, self.idle_wall_blue_spritesheet.get_width() // 4,
                                   self.idle_wall_blue_spritesheet.get_height(), 4)
        self.load_animation_frames(self.idle_wall_yellow_spritesheet, self.idle_wall_yellow_frames, self.idle_wall_yellow_spritesheet.get_width() // 4,
                                   self.idle_wall_yellow_spritesheet.get_height(), 4)
        self.load_animation_frames(self.idle_wall_red_spritesheet, self.idle_wall_red_frames, self.idle_wall_red_spritesheet.get_width() // 4,
                                   self.idle_wall_red_spritesheet.get_height(), 4)
        self.load_animation_frames(self.run_wall_blue_spritesheet, self.run_wall_blue_frames, self.run_wall_blue_spritesheet.get_width() // 6,
                                   self.run_wall_blue_spritesheet.get_height(), 6)
        self.load_animation_frames(self.run_wall_yellow_spritesheet, self.run_wall_yellow_frames, self.run_wall_yellow_spritesheet.get_width() // 6,
                                   self.run_wall_yellow_spritesheet.get_height(), 6)
        self.load_animation_frames(self.run_wall_red_spritesheet, self.run_wall_red_frames, self.run_wall_red_spritesheet.get_width() // 6,
                                   self.run_wall_red_spritesheet.get_height(), 6)
        self.load_animation_frames(self.death_spritesheet, self.death_frames, self.death_spritesheet.get_width() // 18,
                                   self.death_spritesheet.get_height(), 18)
        

        self.active_frames = self.idle_frames  # Frames ativos inicialmente




    def load_animation_frames(self, spritesheet, frame_list, frame_width, frame_height, frame_count):
        for i in range(frame_count):
            frame = spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame_list.append(frame)

    def draw(self):
        previous_frames = self.active_frames  #guarda qual era a animação anterior

        # Determina qual animação usar
        if self.dead:
            self.active_frames = self.death_frames
        elif self.dash_active:  # dash
            self.active_frames = self.dash_frames
        elif not self.touched_ground:  # pulando
            self.active_frames = self.jump_frames
        elif pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]:  # correndo
            if not self.inside_wall:
                self.active_frames = self.run_frames
            elif self.in_wall_timer < 1:
                self.active_frames = self.run_wall_blue_frames
            elif self.in_wall_timer < 2:
                self.active_frames = self.run_wall_yellow_frames
            elif self.in_wall_timer < 3:
                self.active_frames = self.run_wall_red_frames
        else:  # parado
            if not self.inside_wall:
                self.active_frames = self.idle_frames
            elif self.in_wall_timer < 1:
                self.active_frames = self.idle_wall_blue_frames
            elif self.in_wall_timer < 2:
                self.active_frames = self.idle_wall_yellow_frames
            elif self.in_wall_timer < 3:
                self.active_frames = self.idle_wall_red_frames

        # se a animação mudar, vai reiniciar o indice dos frames
        if self.active_frames != previous_frames:
            self.current_frame = 0

        # atualizando a animação
        now = pygame.time.get_ticks()
        if now - self.last_animation_update > self.animation_speed:
            self.last_animation_update = now
            self.current_frame = (self.current_frame + 1) % len(self.active_frames)
            if self.dead and self.current_frame == 6:
                self.explosion_sound.play()
            
        #frame atual
        current_frame_image = self.active_frames[self.current_frame]

        # Espelha o frame se necessário
        if self.direction == -1:  # indo para a esquerda
            current_frame_image = pygame.transform.flip(current_frame_image, True, False)

        #aqui eu declarei esse offset pra centralizar o sprite com o retangulo
        base_offset_x = 29  #aq é o quando a animação vai mexer no eixo x pra centralizar com o retangulo
        if self.direction == -1:  #se tiver virado para a esquerda
            offset_x = (self.width - current_frame_image.get_width()) // 2 - base_offset_x
        else:  #se tiver virado para a direita
            offset_x = (self.width - current_frame_image.get_width()) // 2 + base_offset_x

        offset_y = self.height - current_frame_image.get_height()  #alinha verticalmente

        #aq eu desenho o frame na posição q eu quero
        self.janela.screen.blit(current_frame_image, (self.image.x + offset_x, self.image.y + offset_y))

        self.janela.screen.blit(current_frame_image, (self.image.x + offset_x, self.image.y + offset_y))

    def move(self, velx, esq, dire):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] and not dire and self.image.x > 0:
            self.direction = -1  # indo p esquerda
            self.image.x -= velx*self.janela.delta_time()
            #self.image.x = self.x
        if pressed_keys[pygame.K_RIGHT] and not esq:
            self.direction = 1  # indo p direita
            self.image.x += velx*self.janela.delta_time()
            #self.image.x = self.x

    def dash(self, dictdash):
        c = 0
        if self.dashing and self.dashduration == 0:
            self.dashes = [dictdash["left"], dictdash["right"], dictdash["up"], dictdash["down"]]
            self.dash_sound.play()
        for i in self.dashes:
            if i:
                c += 1

        if c == 1:
            if dictdash["left"]:
                self.dashsprite_left.x = self.image.x - self.dashsprite_left.width
                self.dashsprite_left.y = self.image.y + self.image.height/2 - self.dashsprite_left.height/2
            elif dictdash["right"]:
                self.dashsprite_right.x = self.image.x + self.image.width
                self.dashsprite_right.y = self.image.y + self.dashsprite_right.height/2
            elif dictdash["up"]:
                self.dashsprite_up.x = self.image.x + self.image.width/2 - self.dashsprite_up.width/2
                self.dashsprite_up.y = self.image.y - self.dashsprite_up.height
            elif dictdash["down"]:
                self.dashsprite_down.x = self.image.x + self.image.width/2 - self.dashsprite_down.width/2
                self.dashsprite_down.y = self.image.y + self.image.height
        elif c == 2:
            if self.dashes[1] and self.dashes[2]:
                self.dashsprite_lu.x = self.image.x + self.image.width
                self.dashsprite_lu.y = self.image.y - self.dashsprite_lu.height

            elif self.dashes[0] and self.dashes[2]:
                self.dashsprite_ru.x = self.image.x - self.dashsprite_ru.width
                self.dashsprite_ru.y = self.image.y - self.dashsprite_ru.height

            elif self.dashes[1] and self.dashes[3]:
                self.dashsprite_ld.x = self.image.x + self.image.width
                self.dashsprite_ld.y = self.image.y + self.image.height

            elif self.dashes[0] and self.dashes[3]:
                self.dashsprite_rd.x = self.image.x - self.dashsprite_rd.width
                self.dashsprite_rd.y = self.image.y + self.image.height

        if self.dashduration < 0.08 and self.dashing and c != 0:
            if c == 1:
                if self.dashes[0]:
                    self.dashsprite = self.dashsprite_left
                    self.dashsprite.draw()
                if self.dashes[1]:
                    self.dashsprite = self.dashsprite_right
                    self.dashsprite.draw()
                if self.dashes[2]:
                    self.dashsprite = self.dashsprite_up
                    self.dashsprite.draw()
                if self.dashes[3]:
                    self.dashsprite = self.dashsprite_down
                    self.dashsprite.draw()
            elif c == 2:
                if self.dashes[1] and self.dashes[2]:
                    self.dashsprite = self.dashsprite_lu
                    self.dashsprite.draw()
                elif self.dashes[0] and self.dashes[2]:
                    self.dashsprite = self.dashsprite_ru
                    self.dashsprite.draw()
                elif self.dashes[1] and self.dashes[3]:
                    self.dashsprite = self.dashsprite_ld
                    self.dashsprite.draw()
                elif self.dashes[0] and self.dashes[3]:
                    self.dashsprite = self.dashsprite_rd
                    self.dashsprite.draw()
            self.dashduration += self.janela.delta_time()
        else:
            self.dashduration = 0
            self.dashing = False
            self.dashsprite = self.point
            if c == 1:
                if self.dashes[0]:
                    self.image.x = self.dashsprite_left.x - self.image.width
                    #self.image.y = self.dashsprite_left.y - self.dashsprite_left.height/2
                if self.dashes[1]:
                    self.image.x = self.dashsprite_right.x + self.dashsprite_right.width
                    #self.image.y = self.dashsprite_right.y - self.dashsprite_right.height/2
                if self.dashes[2]:
                    if self.dashes[2] == "ceil":
                        self.image.y = 64
                    else:
                        self.image.y = self.dashsprite_up.y - self.image.height
                    #self.image.x = self.dashsprite_up.x + self.dashsprite_up.width/2
                if self.dashes[3]:
                    self.image.y = self.dashsprite_down.y + self.image.height
                    #self.image.x = self.dashsprite_down.x - self.dashsprite_down.width/2
            elif c == 2:
                if self.dashes[1] and self.dashes[2]:
                    self.image.x = self.dashsprite_lu.x + self.dashsprite_lu.width
                    if self.dashes[2] == "ceil":
                        self.image.y = 64
                    else:
                        self.image.y = self.dashsprite_lu.y - self.image.height
                elif self.dashes[0] and self.dashes[2]:
                    self.image.x = self.dashsprite_ru.x - self.image.width
                    if self.dashes[2] == "ceil":
                        self.image.y = 64
                    else:
                        self.image.y = self.dashsprite_lu.y - self.image.height
                elif self.dashes[1] and self.dashes[3]:
                    self.image.x = self.dashsprite_ld.x + self.image.width
                    self.image.y = self.dashsprite_ld.y + self.image.height
                elif self.dashes[0] and self.dashes[3]:
                    self.image.x = self.dashsprite_rd.x - self.image.width
                    self.image.y = self.dashsprite_rd.y + self.image.height


    def jump(self, colibaixo, colicima, gravity=11, jumpheight=1600, yvel=1600):
        self.touched_ground = False  # player está no ar
        if not self.dashing:
            self.image.y -= yvel*self.janela.delta_time()
            if colicima:
                yvel = -400
            yvel -= gravity*self.janela.delta_time()
        if yvel < -jumpheight - 720 or colibaixo:  # final do jump
            yvel = 1600
            return False, gravity, jumpheight, yvel
        return True, gravity, jumpheight, yvel

    def check_ground(self, floor_y):
        if self.image.y >= floor_y - self.height:
            self.touched_ground = True
            self.can_dash = True
            self.image.y = floor_y - self.height

class BipedalUnit():
    def __init__(self, x, y, janela):
        self.body = GameImage("enemies/bipedal_unit_inv.png")
        self.body.x = x
        self.body.y = y
        self.janela = janela
        self.type = "bipedalunit"

        self.idle_spritesheet = pygame.image.load(
            "enemies/bipedal_unit_idle_inv.png")
        
        self.current_frame = 0
        self.animation_speed = 200  # Tempo entre frames
        self.last_animation_update = pygame.time.get_ticks()
        
        self.idle_frames = []

        self.load_animation_frames(self.idle_spritesheet, self.idle_frames, self.idle_spritesheet.get_width() // 7, self.idle_spritesheet.get_height(), 7)

        self.active_frames = self.idle_frames
        
    def draw(self):
        # atualizando a animação
        now = pygame.time.get_ticks()
        if now - self.last_animation_update > self.animation_speed:
            self.last_animation_update = now
            self.current_frame = (self.current_frame + 1) % len(self.active_frames)

        #frame atual
        current_frame_image = self.active_frames[self.current_frame]

        #aqui eu declarei esse offset pra centralizar o sprite com o retangulo

        offset_x = (self.body.width - current_frame_image.get_width()) // 2

        offset_y = self.body.height - current_frame_image.get_height()  #alinha verticalmente

        #aq eu desenho o frame na posição q eu quero
        self.janela.screen.blit(current_frame_image, (self.body.x + offset_x, self.body.y + offset_y))

        self.janela.screen.blit(current_frame_image, (self.body.x + offset_x, self.body.y + offset_y))

    def load_animation_frames(self, spritesheet, frame_list, frame_width, frame_height, frame_count):
        for i in range(frame_count):
            frame = spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame_list.append(frame)

    def move(self, player, background, esq, velx=0, vely=0):
        if not player.dead:
            if player.image.x >= self.janela.width*7.5/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
                self.body.x -= 1200*self.janela.delta_time() # 0.9
            elif player.image.x >= self.janela.width*7/21 and player.image.x < self.janela.width*7.5/21  and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
                self.body.x -= 750*self.janela.delta_time() # 0.6
            if self.body.x + self.body.width < 0:
                return True
            return False
        
class CarGuy():
    def __init__(self, x, y, janela):
        self.body = GameImage("enemies/carguy.png")
        self.body.x = x
        self.body.y = y
        self.janela = janela
        self.type = "carguy"

        self.idle_spritesheet = pygame.image.load(
            "enemies/carguy_animation.png")
        
        self.current_frame = 0
        self.animation_speed = 200  # Tempo entre frames
        self.last_animation_update = pygame.time.get_ticks()
        
        self.idle_frames = []

        self.load_animation_frames(self.idle_spritesheet, self.idle_frames, self.idle_spritesheet.get_width() // 4, self.idle_spritesheet.get_height(), 4)

        self.active_frames = self.idle_frames
        
    def draw(self):
        # atualizando a animação
        now = pygame.time.get_ticks()
        if now - self.last_animation_update > self.animation_speed:
            self.last_animation_update = now
            self.current_frame = (self.current_frame + 1) % len(self.active_frames)

        #frame atual
        current_frame_image = self.active_frames[self.current_frame]

        #aqui eu declarei esse offset pra centralizar o sprite com o retangulo

        offset_x = (self.body.width - current_frame_image.get_width()) // 2

        offset_y = self.body.height - current_frame_image.get_height()  #alinha verticalmente

        #aq eu desenho o frame na posição q eu quero
        self.janela.screen.blit(current_frame_image, (self.body.x + offset_x, self.body.y + offset_y))

        self.janela.screen.blit(current_frame_image, (self.body.x + offset_x, self.body.y + offset_y))

    def load_animation_frames(self, spritesheet, frame_list, frame_width, frame_height, frame_count):
        for i in range(frame_count):
            frame = spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame_list.append(frame)

    def move(self, player, background, esq, velx=0, vely=0):
        if not player.dead:
            if player.image.x >= self.janela.width*7.5/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
                self.body.x -= 1200*self.janela.delta_time() # 0.9
            elif player.image.x >= self.janela.width*7/21 and player.image.x < self.janela.width*7.5/21  and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
                self.body.x -= 750*self.janela.delta_time() # 0.6
            if self.body.x + self.body.width < 0:
                return True
            return False
