import numpy as np
import pygame
import tensorflow as tf

from constantes_game import *
from direcao import Direcao
from deep_ambiente_treinamento import DeepQTreinamento
from base_pygame import BaseGame


class DeepQGame(BaseGame, DeepQTreinamento):
    def __init__(self):
        super().__init__()
        pygame.display.set_caption('Jogo da cobrinha com Deep Q Learning')

    def funcao_tela_jogo(self, geracao):
        """
        Desenha o estado atual do jogo na tela.

        Args:
            geracao (int): Número da geração atual.
        """
        self.display.fill(BLACK)
        self.funcao_comida_tela()
        self.funcao_cobra_tela(self.snake_lista)
        self.funcao_pontos_tela(self.pontos, 5, 30)
        self.funcao_geracao_tela(geracao, 5, 5)

        pygame.display.update()
        self.clock.tick(VEL_GAME)

    def funcao_visualizacao(self, path, geracao, quit_game):
        """
        Executa a visualização do jogo utilizando o modelo de Deep Q Learning treinado.

        Args:
            path (str): Caminho para o diretório onde estão armazenados os modelos treinados.
            geracao (int): Número da geração do modelo a ser carregado.
            quit_game (bool): Indica se o jogo deve ser fechado após a visualização.

        Returns:
            int: Tamanho final da cobra no jogo.
        """
        model = tf.keras.models.load_model(path + f"geracao-{geracao}.model")

        length = self.funcao_tamanho_cobra()
        steps_without_food = 0

        while self.vivo:
            pygame.event.pump()
            state = np.reshape(self.funcao_retorno_estado_snake(), (1, self.state_space))

            act_values = model.predict(state, verbose=0)
            action_index = np.argmax(act_values[0])
            action = Direcao(action_index)
            self.funcao_keyboard_treinamento(action)

            self.movimento_cobra()
            self.come_food()
            self.funcao_aumenta_tam_cobra()

            if self.funcaoColisao(self.pos_x, self.pos_y):
                self.vivo = False

            if self.funcao_tamanho_cobra() != length:
                steps_without_food = 0
                length = self.funcao_tamanho_cobra()
            else:
                steps_without_food += 1

            if steps_without_food == 1000:
                break

            self.funcao_tela_jogo(geracao)

        if quit_game:
            pygame.quit()

        return self.funcao_tamanho_cobra()


if __name__ == '__main__':
    path = "./models/deepq_base_treinamento/"
    deep_q_visualiser = DeepQGame()
    deep_q_visualiser.funcao_visualizacao(path, 6, True)

