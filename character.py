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

        # caminho das animacoes
        self.idle_spritesheet = pygame.image.load(
            "player_animation/Cyborg_idle.png")
        self.run_spritesheet = pygame.image.load(
            "player_animation/Cyborg_run.png")
        self.jump_spritesheet = pygame.image.load(
            "player_animation/Cyborg_jump.png")
        self.dash_spritesheet = pygame.image.load(
            "player_animation/Cyborg_dash.png")

        self.idle_frames = []
        self.run_frames = []
        self.jump_frames = []
        self.dash_frames = []

        self.current_frame = 0
        self.animation_speed = 200  # Tempo entre frames
        self.last_animation_update = pygame.time.get_ticks()

        #carregando os frames
        self.load_animation_frames(self.idle_spritesheet, self.idle_frames, self.idle_spritesheet.get_width() // 4,
                                   self.idle_spritesheet.get_height(), 4)
        self.load_animation_frames(self.run_spritesheet, self.run_frames, self.run_spritesheet.get_width() // 6,
                                   self.run_spritesheet.get_height(), 6)
        self.load_animation_frames(self.jump_spritesheet, self.jump_frames, self.jump_spritesheet.get_width() // 4,
                                   self.jump_spritesheet.get_height(), 4)
        self.load_animation_frames(self.dash_spritesheet, self.dash_frames, 128, 48, 3)

        self.active_frames = self.idle_frames  # Frames ativos inicialmente
    def load_animation_frames(self, spritesheet, frame_list, frame_width, frame_height, frame_count):
        for i in range(frame_count):
            frame = spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame_list.append(frame)

    def draw(self):
        previous_frames = self.active_frames  #guarda qual era a animação anterior

        # Determina qual animação usar
        if self.dash_active:  # dash
            self.active_frames = self.dash_frames
        elif not self.touched_ground:  # pulando
            self.active_frames = self.jump_frames
        elif pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]:  # correndo
            self.active_frames = self.run_frames
        else:  # parado
            self.active_frames = self.idle_frames

        # se a animação mudar, vai reiniciar o indice dos frames
        if self.active_frames != previous_frames:
            self.current_frame = 0

        # atualizando a animação
        now = pygame.time.get_ticks()
        if now - self.last_animation_update > self.animation_speed:
            self.last_animation_update = now
            self.current_frame = (self.current_frame + 1) % len(self.active_frames)

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
        if pressed_keys[pygame.K_LEFT] and not dire:
            self.direction = -1  # indo p esquerda
            self.image.x -= velx*self.janela.delta_time()
            #self.image.x = self.x
        if pressed_keys[pygame.K_RIGHT] and not esq:
            self.direction = 1  # indo p direita
            self.image.x += velx*self.janela.delta_time()
            #self.image.x = self.x

    def dash(self, dash_speed):
        pressed_keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if (pressed_keys[pygame.K_LSHIFT] or pressed_keys[pygame.K_RSHIFT]):
            if self.dash_key_released:
                self.dash_key_released = False
                if self.can_dash and not self.dash_active and current_time - self.last_dash_time >= 1500: #1500 = 1,5 segundos de cooldown pra usar o dash
                    self.dash_active = True
                    self.dash_start_time = current_time
                    self.can_dash = False
                    self.touched_ground = False

        if not (pressed_keys[pygame.K_LSHIFT] or pressed_keys[pygame.K_RSHIFT]):
            self.dash_key_released = True

        if self.dash_active:
            if current_time - self.dash_start_time < 300:  #duração do dash (300 = 0.3 segundos)
                self.image.x += dash_speed * self.janela.delta_time() * self.direction
                #self.image.x = self.x
            else:
                self.dash_active = False

    def jump(self, colibaixo, colicima, gravity=11, jumpheight=1600, yvel=1600):
        self.touched_ground = False  # player está no ar
        self.image.y -= yvel*self.janela.delta_time()
        if colicima:
            yvel = -400
        yvel -= gravity
        if yvel < -jumpheight - 720 or colibaixo:  # final do jump
            yvel = 1600
            return False, gravity, jumpheight, yvel
        return True, gravity, jumpheight, yvel

    def check_ground(self, floor_y):
        if self.image.y >= floor_y - self.height:
            self.touched_ground = True
            self.can_dash = True
            self.image.y = floor_y - self.height

