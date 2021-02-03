import Bird
import pygame


class BirdView:
    """
    Classe s'occupant de la partie graphique de l'avion dans une partie
    """

    def __init__(self, window, b: Bird.Bird):
        """
        Initialisation de la classe
        :param window: La fenêtre pygame principale sur laquelle afficher l'avion
        :param b: Un objet "Bird"
        """

        self.window = window

        self.bird = b

        self.sprites = {
            "UP": pygame.image.load("images/bird1.png"),
            "DOWN": pygame.image.load("images/bird2.jpg")
        }

        self.wings_up = True

    def display(self) -> None:
        """
        Affiche l'avion sur la fenêtre pygame
        :return: None
        """

        image = self.sprites['UP'] if self.wings_up else self.sprites['DOWN']

        self.wings_up = not self.wings_up

        self.window.blit(image, (self.bird.position[0][0], self.bird.position[0][1]))

