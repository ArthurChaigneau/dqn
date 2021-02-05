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
    ACTION_SPACE_SIZE = 2
    OBSERVATION_SIZE = 6

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

        return self.create_observation()

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

    def create_observation(self) -> list:
        """
        Créer l'état dans lequel se trouve le serpent
        :return: Un np.array contenant les info : dist par rapport au mur, dist par rapport à nourriture, dist
        par rapport à tail, bool si je suis sur moi-même
        """
        cur_observ = [0 for _ in range(self.OBSERVATION_SIZE)]

        # En haut à droite / En bas à droite
        pos_plane_right = [(self.plane.position[0][0] + self.plane.WIDTH_SPRITE, self.plane.position[0][1]),
                           self.plane.position[1]]

        # Distance avec le haut de l'écran
        cur_observ[0] = euclidean_distance(pos_plane_right[0], (pos_plane_right[0][0], 0))

        # Distance avec le bas de l'écran
        cur_observ[1] = euclidean_distance(pos_plane_right[1], (pos_plane_right[1][0], self.height))

        # On trouve quel est le prochain groupe d'oiseaux (s'il y a un groupe d'oiseaux)
        if len(self.list_group_birds):

            idx_next_group = 0

            while self.list_group_birds[idx_next_group].birds[0].position[1][0] < self.plane.position[0][0]:
                idx_next_group += 1

            # En haut à gauche / En bas à gauche
            pos_next_hole = [(self.list_group_birds[idx_next_group].birds[0].position[0][0],
                              self.list_group_birds[idx_next_group].posYHole),
                             (self.list_group_birds[idx_next_group].birds[0].position[0][0],
                              self.list_group_birds[idx_next_group].posYHole +
                              self.list_group_birds[idx_next_group].LENGTH_HOLE)]

            # Distance avec le coin gauche du haut du trou dans le prochain groupe d'oiseaux
            cur_observ[2] = euclidean_distance(pos_plane_right[0], pos_next_hole[0])

            # Distance avec le coin gauche du bas du trou dans le prochain groupe d'oiseaux
            cur_observ[3] = euclidean_distance(pos_plane_right[1], pos_next_hole[1])

            # Est-ce que l'avion est au dessus du trou
            cur_observ[4] = int(pos_plane_right[0][1] < pos_next_hole[0][1])

            # Est-ce que l'avion est en train de passer à travers le passage entre les oiseaux
            xpos_end_hole = self.list_group_birds[idx_next_group].birds[0].position[1][0]
            cur_observ[5] = int(pos_next_hole[0][0] <= pos_plane_right[0][0] <= xpos_end_hole or
                                pos_next_hole[0][0] <= self.plane.position[0][0] <= xpos_end_hole)

        else:

            # Distance avec le bord droit de l'écran par défaut
            cur_observ[2] = euclidean_distance(pos_plane_right[0], (self.width, pos_plane_right[0][1]))

            # Distance avec le bord droit de l'écran par défaut
            cur_observ[3] = euclidean_distance(pos_plane_right[1], (self.width, pos_plane_right[1][1]))

        return cur_observ

    def step(self, action: int):
        """
        Effectue une action avec l'avion de chasse
        :param action: Int 0 <= x <= 1
        :return: Un tuple avec : un nouvel état, une réc, si la partie est finie ou non
        """

        # Action de l'avion
        self.episode_step += 1
        self.plane.action(action)
        self.distance += 1

        # Spawn éventuel des oiseaux
        self.spawn_birds()

        # Déplacement des oiseaux
        self.move_groups_birds()

        # Nouvel état
        new_obs = self.create_observation()

        # Récompenses / Pénalités
        if self.plane_out_of_screen():
            reward = - self.OUT_OF_SCREEN_PENALTY
        elif self.plane_collides_with_birds():
            reward = - self.COLLISION_WITH_BIRDS_PENALTY
        else:
            reward = - self.MOVE_PENALTY

        # état terminal ou non
        done = False

        if reward in (-self.OUT_OF_SCREEN_PENALTY, -self.COLLISION_WITH_BIRDS_PENALTY):
            done = True

        return new_obs, reward, done



