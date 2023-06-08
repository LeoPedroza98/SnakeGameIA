import random

import pygame

from constantes_game import *
from direcao import Direcao
from base_pygame import BaseGame

class ManualSnake(BaseGame):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption('Snake')

        self.game_open = True
        self.input_direction = None

    def reseta_game(self):
        # Reinicia todas as variáveis e configurações do jogo
        self.game_open = True
        self.alive = True
        self.score = 0

        self.snake_list = []
        self.pos_x = DIS_LARG / 2
        self.pos_y = DIS_ALTURA / 2
        self.input_direction = None
        self.direcao = None

        self.food_x = round(random.randrange(0, DIS_LARG - BLOCK_TAM) / 10.0) * 10.0
        self.food_y = round(random.randrange(0, DIS_ALTURA - BLOCK_TAM) / 10.0) * 10.0

    def botoes_usuarios(self, event):
        # Lida com os eventos de entrada do usuário
        if event.type == pygame.QUIT:
            self.game_open = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.direcao != Direcao.DIREITA:
                self.input_direction = Direcao.ESQUERDA
            elif event.key == pygame.K_RIGHT and self.direcao != Direcao.ESQUERDA:
                self.input_direction = Direcao.DIREITA
            elif event.key == pygame.K_UP and self.direcao != Direcao.BAIXO:
                self.input_direction = Direcao.CIMA
            elif event.key == pygame.K_DOWN and self.direcao != Direcao.CIMA:
                self.input_direction = Direcao.BAIXO

    def vida_pos_morte(self):
        # Mostra a tela de derrota quando o jogador perde
        self.display.fill(BLACK)
        self.mesangem_tela("Vish você morreu! Aperte Q para finalizar o jogo ou C para resetar o game", WHITE)
        self.funcao_pontos_tela(self.score, 5, 5)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_open = False
                    self.alive = True
                if event.key == pygame.K_c:
                    self.game_loop()

    def mesangem_tela(self, msg, color):
        # Exibe uma mensagem na tela
        font_style = pygame.font.SysFont("arial", 18)
        message = font_style.render(msg, True, color)
        self.display.blit(message, [10, DIS_ALTURA / 3])

    def game_tela(self):
        # Desenha o estado atual do jogo na tela
        self.display.fill(BLACK)
        self.funcao_comida_tela()
        self.funcao_cobra_tela(self.snake_list)
        self.funcao_pontos_tela(self.score, 5, 5)
        pygame.display.update()
        self.clock.tick(VEL_GAME)

    def game_loop(self):
        # Loop principal do jogo
        self.reseta_game()

        while self.game_open:
            while not self.alive:
                self.vida_pos_morte()

            for event in pygame.event.get():
                self.botoes_usuarios(event)

            self.direcao = self.input_direction
            self.movimento_cobra()
            self.come_comida()
            self.funcao_aumenta_tam_cobra()

            if self.funcaoColisao(self.pos_x, self.pos_y):
                self.alive = False

            self.game_tela()

        pygame.quit()
        quit()

if __name__ == '__main__':
    # Cria uma instância da classe ManualSnake e inicia o jogo
    snake = ManualSnake()
    snake.game_loop()