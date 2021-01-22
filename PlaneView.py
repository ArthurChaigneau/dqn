import Plane
import pygame


class PlaneView:
    """
    Classe s'occupant de la partie graphique de l'avion dans une partie
    """

    def __init__(self, window, plane: Plane.Plane):
        """
        Initialisation de la classe
        :param window: La fenêtre pygame principale sur laquelle afficher l'avion
        :param plane: Un objet "Plane"
        """

        self.window = window

        self.plane = plane

        self.sprites = {
            "CLIMB" : pygame.image.load("images/plane2.png"),
            "FALL" : pygame.image.load("images/plane3.png"),
            "STABLE" : pygame.image.load("images/plane1.png")
        }

    def display(self) -> None:
        """
        Affiche l'avion sur la fenêtre pygame
        :return: None
        """

        if self.plane.speedy < 0:
            image = self.sprites['CLIMB']
        elif self.plane.speedy > 0:
            image = self.sprites['FALL']
        else:
            image = self.sprites['STABLE']

        self.window.blit(image, (self.plane.position[0][0], self.plane.position[0][1]))

