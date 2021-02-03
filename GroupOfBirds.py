from random import choice
from Bird import Bird


class GroupOfBirds:
    """
    Créer une ligne d'oiseau (obstacles)
    Le principe c'est que aléatoirement on va choisir un trou sur la hauteur de l'écran, on remplit la ligne verticale
    d'oiseau sauf au niveau du trou
    """

    LENGTH_HOLE = 180
    HEIGHT_BIRD = 90
    WIDTH_BIRD = 85

    def __init__(self, env, speed):
        self.birds = []
        self.env = env
        self.speed = speed

        self.posYHole = choice(range(0, self.env.height - self.LENGTH_HOLE, self.LENGTH_HOLE))  # Choix du trou aléatoirement

        allThePositionPossible = [i for i in range(0, self.env.height - self.HEIGHT_BIRD, self.HEIGHT_BIRD)]  # Liste contenant toutes les positions y disponibles pour les oiseaux

        for i in allThePositionPossible:
            if not (self.posYHole < i < self.posYHole + self.LENGTH_HOLE):
                self.birds.append(Bird(self.env, self.env.width + 85, i, self.speed))

    def move(self) -> None:
        """
        Fait avancer tous les oiseaux
        :return: None
        """

        birds_onscreen = []

        for bird in self.birds:
            bird.move()

            if bird.position[0][0] > - self.WIDTH_BIRD:
                birds_onscreen.append(bird)

        self.birds = birds_onscreen

