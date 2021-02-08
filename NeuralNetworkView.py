import pygame
import math


class NeuronView:
    """
    Graphiques pour d'un neurone
    """

    WIDTH_SPRITE = 23
    HEIGHT_SPRITE = 20

    WIDTH_LINE = 1

    def __init__(self, window, pos: tuple):
        """
        Initialisation de la classe
        :param window: La fenêtre sur laquelle afficher le neurone
        :param pos: La position sur la fenêtre où afficher le neurone
        """

        self.window = window

        # Sprite pour le neurone
        self.neuron_sprite = pygame.image.load('images/neuron.png')

        self.pos = pos

        # Centre du neurone
        self.center = (self.pos[0] + math.ceil(self.WIDTH_SPRITE // 2),
                       self.pos[1] + math.ceil(self.HEIGHT_SPRITE // 2))

        self.activated = False

    def connect_to_neuron(self, neuron) -> None:
        """
        Connecte le neurone actuel à un autre neurone
        :param neuron: Un autre neurone
        :return: None
        """
        if self.activated and neuron.activated:
            pygame.draw.line(self.window, pygame.Color('#000000'), self.center, neuron.center, self.WIDTH_LINE)

    def display(self) -> None:
        """
        Méthode affichant le neurone
        :return: None
        """

        if self.activated:
            self.window.blit(self.neuron_sprite, self.pos)


class LayerView:
    """
    Graphiques pour une couche de neurones
    """

    def __init__(self, window, pos: tuple, n_neuron: int):
        """
        Initialisation de la classe
        :param window: La fenêtre sur laquelle afficher la couche de neurones
        :param pos: Les coordonnées du neurone le plus haut (coin en haut à gauche)
        :param n_neuron: Le nombre de neurones dans cette couche
        """

        self.window = window

        self.pos = pos

        self.neurons = [NeuronView(self.window, (pos[0], pos[1] + i * NeuronView.HEIGHT_SPRITE))
                        for i in range(n_neuron)]

        self.hidden_layer_activation = lambda l: [(ele > 0) for ele in l]

        self.last_layer_activation = lambda l: [(ele == max(l)) for ele in l]

    def update_neurons(self, res_layer: list, output_layer=False) -> None:
        """
        Met à jour les neurones à afficher
        :param res_layer: Les résultats de la couche dans une liste
        :param output_layer: Param pour indiquer qu'il s'agit de la dernière couche du réseau de neurones
        :return: None
        """

        assert len(self.neurons) == len(res_layer), "Prob de taille entre les listes au niveau des paramètres"

        if output_layer:
            list_activation = self.last_layer_activation(res_layer)
        else:
            list_activation = self.hidden_layer_activation(res_layer)

        assert len(list_activation) == len(self.neurons), "Prob de taille entre les listes au niveau des variables"

        for i in range(len(list_activation)):

            self.neurons[i].activated = list_activation[i]

    def connect_to_previous_layer(self, prev_layer):
        """
        Connecte le layer actuel à la précédente couche
        :param prev_layer: Layer précédent
        :return: None
        """

        for my_neuron in self.neurons:

            for prev_layer_neuron in prev_layer.neurons:

                my_neuron.connect_to_neuron(prev_layer_neuron)

    def display(self) -> None:
        """
        Affiche les neurones de sa couche
        :return: None
        """

        for n in self.neurons:

            n.display()


class NeuralNetworkView:
    """
    Graphiques pour un réseau de neurones
    """

    DISTANCE_BTW_LAYERS = 20

    def __init__(self, window, pos: tuple, layers: list):
        """
        Initialisation de la classe
        :param window: La fenêtre sur laquelle afficher le réseau de neurones
        :param pos: Les coordonnées à partir desquelles on commence à afficher le réseau de neurones
        :param layers: Une liste contenant à chaque fois le nb de neurones par couche
        """

        self.window = window

        self.pos = pos

        self.layers = layers

        max_n_layers = max(layers)

        lenght_biggest_layer = NeuronView.HEIGHT_SPRITE * max_n_layers

        self.layers_view = [LayerView(self.window,
                                      (self.pos[0] + i * (NeuronView.WIDTH_SPRITE + self.DISTANCE_BTW_LAYERS),
                                       self.pos[1] + int(((1.0 - layers[i] / max_n_layers) * lenght_biggest_layer) / 2))
                                      , layers[i]) for i in range(len(layers))]

    def update_layers(self, res_forward_prop: list) -> None:
        """
        Met à jour les neurones de chaque layer à afficher
        :param res_forward_prop: La liste des résultats ce chaque couche
        :return: None
        """
        i = 0

        for l in res_forward_prop:

            output_layer = i == len(res_forward_prop) - 1

            self.layers_view[i].update_neurons(l, output_layer=output_layer)

            i += 1

    def display(self) -> None:
        """
        Affiche le réseau de neurones
        :return: None
        """

        for i in reversed(range(len(self.layers_view))):

            if i:

                self.layers_view[i].connect_to_previous_layer(self.layers_view[i - 1])

            self.layers_view[i].display()

