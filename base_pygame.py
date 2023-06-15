import pygame

from constantes_game import *
from base_game import BaseSnake


class BaseGame(BaseSnake):
    def __init__(self):
        super().__init__()
        pygame.init()

        # Inicializa o relógio do Pygame
        self.clock = pygame.time.Clock()

        # Cria uma janela de exibição com as dimensões definidas em constantes_game
        self.display = pygame.display.set_mode((DIS_LARG, DIS_ALTURA))

        # Cria uma fonte para exibir a pontuação na tela
        self.ponto_font = pygame.font.SysFont("arial", 25)

    def funcao_pontos_tela(self, pontos, x, y):
        # Renderiza o texto da pontuação com a fonte definida
        value = self.ponto_font.render(f"Pontos: {pontos}", True, WHITE)

        # Exibe o texto da pontuação na posição (x, y) na tela
        self.display.blit(value, [x, y])

    def funcao_geracao_tela(self, geracao, x, y):
        # Renderiza o texto da geração com a fonte definida
        value = self.ponto_font.render(f"Geração: {geracao}", True, WHITE)

        # Exibe o texto da geração na posição (x, y) na tela
        self.display.blit(value, [x, y])

    def funcao_cobra_tela(self, snake_lista):
        # Desenha cada segmento da cobra na tela usando a cor verde
        for x in snake_lista:
            pygame.draw.rect(self.display, GREEN, [x[0], x[1], BLOCK_TAM, BLOCK_TAM])

    def funcao_comida_tela(self):
        # Desenha a comida na tela usando a cor vermelha nas coordenadas (food_x, food_y)
        pygame.draw.rect(self.display, RED, [self.food_x, self.food_y, BLOCK_TAM, BLOCK_TAM])
