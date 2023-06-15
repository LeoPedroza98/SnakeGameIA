from direcao import Direcao
from base_game import BaseSnake


class BaseTreinamento(BaseSnake):
    def __init__(self):
        super().__init__()

    def funcao_keyboard_treinamento(self, action):
        """
        Define a ação do teclado para o treinamento do jogo da serpente.

        Args:
            action (Direcao): Ação a ser executada (ESQUERDA, DIREITA, CIMA, BAIXO).

        Raises:
            Exception: Se a ação for inválida.

        """
        if action != Direcao.ESQUERDA and action != Direcao.DIREITA and action != Direcao.CIMA and action != Direcao.BAIXO:
            raise Exception('Invalid action')

        # Atualiza a direção da serpente com base na ação recebida
        if action == Direcao.ESQUERDA and self.direcao != Direcao.DIREITA:
            self.direcao = Direcao.ESQUERDA
        elif action == Direcao.DIREITA and self.direcao != Direcao.ESQUERDA:
            self.direcao = Direcao.DIREITA
        elif action == Direcao.CIMA and self.direcao != Direcao.BAIXO:
            self.direcao = Direcao.CIMA
        elif action == Direcao.BAIXO and self.direcao != Direcao.CIMA:
            self.direcao = Direcao.BAIXO

    def funcao_colisao_treinamento(self, x, y):
        """
        Verifica se ocorreu uma colisão durante o treinamento do jogo da serpente.

        Args:
            x (int): Coordenada x a ser verificada.
            y (int): Coordenada y a ser verificada.

        Returns:
            bool: True se não houver colisão, False caso contrário.

        """
        # Verifica se houve colisão chamando a função de colisão da classe pai (BaseSnake)
        if self.funcaoColisao(x, y):
            return False
        return True
