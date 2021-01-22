import pygame
import random


class CloudsView:
    """
    Classe s'occupant d'afficher les nuages en fond
    """

    MAX_N_CLOUDS = 5
    HEIGHT_SPRITE = 189
    WIDTH_SPRITE = 200
    INC_SPEED = 5

    def __init__(self, height: int, width: int, window):
        """
        Initialisation de la classe
        :param height: Hauteur de la fenêtre pygame
        :param width: Largeur de la fenêtre pygame
        :param window: La fenêtre pygame principale sur laquelle afficher l'avion
        """

        self.height = height

        self.width = width

        self.window = window

        # Sprite pour les nuages
        self.cloud_sprite = pygame.image.load('images/cloud.png')

        # Les positions des nuages sur l'écran
        # Maximum 5 positions ( car 5 nuages au max)
        self.clouds_pos = []

    def create_cloud(self) -> None:
        """
        Ajoute éventuellement un nuage sur l'écran
        :return: None
        """

        if len(self.clouds_pos) < self.MAX_N_CLOUDS:

            if random.random() > 0.99:

                self.clouds_pos.append((self.width, random.randint(0, self.height - self.HEIGHT_SPRITE)))

    def update(self) -> None:
        """
        Met à jour les coordonnées des nuages sur la fenêtre principale
        :return: None
        """

        clouds2keep = []

        for pos in self.clouds_pos:

            if pos[0] + self.WIDTH_SPRITE > 0:

                clouds2keep.append((pos[0] - self.INC_SPEED, pos[1]))

        self.clouds_pos = clouds2keep

    def display(self) -> None:
        """
        Affiche l'avion sur la fenêtre pygame
        :return: None
        """

        for pos in self.clouds_pos:

            self.window.blit(self.cloud_sprite, (pos[0], pos[1]))
