from direcao import *
from base_game import *

class BaseTreinamento(BaseSnake):
    def __int__(self):
        super().__int__()

    def funcao_keyboard_treinamento(self,keyboard):
        if keyboard != Direcao.ESQUERDA and keyboard != Direcao.DIREITA and keyboard != Direcao.CIMA and keyboard != Direcao.BAIXO:
            raise  Exception('Erro')
        if keyboard == Direcao.ESQUERDA and self.direcao != Direcao.DIREITA:
            self.direcao = Direcao.ESQUERDA
        elif keyboard == Direcao.DIREITA and self.direcao != Direcao.ESQUERDA:
            self.direcao = Direcao.DIREITA
        elif keyboard == Direcao.CIMA and self.direcao != Direcao.BAIXO:
            self.direcao = Direcao.CIMA
        elif keyboard == Direcao.BAIXO and self.direcao != Direcao.CIMA:
            self.direcao = Direcao.BAIXO

    def funcao_colisao_treinamento(self, x, y):
        if self.colisao(x, y):
            return False
        return True