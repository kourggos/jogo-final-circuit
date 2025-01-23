import pygame
from PPlay.gameimage import *

class Platform():
    def __init__(self, arq, janela, y):
        self.janela = janela
        self.body = GameImage(arq)
        self.body.x = janela.width
        self.body.y = y
        self.enemy = False

    def move(self, player, background, esq, velx=0, vely=0):
        if player.image.x >= self.janela.width*7.5/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
            self.body.x -= 1200*self.janela.delta_time() # 0.9
        elif player.image.x >= self.janela.width*7/21 and player.image.x < self.janela.width*7.5/21  and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
            self.body.x -= 750*self.janela.delta_time() # 0.6
        if self.body.x + self.body.width < 0:
            return True
        return False

    def draw(self):
        self.body.draw()

class Explosion():
    def __init__(self, x, y, janela):
        self.janela = janela
        self.body = GameImage("enemies/big_explosion_sprite.png")
        self.body.x = x
        self.body.y = y

        self.explosion_spritesheet = pygame.image.load("enemies/big_explosion.png")
        self.explosion_frames = []

        self.current_frame = 0
        self.animation_speed = 65  # Tempo entre frames
        self.last_animation_update = pygame.time.get_ticks()

        self.load_animation_frames(self.explosion_spritesheet, self.explosion_frames, self.explosion_spritesheet.get_width() // 12,
                                   self.explosion_spritesheet.get_height(), 12)
        
        self.active_frames = self.explosion_frames

    def load_animation_frames(self, spritesheet, frame_list, frame_width, frame_height, frame_count):
        for i in range(frame_count):
            frame = spritesheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frame_list.append(frame)

    def draw(self):
        previous_frames = self.active_frames  #guarda qual era a animação anterior

        # se a animação mudar, vai reiniciar o indice dos frames
        #if self.active_frames != previous_frames:
            #self.current_frame = 0

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

    def move(self, player, background, esq, velx=0, vely=0):
        if player.image.x >= self.janela.width*7.5/21 and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
            self.body.x -= 1200*self.janela.delta_time() # 0.9
        elif player.image.x >= self.janela.width*7/21 and player.image.x < self.janela.width*7.5/21  and pygame.key.get_pressed()[pygame.K_RIGHT] and not background.bg_change and not esq and not player.dashing:
            self.body.x -= 750*self.janela.delta_time() # 0.6
        if self.body.x + self.body.width < 0:
            return True
        return False

