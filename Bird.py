class Bird:
    """
    Les obstacles à eviter
    """

    def __init__(self, posXInit, posYInit, speed):
        """
        Constructeur
        :param posXInit: La position X lors de sa création
        :param posYInit: La position Y lors de sa création
        :param speed: La vitesse de l'oiseau selon l'axe x
        """
        self.posX = posXInit
        self.posY = posYInit
        self.speed = speed

    def move(self):
        """
        Déplace l'oiseau en position x selon sa vitesse
        """

