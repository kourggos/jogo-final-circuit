import pygame
from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse

class Menu:
    def __init__(self, janela):
        self.janela = janela
        self.mouse = Mouse()
        self.font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 30)
        self.fonttitle = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 70)

        pygame.mixer.music.load("songs/solar_sailer.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        self.hover_sound = pygame.mixer.Sound("songs/hover.mp3")
        self.hover_sound.set_volume(0.2)

        # inicializando os botoes(x, y, largura, altura)
        self.background = GameImage("scenery/background.png")
        self.play_button = pygame.Rect(530, 200, 300, 60)
        self.how_to_play_button = pygame.Rect(530, 280, 300, 60)
        self.rank_button = pygame.Rect(530, 360, 300, 60)
        self.exit_button = pygame.Rect(530, 440, 300, 60)

    def draw_button(self, button_rect, text, active=False):
        # pra quando o mouse passar por cima
        color = (241, 241, 44) if active else (255, 255, 255)
        pygame.draw.rect(self.janela.screen, color, button_rect, 2)
        label = self.font.render(text, False, color)
        self.janela.screen.blit(label, (button_rect.x + (button_rect.width - label.get_width()) / 2,
                                        button_rect.y + (button_rect.height - label.get_height()) / 2))

    def show(self):
        last_played_button = None

        while True:
            self.janela.update()
            self.janela.screen.fill((0, 0, 0))
            self.background.draw()

            mouse_x, mouse_y = self.mouse.get_position()

            #ve se mouse sobre um botao
            play_active = self.play_button.collidepoint(mouse_x, mouse_y)
            how_to_play_active = self.how_to_play_button.collidepoint(mouse_x, mouse_y)
            rank_active = self.rank_button.collidepoint(mouse_x, mouse_y)
            exit_active = self.exit_button.collidepoint(mouse_x, mouse_y)

            #se o mouse estiver em cima de um botao, toca o som
            if play_active and last_played_button != "play":
                self.hover_sound.play()
                last_played_button = "play"
            elif how_to_play_active and last_played_button != "how_to_play":
                self.hover_sound.play()
                last_played_button = "how_to_play"
            elif rank_active and last_played_button != "rank":
                self.hover_sound.play()
                last_played_button = "rank"
            elif exit_active and last_played_button != "exit":
                self.hover_sound.play()
                last_played_button = "exit"
            elif not (play_active or how_to_play_active or rank_active or exit_active):
                last_played_button = None  #reset se n tiver em nenhum botao

            title_surface = self.fonttitle.render("Final Circuit", False, (255, 255, 255))
            self.janela.get_screen().blit(title_surface, (self.janela.width/2 - title_surface.get_width()/2, self.janela.height/7))
            self.draw_button(self.play_button, "JOGAR", play_active)
            self.draw_button(self.how_to_play_button, "COMO JOGAR", how_to_play_active)
            self.draw_button(self.rank_button, "RANKING", rank_active)
            self.draw_button(self.exit_button, "SAIR", exit_active)

            # Se o mouse clicou
            if play_active and self.mouse.is_button_pressed(1):
                return "jogar"
            elif how_to_play_active and self.mouse.is_button_pressed(1):
                return "como_jogar"
            elif rank_active and self.mouse.is_button_pressed(1):
                return "ranking"
            elif exit_active and self.mouse.is_button_pressed(1):
                return "sair"


class Ranking:
    def __init__(self, janela):
        self.janela = janela
        self.mouse = Mouse()
        self.font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 30)
        self.background = GameImage("scenery/background.png")
        self.hover_sound = pygame.mixer.Sound("songs/hover.mp3")
        self.hover_sound.set_volume(0.2)

    def draw_button(self, button_rect, text, active=False):
        # pra quando o mouse passar por cima
        color = (241, 241, 44) if active else (255, 255, 255)
        pygame.draw.rect(self.janela.screen, color, button_rect, 2)
        label = self.font.render(text, False, color)
        self.janela.screen.blit(label, (button_rect.x + (button_rect.width - label.get_width()) / 2,
                                        button_rect.y + (button_rect.height - label.get_height()) / 2))

    def show_ranking(self):
        last_played_button = None

        #lendo arquivo de ranking
        try:
            with open("ranking.txt", "r") as file:
                rankings = file.readlines()
        except FileNotFoundError:
            rankings = []

        #quantos rankings vão ser mostrados
        top_rankings = rankings[:5]

        #exibir resultado
        while True:
            self.janela.update()

            # Desenha o fundo do menu
            self.background.draw()

            self.background.draw()

            y_offset = 70  #começa a partir dessa posicao y

            for i, rank in enumerate(top_rankings):
                player_name, score = rank.strip().split(" - ")
                score = score.replace(" segundos", "")  #tira a parte de "segundos. é só tirar isso da main, mas faço isso depois, tanto faz

                #calculando posição fixa para o nome e pontuação
                name_x = self.janela.width / 2 - 500  #pos coluna para nome
                score_x = self.janela.width / 2 + 200  #pos coluna para pontuacao

                #desenhar o nome e a pontuação
                name_label = self.font.render(f"{i + 1}. {player_name}", False, (255, 255, 255))
                score_label = self.font.render(f"{score} pontos", False, (255, 255, 255))

                self.janela.screen.blit(name_label, (name_x, y_offset))
                self.janela.screen.blit(score_label, (score_x, y_offset))

                y_offset += 100  #espaçamento entre os rankings

            # Botão de voltar para o menu
            mouse_x, mouse_y = self.mouse.get_position()
            back_button = pygame.Rect(self.janela.width - 350, self.janela.height - 100, 200, 50)
            back_active = back_button.collidepoint(mouse_x, mouse_y)


            if back_active and last_played_button != "back":
                self.hover_sound.play()
                last_played_button = "back"
            elif not back_active:
                last_played_button = None


            self.draw_button(back_button, "Voltar", back_active)

            if back_active and self.mouse.is_button_pressed(1):
                return  # Volta para o menu


