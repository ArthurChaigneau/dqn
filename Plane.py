import numpy as np
import Env


class Plane:
    """
    Avion de chasse
    """

    HEIGHT_SPRITE = 90
    WIDTH_SPRITE = 85
    OFFSET_START = 100
    HORIZONTAL_OFFSET = 50
    MAX_SPEED_FALL = 5
    INC_SPEED_FALL = 1
    INC_SPEED_CLIMB = 1

    def __init__(self, env: Env.Env):
        """
        Initialisation de la classe
        """

        # Environnement global
        self.env = env

        # Coin en haut à gauche / Coin en bas à droite
        self.position = ([self.HORIZONTAL_OFFSET, self.env.height // 2 - self.OFFSET_START],
                         [self.HORIZONTAL_OFFSET + self.WIDTH_SPRITE,
                          self.env.height // 2 - self.OFFSET_START + self.HEIGHT_SPRITE])

        # Vitesse à laquelle l'avion tombe
        self.speedy = 0

    def move(self, action: str) -> None:
        """
        Fait bouger l'avion soit vers le haut, soit vers le bas
        :param action: une action entre "UP", "NOP" (no operation)
        :return: None
        """

        if action == "UP":
            self.speedy -= self.INC_SPEED_CLIMB
        else:
            self.speedy = min(self.MAX_SPEED_FALL, self.speedy + self.INC_SPEED_FALL)

        if self.position[1][1] + self.speedy < 800:
            self.position[0][1], self.position[1][1] = self.position[0][1] + self.speedy, self.position[1][1] + self.speedy

    def action(self, choice: int) -> None:
        """
        Effectue une action
        :param choice: 0 -> UP, 1 -> NOP
        :return: None
        """
        action = "UP" if not choice else "NOP"

        self.move(action)







