import pygame


class Fade():
    def __init__(self, janela):
        self.janela = janela

    def fade(self):
        fade = pygame.Surface((self.janela.width, self.janela.height))
        fade.fill((0,0,0))
        for i in range(0, 150):
            fade.set_alpha(i)
            #self.redrawWindow()
            self.janela.screen.blit(fade,(0,0))
            self.janela.update()
            pygame.time.delay(5)

    #def redrawWindow(self):
        #self.janela.screen.fill((255,255,255))
        #pygame.draw.rect(self.janela.screen, (255,0,0), (200,300,200,200), 0)
        #pygame.draw.rect(self.janela.screen, (0,255,0), (500,500,100,200), 0)