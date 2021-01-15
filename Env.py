import numpy as np


class Env:
    """
    Environnement du jeu
    """

    def __init__(self, height, width):
        """
        Init
        :param height: Hauteur de la fenêtre
        :param width: Largeur de la fenêtre
        """

        self.height = height

        self.width = width

    def reset(self):
        """
        Remet l'env à 0 et renvoie l'observ de l'état init
        :return: l'observ de l'étant init
        """

        self.distance = 0

        self.plane = None

        self.birds = []