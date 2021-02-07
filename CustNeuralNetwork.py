import tensorflow as tf
import numpy as np


def relu(z):
    """
    Calcule l'image de chaque élément de Z à travers la fonction g(x) = max(x, 0)
    :param z: Une matrice
    :return: L'image par la fonction relu
    """
    return np.maximum(z, 0)


def sigmoid(z) -> np.ndarray:
    """
    Calcule l'image d'une matrice par la fonction f(x) = 1 / (1 + e^(-x))
    :param z: Une matrice
    :return: L'image par la fonction sigmoid
    """

    return 1 / (1 + np.exp(-z))


def softmax(z) -> np.ndarray:
    """
    Calcule l'image d'une matrice par la fonction softmax
    :param z: Une matrice
    :return: L'image de la matrice par la fonction softmax
    """
    temp = np.exp(z - np.max(z))
    return temp / temp.sum(axis=1, keepdims=True)


def linear(z) -> np.ndarray:
    """
    Retourne la matrice inchangée
    :param z: Une matrice
    :return: La matrice z
    """
    return z


class CustNeuralNetwork:
    """
    Construit un réseau de neurones à partir d'un "model" TF
    """

    def __init__(self, file_name: str):
        """
        Initialisation de la classe.
        :param file_name: Le nom du fichier où est enregistré un "model" TF
        """

        self.parameters = self.load_model(file_name)

    def load_model(self, file_name: str) -> dict:
        """
        Charge un réseau de neurones à partir d'un fichier où est enregistré un "model" TF
        :param file_name: Le nom du fichier
        :return: Un dictionnaire conteant les paramètres du réseau de neurones
        """
        model = tf.keras.models.load_model('model/' + file_name + '.h5')

        parameters = {}

        idx = 1

        for weight in model.get_weights():

            if len(weight.shape) > 1:

                parameters['W' + str(idx)] = weight
            else:

                parameters['b' + str(idx)] = weight
                idx += 1

        return parameters

    def linear_forward(self, A: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        Implémente la partie linéaire du la propagation avant
        :param A: La matrice d'activation de la précédente couche
        :param W: Les poids sous la forme d'une matrice
        :param b: Le vecteur pour les biais
        :return: La matrice Z, résultat de la multiplication entre A et W et de l'ajout de b
        """

        Z = np.dot(A, W) + b

        return Z

    def linear_activation_forward(self, A: np.ndarray, W: np.ndarray, b: np.ndarray, activation: str) -> np.ndarray:
        """
        Fait appel à linear_forward ainsi qu'à la fonction d'activation choisie
        :param A: La matrice d'activation de la précédente couche
        :param W: Les poids sous la forme d'une matrice
        :param b: Le vecteur pour les biais
        :param activation: Le nom de la fonction d'activation choisie
        :return: La prochaine matrice A
        """

        func = globals()[activation]

        return func(self.linear_forward(A, W, b))

    def forward_propagation(self, X: np.ndarray) -> list:
        """
        Effectue la propagation avant du réseau de neurones
        :param X: La matrice en entrée du réseau de neurones
        :return: Une liste avec les matrices A de chaque couche
        """

        A = X

        L = len(self.parameters) // 2

        result = []

        for l in range(1, L):

            A_prev = A

            A = self.linear_activation_forward(A_prev, self.parameters['W' + str(l)], self.parameters['b' + str(l)],
                                               'relu')

            result.append(A)

        result.append(self.linear_activation_forward(A, self.parameters['W' + str(L)], self.parameters['b' + str(L)],
                                                     'linear'))

        return result

    def predict(self, inputs: np.ndarray) -> np.ndarray:
        """
        Effectue une prédiction à partir de la dernière A obtenue
        :param inputs: La matrice en entrée
        :return: La matrice de la dernière couche
        """

        return self.forward_propagation(inputs)[-1]

