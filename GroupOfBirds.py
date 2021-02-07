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

        self.on_screen = True

        self.posYHole = choice(range(0, self.env.height - self.LENGTH_HOLE, self.LENGTH_HOLE))  # Choix du trou aléatoirement

        # Liste contenant toutes les positions y disponibles pour les oiseaux
        allThePositionPossible = [i for i in range(self.posYHole - self.HEIGHT_BIRD, - self.HEIGHT_BIRD // 2, - self.HEIGHT_BIRD)] + \
                                 [i for i in range(
                                     self.posYHole + self.LENGTH_HOLE + 1, self.env.height, self.HEIGHT_BIRD)]

        for i in allThePositionPossible:

            if not (self.posYHole <= i <= self.posYHole + self.LENGTH_HOLE):
                self.birds.append(Bird(self.env, self.env.width + self.WIDTH_BIRD, i, self.speed))

    def move(self) -> bool:
        """
        Fait avancer tous les oiseaux
        :return: Retourne vrai si les oiseaux sont toujours sur l'écran près avoir avancé, faux sinon
        """

        for bird in self.birds:
            bird.move()

            if bird.position[0][0] <= - self.WIDTH_BIRD:
                self.on_screen = False

        return self.on_screen

