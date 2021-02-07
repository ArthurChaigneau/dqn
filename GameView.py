import pygame
import Game
import PlaneView
import CloudsView
import GroupOfBirdsView


class GameView:
    """
    Classe gérant les graphiques
    """

    BACKGROUND_COLOR = '#0080FF'

    def __init__(self, height: int, width: int, game: Game.Game):
        """
        Init de la classe
        :param width: Largeur
        :param height: Hauteur
        :param env: Env de la partie
        """

        # Largeur de la fenêtre
        self.width = width

        # Hauteur de la fenêtre
        self.height = height

        # Classe s'occupant de jouer
        self.game = game

        # Environnement de la partie
        self.env = game.env

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("PlaneVsBirds")
        pygame.key.set_repeat(1, 100)

        # Fenêtre principale
        self.window = pygame.display.set_mode((self.width, self.height))

        # Graphismes de l'avion
        self.planeview = PlaneView.PlaneView(self.window, self.env.plane)

        # Graphismes des nuages
        self.cloudsview = CloudsView.CloudsView(self.height, self.width, self.window)

        # Graphismes des oiseaux
        self.groups_birds_view = [GroupOfBirdsView.GroupOfBirdsView(self.window, g) for g in self.env.list_group_birds]

        # Background de la fenêtre
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(pygame.Color(self.BACKGROUND_COLOR))

        # Booléen de la boucle principale
        self.running = True

    def display_bg(self) -> None:
        """Affichage du background"""

        self.window.blit(self.background, (0, 0))

    def update_groups_birds(self) -> None:
        """
        Met à jour les groupes des oiseaux
        :return: None
        """

        groups_onscreen = []

        # On ne garde que les groupes à l'écran
        for group_view in self.groups_birds_view:
            if group_view.on_screen:
                groups_onscreen.append(group_view)

        # On ajoute éventuellement une nouvelle view pour les nouveaux groupes d'oiseaux
        for group in self.env.list_group_birds:
            if not any(group is g.group_birds for g in groups_onscreen):
                groups_onscreen.append(GroupOfBirdsView.GroupOfBirdsView(self.window, group))

        self.groups_birds_view = groups_onscreen

    def reset_game(self) -> None:
        """
        Réinitialise les objets en rapport avec l'affichage du jeu
        :return: None
        """

        self.planeview = PlaneView.PlaneView(self.window, self.env.plane)

        self.groups_birds_view = [GroupOfBirdsView.GroupOfBirdsView(self.window, g) for g in self.env.list_group_birds]

    def display_groups_birds(self) -> None:
        """
        Affiche les groupes d'oiseaux
        :return: None
        """

        for view in self.groups_birds_view:
            view.display()

    def run(self):
        """Méthode principale de la classe. S'occupe de l'affichage de la partie"""

        clock = pygame.time.Clock()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.game.graphic_test()

            if self.game.restarted:

                self.reset_game()

                self.game.restarted = False

            self.update_groups_birds()

            self.display_bg()

            self.cloudsview.display()

            self.display_groups_birds()

            self.planeview.display()

            self.cloudsview.create_cloud()

            self.cloudsview.update()

            pygame.display.update()
            clock.tick(60)



