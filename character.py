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

        # Configurações das animações
        self.idle_spritesheet = pygame.image.load("player_animation/Cyborg_idle.png")
        self.run_spritesheet = pygame.image.load("player_animation/Cyborg_run.png")
        self.jump_spritesheet = pygame.image.load("player_animation/Cyborg_jump.png")
        self.dash_spritesheet = pygame.image.load("player_animation/Cyborg_dash.png")

        self.idle_frames = []
        self.run_frames = []
        self.jump_frames = []
        self.dash_frames = []

        self.current_frame = 0
        self.animation_speed = 200  # Tempo entre frames
        self.last_animation_update = pygame.time.get_ticks()

        # Carregar frames de animação
        self.load_animation_frames(self.idle_spritesheet, self.idle_frames, self.idle_spritesheet.get_width()/4, self.idle_spritesheet.get_height(), 4)
        self.load_animation_frames(self.run_spritesheet, self.run_frames, self.run_spritesheet.get_width()/6, self.run_spritesheet.get_height(), 6)
        self.load_animation_frames(self.jump_spritesheet, self.jump_frames, self.jump_spritesheet.get_width()/4, self.jump_spritesheet.get_height(), 4)
        self.load_animation_frames(self.dash_spritesheet, self.dash_frames, 128, 48, 3)

        self.active_frames = self.idle_frames  #frames ativos

    def load_animation_frames(self, spritesheet, frame_list, frame_width, frame_height, frame_count):
        for i in range(frame_count):
            frame = spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame_list.append(frame)

    def draw(self):
        #animacao
        previous_frames = self.active_frames  #guarda qual era a animação anterior

        if self.dash_active:    #dash
            self.active_frames = self.dash_frames
        elif not self.touched_ground:  #pulando
            self.active_frames = self.jump_frames
        elif pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]:  #correndo
            self.active_frames = self.run_frames
        else:  #parado
            self.active_frames = self.idle_frames

        # se a animação mudou, reiniciar o índice do frame
        if self.active_frames != previous_frames:
            self.current_frame = 0

        # atualizando a animação
        now = pygame.time.get_ticks()
        if now - self.last_animation_update > self.animation_speed:
            self.last_animation_update = now
            self.current_frame = (self.current_frame + 1) % len(self.active_frames)

        # ajustando a posição do personagem no chão
        current_frame_image = self.active_frames[self.current_frame]
        frame_height = current_frame_image.get_height()
        self.y += self.height - frame_height
        self.height = frame_height

        # espelhar a animação se estiver indo pra esquerda ou direita, ne
        if self.direction == -1:  # só precisa mudar pra esquerda pq os sprites sao todos pra dreita
            current_frame_image = pygame.transform.flip(current_frame_image, True, False)

        # desenha o frame atual
        self.image.image = current_frame_image
        self.image.x = self.x
        self.image.y = self.y
        self.image.draw()

    def move(self, velx):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.direction = -1  # indo p esquerda
            self.x -= velx*self.janela.delta_time()
            self.image.x = self.x
        if pressed_keys[pygame.K_RIGHT]:
            self.direction = 1  # indo p direita
            self.x += velx*self.janela.delta_time()
            self.image.x = self.x

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
                self.x += dash_speed * self.janela.delta_time() * self.direction
                self.image.x = self.x
            else:
                self.dash_active = False

    def jump(self, gravity=11, jumpheight=1600, yvel=1600):
        self.touched_ground = False  # player está no ar
        self.y -= yvel*self.janela.delta_time()
        yvel -= gravity
        if yvel < -jumpheight - 100:  # final do jump
            yvel = jumpheight
            return False, gravity, jumpheight, yvel
        return True, gravity, jumpheight, yvel

    def check_ground(self, floor_y):
        if self.y >= floor_y - self.height:
            self.touched_ground = True
            self.can_dash = True
            self.y = floor_y - self.height
