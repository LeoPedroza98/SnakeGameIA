import random
import pygame
from constantes_game import *
from direcao import Direcao
from base_pygame import BaseGame

class JogoDaCobrinha(BaseGame):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption('Jogo da Cobrinha sem IA')

        self.game_open = True  # Variável que indica se o jogo está aberto ou não
        self.input_direcao = None  # Direção de entrada fornecida pelo usuário

    def reseta_game(self):
        # Reinicializa todas as variáveis e configurações do jogo para começar um novo jogo
        self.game_open = True
        self.vivo = True
        self.pontos = 0

        self.snake_lista = []  # Lista que armazena as coordenadas dos segmentos da cobra
        self.pos_x = DIS_LARG / 2  # Posição inicial da cabeça da cobra no eixo x
        self.pos_y = DIS_ALTURA / 2  # Posição inicial da cabeça da cobra no eixo y
        self.input_direcao = None  # Reinicializa a direção de entrada fornecida pelo usuário
        self.direcao = None  # Direção atual da cobra

        self.food_x = round(random.randrange(0, DIS_LARG - BLOCK_TAM) / 10.0) * 10.0  # Posição x aleatória da comida
        self.food_y = round(random.randrange(0, DIS_ALTURA - BLOCK_TAM) / 10.0) * 10.0  # Posição y aleatória da comida

    def botoes_usuarios(self, event):
        # Lida com os eventos de entrada do usuário (teclas pressionadas)
        if event.type == pygame.QUIT:
            self.game_open = False  # Fecha o jogo se o evento for o de fechar a janela
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.direcao != Direcao.DIREITA:
                self.input_direcao = Direcao.ESQUERDA  # Define a direção de entrada para a esquerda
            elif event.key == pygame.K_RIGHT and self.direcao != Direcao.ESQUERDA:
                self.input_direcao = Direcao.DIREITA  # Define a direção de entrada para a direita
            elif event.key == pygame.K_UP and self.direcao != Direcao.BAIXO:
                self.input_direcao = Direcao.CIMA  # Define a direção de entrada para cima
            elif event.key == pygame.K_DOWN and self.direcao != Direcao.CIMA:
                self.input_direcao = Direcao.BAIXO  # Define a direção de entrada para baixo

    def vida_pos_morte(self):
        # Exibe a mensagem de "Você morreu!" e oferece opções para finalizar ou reiniciar o jogo
        self.display.fill(BLACK)
        self.mesangem_tela("Vish você morreu! Aperte Q para finalizar o jogo ou C para resetar o game", WHITE)
        self.funcao_pontos_tela(self.pontos, 5, 5)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_open = False  # Fecha o jogo se a tecla 'Q' for pressionada
                    self.vivo = True
                if event.key == pygame.K_c:
                    self.game_loop()  # Reinicia o jogo se a tecla 'C' for pressionada

    def mesangem_tela(self, msg, color):
        # Exibe uma mensagem na tela
        font_style = pygame.font.SysFont("arial", 18)
        message = font_style.render(msg, True, color)
        self.display.blit(message, [10, DIS_ALTURA / 3])

    def game_tela(self):
        # Atualiza a tela do jogo
        self.display.fill(BLACK)
        self.funcao_comida_tela()
        self.funcao_cobra_tela(self.snake_lista)
        self.funcao_pontos_tela(self.pontos, 5, 5)

        pygame.display.update()
        self.clock.tick(VEL_GAME)  # Controla a velocidade de atualização da tela

    def game_loop(self):
        self.reseta_game()

        while self.game_open:
            while not self.vivo:
                self.vida_pos_morte()

            for event in pygame.event.get():
                self.botoes_usuarios(event)

            self.direcao = self.input_direcao
            self.movimento_cobra()
            self.come_food()
            self.funcao_aumenta_tam_cobra()

            if self.funcaoColisao(self.pos_x, self.pos_y):
                self.vivo = False

            self.game_tela()

        pygame.quit()
        quit()


if __name__ == '__main__':
    snake = JogoDaCobrinha()
    snake.game_loop()
