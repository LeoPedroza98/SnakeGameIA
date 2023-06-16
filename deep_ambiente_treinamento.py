import os
import keras.models
import numpy as np
import pandas as pd

from constantes_game import VEL_MOV
from direcao import Direcao
from base_treinamento_deep import BaseTreinamento

class DeepQTreinamento(BaseTreinamento):
    def __init__(self):
        super().__init__()
        self.state_space = 12
        self.action_space = 4

    def funcao_manhattan(self):
        """
        Calcula a distância Manhattan entre a cabeça da cobra e a comida.
        Retorna a distância Manhattan.
        """
        return abs(self.pos_x - self.food_x) + abs(self.pos_y - self.food_y)

    def passos_snake(self, action):
        """
        Executa um passo do jogo Snake.
        Recebe uma ação como entrada e atualiza o estado do jogo de acordo com a ação escolhida.
        Retorna o próximo estado, a recompensa e se o jogo terminou.
        """
        prev_distancia = self.funcao_manhattan()
        reward = -1
        done = False

        self.funcao_keyboard_treinamento(action)

        self.movimento_cobra()

        distancia = self.funcao_manhattan()
        if distancia < prev_distancia:
            reward = 1

        if self.come_food():
            reward = 10
        self.funcao_aumenta_tam_cobra()

        if self.funcaoColisao(self.pos_x, self.pos_y):
            self.vivo = False
            done = True
            reward = -100

        return self.funcao_retorno_estado_snake(), reward, done

    def funcao_retorno_estado_snake(self):
        """
        Retorna o estado atual do jogo Snake como uma lista de valores binários.
        Cada valor binário indica uma característica do estado do jogo.
        """
        snake_head_x, snake_head_y = self.pos_x, self.pos_y

        state = [
            int(self.direcao == Direcao.ESQUERDA),
            int(self.direcao == Direcao.DIREITA),
            int(self.direcao == Direcao.CIMA),
            int(self.direcao == Direcao.BAIXO),
            int(self.funcao_colisao_treinamento(snake_head_x + VEL_MOV, snake_head_y)),
            int(self.funcao_colisao_treinamento(snake_head_x - VEL_MOV, snake_head_y)),
            int(self.funcao_colisao_treinamento(snake_head_x, snake_head_y + VEL_MOV)),
            int(self.funcao_colisao_treinamento(snake_head_x, snake_head_y - VEL_MOV)),
            int(self.food_x > snake_head_x),
            int(self.food_x < snake_head_x),
            int(self.food_y < snake_head_y),
            int(self.food_y > snake_head_y),
        ]

        return state

    def play(self, model):
        """
        Executa o jogo Snake usando o modelo treinado.
        Retorna o tamanho final da cobra.
        """
        tam = self.funcao_tamanho_cobra()
        passos_sem_comida = 0

        while self.vivo:
            state = self.funcao_retorno_estado_snake()
            state = np.reshape(state, (1, self.state_space))

            action_index = np.argmax(model.predict(state, verbose=0)[0])
            action = Direcao(action_index)
            self.passos_snake(action)

            if self.funcao_tamanho_cobra() != tam:
                passos_sem_comida = 0
                tam = self.funcao_tamanho_cobra()
            else:
                passos_sem_comida += 1

            if passos_sem_comida == 200:
                break

        return self.funcao_tamanho_cobra()


if __name__ == '__main__':
    directory = './models/deepq_base_treinamento'
    models = os.listdir(directory)

    scores = []

    for model_count in range(1, 101):
        if model_count > 10 and model_count % 10 != 0:
            continue

        model = keras.models.load_model(f"{directory}/geracao-{model_count}.model")

        env = DeepQTreinamento()
        ponto = env.play(model)
        scores.append([model_count, ponto])
        print(f"Pontos do modelo {model_count}: {ponto}")

    df = pd.DataFrame(data=scores)
    df.to_csv("base_deepq_results")

