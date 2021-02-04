class Bird:
    """
    Les obstacles à eviter
    """

    MAX_SPEED = 3

    def __init__(self, env, posXInit, posYInit, speed):
        """
        Constructeur
        :param env: l'environnement du jeu
        :param posXInit: La position X lors de sa création
        :param posYInit: La position Y lors de sa création
        :param speed: La vitesse de l'oiseau selon l'axe x
        """
        self.env = env
        self.position = ([posXInit, posYInit], [posXInit + 90, posYInit + 85])
        self.speed = min(speed, self.MAX_SPEED)  # Au maximum l'oiseau pourra se déplacer d'un 10e de la largeur de l'écran par frame

    def move(self):
        """
        Déplace l'oiseau en position x selon sa vitesse
        """
        self.position[0][0] -= self.speedFormule()  # Postion x du point haut gauche (mise à jour)
        self.position[1][0] -= self.speedFormule()  # Position x du point bas droite (mise à jour)

    def speedFormule(self):
        """
        Retourne le déplacement en x selon la vitesse indiqué
        :return: le déplacement en x selon la vitesse indiqué
        """
        return self.env.width/(500 - self.speed)
    