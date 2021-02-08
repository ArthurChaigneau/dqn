import GroupOfBirds
import BirdView
import pygame


class GroupOfBirdsView:
    """
    Classe s'occupant de la partie graphique de l'avion dans une partie
    """

    def __init__(self, window, g: GroupOfBirds.GroupOfBirds):
        """
        Initialisation de la classe
        :param window: La fenêtre pygame principale sur laquelle afficher l'avion
        :param b: Un objet "GroupOfBirds"
        """

        self.window = window

        self.group_birds = g

        self.birds_view = [BirdView.BirdView(self.window, bird) for bird in self.group_birds.birds]

        self.on_screen = True

    def display(self) -> None:
        """
        Affiche l'avion sur la fenêtre pygame
        :return: None
        """

        for bird_view in self.birds_view:
            bird_view.display()

        self.on_screen = self.group_birds.on_screen


