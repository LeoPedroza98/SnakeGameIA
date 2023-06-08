import random
from constantes_game import *
from direcao import *

class BaseSnake:
    def __init__(self):
        # Snake
        self.snake_list = []
        self.pos_x = DIS_LARG / 2
        self.pos_y = DIS_ALTURA / 2
        self.direcao = None

        # Cria comida pelo mapa é random
        self.food_x = round(random.randrange(0, DIS_LARG - BLOCK_TAM) / 10.0) * 10.0
        self.food_y = round(random.randrange(0, DIS_ALTURA - BLOCK_TAM) / 10.0) * 10.0
        self.alive = True
        self.score = 0

    def movimento_cobra(self):
        # Verifica a direção atual da cobra e atualiza as coordenadas de acordo
        if self.direcao == Direcao.ESQUERDA:
            self.pos_x += MOV_ESQUERDA
        elif self.direcao == Direcao.DIREITA:
            self.pos_x += MOV_DIREITA
        elif self.direcao == Direcao.CIMA:
            self.pos_y += MOV_CIMA
        elif self.direcao == Direcao.BAIXO:
            self.pos_y += MOVE_BAIXO

        # Cria uma lista contendo as coordenadas atualizadas da cabeça da cobra
        snake_head = [self.pos_x, self.pos_y]

        # Adiciona a cabeça da cobra à lista de posições da cobra
        self.snake_list.append(snake_head)

    def come_comida(self):
        # Verifica se a posição atual da cobra coincide com a posição da comida
        if self.pos_x == self.food_x and self.pos_y == self.food_y:
            # Gera novas coordenadas aleatórias para a comida dentro dos limites da tela
            self.food_x = round(random.randrange(0, DIS_LARG - VEL_MOV) / 10.0) * 10.0
            self.food_y = round(random.randrange(0, DIS_ALTURA - VEL_MOV) / 10.0) * 10.0

            # Aumenta a pontuação em 1 ponto
            self.score += 1

            # Retorna True para indicar que a cobra comeu a comida
            return True

        # Caso contrário, retorna False para indicar que a cobra não comeu a comida
        return False

    def funcao_aumenta_tam_cobra(self):
        # Verifica se o tamanho atual da lista de posições da cobra é maior do que o comprimento desejado
        if len(self.snake_list) > self.funcao_tamanho_cobra():
            # Se for maior, remove a posição mais antiga da cauda da cobra (primeiro elemento da lista)
            del self.snake_list[0]

    def funcao_tamanho_cobra(self):
        # Retorna o comprimento da cobra, que é igual à pontuação atual mais 1
        return self.score + 1

    def funcaoColisao(self, x, y):
        # Verifica se a posição (x, y) está fora dos limites da janela do jogo
        if x >= DIS_LARG or x < 0 or y >= DIS_ALTURA or y < 0:
            return True

        # Verifica se a posição (x, y) está presente em qualquer posição da cobra, exceto a última
        if [x, y] in self.snake_list[:-1]:
            return True
