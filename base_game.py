import random
from constantes_game import *
from direcao import Direcao

class BaseSnake:
    def __init__(self):
        # Lista que representa o corpo da cobra
        self.snake_lista = []
        # Posição inicial da cabeça da cobra no eixo X
        self.pos_x = DIS_LARG / 2
        # Posição inicial da cabeça da cobra no eixo Y
        self.pos_y = DIS_ALTURA / 2
        # Direção inicial da cobra (None indica que a direção ainda não foi definida)
        self.direcao = None
        # Lista para armazenar as posições da comida ao longo do jogo
        self.pontos_game = []

        # Criar a primeira comida
        self.food_x = round(random.randrange(0, DIS_LARG - BLOCK_TAM) / 10.0) * 10.0
        self.food_y = round(random.randrange(0, DIS_ALTURA - BLOCK_TAM) / 10.0) * 10.0

        # Estado do jogo
        self.vivo = True
        self.pontos = 0

    def movimento_cobra(self):
        # Atualiza a posição da cobra com base na direção atual
        if self.direcao == Direcao.ESQUERDA:
            self.pos_x += MOV_ESQUERDA
        elif self.direcao == Direcao.DIREITA:
            self.pos_x += MOV_DIREITA
        elif self.direcao == Direcao.CIMA:
            self.pos_y += MOV_CIMA
        elif self.direcao == Direcao.BAIXO:
            self.pos_y += MOVE_BAIXO

        # Cria uma nova cabeça para a cobra na posição atualizada
        snake_head = [self.pos_x, self.pos_y]
        # Adiciona a nova cabeça à lista da cobra
        self.snake_lista.append(snake_head)

    def come_food(self):
        # Verifica se a cobra comeu a comida
        if self.pos_x == self.food_x and self.pos_y == self.food_y:
            # Gera uma nova posição para a comida aleatoriamente
            self.food_x = round(random.randrange(0, DIS_LARG - VEL_MOV) / 10.0) * 10.0
            self.food_y = round(random.randrange(0, DIS_ALTURA - VEL_MOV) / 10.0) * 10.0
            # Incrementa a pontuação do jogador
            self.pontos += 1
            return True
        return False

    def contabiliza_pontos(self, pontos_game):
        # Adiciona os pontos do jogo atual à pontuação total do jogador
        self.pontos += pontos_game

    def funcao_aumenta_tam_cobra(self):
        # Verifica se a cobra precisa crescer (seu tamanho é maior do que a pontuação atual)
        if len(self.snake_lista) > self.funcao_tamanho_cobra():
            # Remove o segmento mais antigo da cauda da cobra
            del self.snake_lista[0]

    def funcao_tamanho_cobra(self):
        # Retorna o tamanho da cobra (pontuação atual + 1, pois a cabeça também é contada)
        return self.pontos + 1

    def funcaoColisao(self, x, y):
        # Verifica se houve colisão da cobra com as bordas do jogo ou com o próprio corpo
        if x >= DIS_LARG or x < 0 or y >= DIS_ALTURA or y < 0:
            return True

        if [x, y] in self.snake_lista[:-1]:
            return True
