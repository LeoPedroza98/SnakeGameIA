import pygame
from constantes_game import *
from base_game import *

class BaseGame(BaseSnake):
    def __init__(self):
        super().__init__()
        pygame.init()

        # Inicialização do Pygame
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((DIS_LARG, DIS_ALTURA))
        self.score_font = pygame.font.SysFont("arial", 25)

    def funcao_pontos_tela(self, score, x, y):
        # Desenha a pontuação na tela
        value = self.score_font.render(f"Pontos: {score}", True, WHITE)
        self.display.blit(value, [x, y])

    def funcao_geracao_tela(self, ger, x, y):
        # Desenha o número da geração/época na tela
        value = self.score_font.render(f"Gerações: {ger}", True, WHITE)
        self.display.blit(value, [x, y])

    def funcao_cobra_tela(self, snake_list):
        # Desenha a cobra na tela
        for x in snake_list:
            pygame.draw.rect(self.display, GREEN, [x[0], x[1], BLOCK_TAM, BLOCK_TAM])

    def funcao_comida_tela(self):
        # Desenha a comida na tela
        pygame.draw.rect(self.display, RED, [self.food_x, self.food_y, BLOCK_TAM, BLOCK_TAM])