class HowToPlay:

    def __init__(self, janela):
        self.janela = janela
        self.mouse = Mouse()
        self.font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 30)
        self.instructions_image = GameImage("scenery/comojogar.png")
        self.back_button = pygame.Rect(self.janela.width - 350, self.janela.height - 100, 200, 50)
        self.hover_sound = pygame.mixer.Sound("songs/hover.mp3")
        self.hover_sound.set_volume(0.2)


    def draw_button(self, button_rect, text, active=False):
        # se o mouse ta em cima
        color = (241, 241, 44) if active else (255, 255, 255)
        pygame.draw.rect(self.janela.screen, color, button_rect, 2)
        label = self.font.render(text, False, color)
        self.janela.screen.blit(label, (button_rect.x + (button_rect.width - label.get_width()) / 2,
                                        button_rect.y + (button_rect.height - label.get_height()) / 2))

    def show(self):
        last_played_button = None

        while True:
            self.janela.update()
            self.janela.screen.fill((0, 0, 0))  #limpa tela
            self.instructions_image.draw()  #mostra as instrucoes

            mouse_x, mouse_y = self.mouse.get_position()

            back_active = self.back_button.collidepoint(mouse_x, mouse_y)

            if back_active and last_played_button != "back":
                self.hover_sound.play()
                last_played_button = "back"
            elif not back_active:
                last_played_button = None

            self.draw_button(self.back_button, "Voltar", back_active)

            if back_active and self.mouse.is_button_pressed(1):
                return "menu"


def run_game():
    import jogo  # Importa o script main diretamente
    jogo.main()  # Chama a função main() do main.py
    exit()


def main():
    janela = Window(1360, 720)
    menu = Menu(janela)

    while True:
        option = menu.show()

        if option == "jogar":
            run_game()
            break
        elif option == "como_jogar":
            how_to_play = HowToPlay(janela)
            how_to_play.show()
        elif option == "ranking":
            ranking = Ranking(janela)  #instancia nova de ranking
            ranking.show_ranking()
        elif option == "sair":
            janela.close()
            break


if __name__ == "__main__":
    main()
