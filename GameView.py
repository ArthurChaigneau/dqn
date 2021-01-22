import pygame
import Env
import PlaneView
import CloudsView


class GameView:
    """
    Classe gérant les graphiques
    """

    BACKGROUND_COLOR = '#0080FF'

    def __init__(self, width: int, height: int, env: Env.Env):
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

        # Environnement de la partie
        self.env = env

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

        # Background de la fenêtre
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill(pygame.Color(self.BACKGROUND_COLOR))

        # Booléen de la boucle principale
        self.running = True

    def display_bg(self) -> None:
        """Affichage du background"""

        self.window.blit(self.background, (0, 0))

    def run(self):
        """Méthode principale de la classe. S'occupe de l'affichage de la partie"""

        clock = pygame.time.Clock()

        action = 1

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = 0
                elif event.type == pygame.MOUSEBUTTONUP:
                    action = 1

            self.env.plane.action(action)

            self.display_bg()

            self.cloudsview.display()

            self.planeview.display()

            self.cloudsview.create_cloud()

            self.cloudsview.update()

            pygame.display.update()
            clock.tick(60)



