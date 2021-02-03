import numpy as np
import Plane
import GroupOfBirds


class Env:
    """
    Environnement du jeu
    """

    ITER_SPAWN_BIRDS = 100
    SPEED_BIRDS = 1

    def __init__(self, height, width):
        """
        Init
        :param height: Hauteur de la fenêtre
        :param width: Largeur de la fenêtre
        """

        self.height = height

        self.width = width

        self.reset()

    def reset(self):
        """
        Remet l'env à 0 et renvoie l'observ de l'état init
        :return: l'observ de l'étant init
        """

        self.distance = 0

        self.plane = Plane.Plane(self)

        self.list_group_birds = []

        # Nombre d'épisodes
        self.episode_step = 0

    def spawn_birds(self) -> None:
        """
        Fait apparaitre des groupes d'oiseaux
        :return: None
        """

        if not (self.episode_step % self.ITER_SPAWN_BIRDS):
            self.list_group_birds.append(GroupOfBirds.GroupOfBirds(self, self.SPEED_BIRDS))

    def step(self, action: int):
        """
        Effectue une action avec l'avion de chasse
        :param action: Int 0 <= x <= 1
        :return: Un tuple avec : un nouvel état, une réc, si la partie est finie ou non
        """

        # Pos avant de bouger
        plane_old_pos = tuple(self.plane.position)

        # Action de l'avion
        self.episode_step += 1
        self.plane.action(action)

        # Spawn éventuel des oiseaux
        self.spawn_birds()

        # Déplacement des oiseaux
        for group in self.list_group_birds:
            group.move()





