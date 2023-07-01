import gc
import os
import random
from collections import deque

import numpy as np
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from keras.optimizers import Adam

from direcao import Direcao
from deep_ambiente_treinamento import DeepQTreinamento


class DeepQTreinamentoIA:
    def __init__(self):
        # Parâmetros de treinamento
        self.gamma = 0.95  # Fator de desconto para recompensas futuras
        self.epsilon = 1.0  # Taxa de exploração inicial
        self.epsilon_min = 0.01  # Taxa de exploração mínima
        self.epsilon_decay = 0.995  # Decaimento da taxa de exploração após cada episódio
        self.learning_rate = 0.00030  # Taxa de aprendizado do otimizador
        self.batch_size = 512  # Tamanho do lote para o replay buffer

        # Configurações do ambiente
        self.geracoes = 200  # Número de gerações de treinamento
        self.geracoes_tam = 1000

        self.env = DeepQTreinamento()  
        self.memory = deque(maxlen=2000)  # Replay buffer para armazenar transições de estado e memoria
        self.model = self.cria_model_treinamento()  # Rede neural principal
        self.target_model = self.cria_model_treinamento()  # Rede neural alvo

        self.pontos_game = []  # Lista para armazenar os pontos de cada geração
        self.rewards = []  # Lista para armazenar as recompensas de cada geração

    def cria_model_treinamento(self):
        # Criação do modelo de rede neural para treinamento
        model = Sequential()
        model.add(Dense(128, input_dim=self.env.state_space, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(128, activation="relu"))
        model.add(Dense(self.env.action_space, activation='softmax'))
        model.compile(loss="mse", optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def funcao_acao_treinamento(self, state):
        # Escolhe uma ação com base na política epsilon-greedy
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.env.action_space)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])

    def funcao_remember_treinamento(self, estado, action, reward, new_state, done):
        # Armazena uma transição de estado no replay buffer
        self.memory.append((estado, action, reward, new_state, done))

    def funcao_replay(self):
        # Realiza a atualização dos pesos da rede neural usando o replay buffer
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        estados = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        estados = np.squeeze(estados)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma * (np.amax(self.model.predict_on_batch(next_states), axis=1)) * (1 - dones)
        targets_full = self.model.predict_on_batch(estados)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(estados, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def salva_modelo_treinamento(self, model_name, geracao):
        # Salva o modelo de treinamento em determinadas gerações
        should_save = False

        if geracao < 10:
            should_save = True
        elif 10 <= geracao < 200 and geracao % 10 == 0:
            should_save = True
        elif geracao <= 200 and geracao % 50 == 0:
            should_save = True

        if should_save:
            file_name = f'./models/{model_name}/geracao-{geracao}.model'
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            self.model.save(file_name)

    def salva_resultados_modelo(self, model_name):
        # Salva os resultados do treinamento em um arquivo CSV
        df = pd.DataFrame()
        df['Geracao'] = self.geracoes
        df['Pontos'] = self.pontos_game
        df['Reward'] = self.rewards

        df.to_csv(f'resultados/{model_name}.csv')

    def funcao_treinamento_snake(self, model_name):
        # Função principal para o treinamento do jogo Snake
        for geracao in range(1, self.geracoes + 1):
            gc.collect()
            self.env = DeepQTreinamento()

            estado_atual = self.env.funcao_retorno_estado_snake()
            estado_atual = np.reshape(estado_atual, (1, self.env.state_space))
            geracao_reward = 0

            for i in range(self.geracoes_tam):
                action = self.funcao_acao_treinamento(estado_atual)
                new_state, reward, done = self.env.passos_snake(Direcao(action))
                new_state = np.reshape(new_state, (1, self.env.state_space))
                geracao_reward += reward

                self.funcao_remember_treinamento(estado_atual, action, reward, new_state, done)

                estado_atual = new_state

                self.funcao_replay()

                if done:
                    print(f'geração: {geracao}/{self.geracoes}, pontos: {self.env.pontos}, '
                          f'reward: {geracao_reward}, epsilon: {self.epsilon}')
                    self.pontos_game.append(self.env.pontos)
                    self.rewards.append(geracao_reward)

                    self.salva_modelo_treinamento(model_name, geracao)
                    self.salva_resultados_modelo(model_name)
                    break


if __name__ == '__main__':
    name = "deepq_base_treinamento"

    deep_q_trainer = DeepQTreinamentoIA()
    deep_q_trainer.funcao_treinamento_snake(name)
    deep_q_trainer.salva_resultados_modelo(name)
