import numpy as np
import Plane
import GroupOfBirds


def euclidean_distance(pos1, pos2):
    """
    Calcule la distance euclidienne entre deux positions
    :param pos1: Un premier tuple (x, y)
    :param pos2: Un deuxième tuple (x, y)
    :return: la distance euclidienne
    """

    return np.sqrt(np.power(pos1[0] - pos2[0], 2) + np.power(pos1[1] - pos2[1], 2))


class Env:
    """
    Environnement du jeu
    """

    ITER_SPAWN_BIRDS = 150
    SPEED_BIRDS = 1
    MARGIN_Y = 30

    # REWARD / PENALITIES
    OUT_OF_SCREEN_PENALTY = 300
    COLLISION_WITH_BIRDS_PENALTY = 150
    MOVE_PENALTY = 1

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

    def move_groups_birds(self) -> None:
        """
        Fait bouger, si possible les groupes d'oiseaux
        :return: None
        """
        groups_onscreen = []

        for group in self.list_group_birds:
            if group.move():
                groups_onscreen.append(group)

        self.list_group_birds = groups_onscreen

    def plane_out_of_screen(self) -> bool:
        """
        Regarde si l'avion est en dehors de l'écran (soit trop haut, soit trop bas)
        :return: Vrai si c'est le cas, faux sinon
        """
        return self.plane.position[0][1] < 0 or self.plane.position[1][1] > self.height

    def plane_collides_with_birds(self) -> bool:
        """
        Regarde si l'avion entre en contact avec des oiseaux
        :return: Vrai si c'est le cas, faux sinon
        """

        collision = False

        if len(self.list_group_birds):

            idx_next_group = 0

            while self.list_group_birds[idx_next_group].birds[0].position[1][0] < self.plane.position[0][0]:
                idx_next_group += 1

            # Si l'avion se situe à l'intérieur d'un groupe d'oiseaux sur l'axe horizontal
            if self.plane.position[0][0] < self.list_group_birds[idx_next_group].birds[0].position[0][0] < \
                    self.plane.position[1][0] or self.plane.position[0][0] < \
                    self.list_group_birds[idx_next_group].birds[0].position[0][0] < self.plane.position[1][0]:

                # print("X OK ")

                # On regarde si l'avion est en contact avec un des oiseaux de ce groupe
                for bird in self.list_group_birds[idx_next_group].birds:

                    # print("Bird left : ", bird.position[0][1])
                    # print("Plane left : ", self.plane.position[0][1])
                    # print("Plane right : ", self.plane.position[1][1])
                    # print("Bird right : ", bird.position[1][1])
                    # print()

                    if bird.position[0][1] + self.MARGIN_Y < self.plane.position[0][1] < \
                            bird.position[1][1] - self.MARGIN_Y or bird.position[0][1] + self.MARGIN_Y < \
                            self.plane.position[1][1] < bird.position[1][1] - self.MARGIN_Y:

                        collision = True

                        break

        return collision

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
        self.move_groups_birds()

        # Récompenses / Pénalités
        if self.plane_out_of_screen():
            reward = - self.OUT_OF_SCREEN_PENALTY
        elif self.plane_collides_with_birds():
            reward = - self.COLLISION_WITH_BIRDS_PENALTY
        else :
            reward = - self.MOVE_PENALTY
        
