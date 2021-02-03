from random import choice
from Bird import Bird

class GroupOfBirds:
    """
    Créer une ligne d'oiseau (obstacles)
    Le principe c'est que aléatoirement on va choisir un trou sur la hauteur de l'écran, on remplit la ligne verticale
    d'oiseau sauf au niveau du trou
    """
    def __init__(self, env, speed):
        self.birds = []
        self.env = env
        self.speed = speed

        self.posYHole = choice(range(0, self.env.height-90))%90 #Choix du trou aléatoirement
        allThePositionPossible = [i%90 for i in range(0, self.env.height)] #Liste contenant toutes les positions y disponibles pour les oiseaux

        for i in allThePositionPossible:
            if i != self.posYHole:
                self.birds.append(Bird(self.env, self.env.width-85, i, self.speed))

