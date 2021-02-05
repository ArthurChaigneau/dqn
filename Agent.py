import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import Plane
import Env
from collections import deque
import random
import numpy as np


class Agent:
    """
    Agent prenant les décisions pour le serpent
    """

    MEMORY_SIZE = 50_000
    MIN_BATCH_SIZE_TRAINING = 1000
    MINI_BATCH_SIZE = 64
    UPDATE_TARGET_EVERY = 5
    DISCOUNT = 0.99

    def __init__(self, env: Env.Env, load_model=False, model_file_name=""):
        """
        Init de la classe
        """

        # Env dans lequel l'avion évolue
        self.env = env

        # Model principal utilisé pour fit et predict
        if load_model:
            self.model = self.load_model(model_file_name)
        else:
            self.model = self.create_model()
            self.model.build(input_shape=(None, self.env.OBSERVATION_SIZE))

        # Deque pour stocker les exemples sur lesquels entrainer le NN
        self.training_q = deque(maxlen=self.MEMORY_SIZE)

    def create_model(self):
        """
        Création d'un model DNN
        :return: Le model créé
        """

        model = tf.keras.Sequential([
            tf.keras.layers.Dense(self.env.OBSERVATION_SIZE, activation='relu'),
            tf.keras.layers.Dense(4, activation='relu'),
            tf.keras.layers.Dense(self.env.ACTION_SPACE_SIZE, activation='linear')
        ])

        model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

        return model

    def update_training_set(self, transition: tuple) -> None:
        """
        Ajoute un nouvel exemple dans training_q
        :param transition: Un tuple de la forme : (observation space, action, reward, new observation space, done)
        :return: None
        """

        self.training_q.append(transition)

    def train(self) -> None:
        """
        Entraine le model principal
        :return: None
        """

        if len(self.training_q) < self.MIN_BATCH_SIZE_TRAINING:
            return None

        # On prend MINI_BATCH_SIZE (64) éléments sur lesuels train
        minibatch = random.sample(self.training_q, self.MINI_BATCH_SIZE)

        # On prédit les q values à partir des états actuels
        cur_states = np.array([row[0] for row in minibatch])
        print("Shape train :", cur_states.shape)
        print("Première ligne :", cur_states[0, :])
        cur_q_values_list = self.model.predict(cur_states)

        # On prédit les q values à partir des états futurs
        new_states = np.array([row[3] for row in minibatch])
        print("Shape futur train :", cur_states.shape)
        print("Première ligne futur :", cur_states[0, :])
        new_q_values_list = self.model.predict(new_states)

        X = []
        Y = []

        # Création du training set
        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):

            # Si on a pas atteint un état final alors on utilise la formule du q learning
            if not done:
                max_future_q_value = np.max(new_q_values_list[index])
                new_q_value = reward + self.DISCOUNT * max_future_q_value

            # Sinon, on prend juste la reward finale
            else:
                new_q_value = reward

            # On update la Q value de l'état actuel en ayant pris l'action "action"
            current_q_values = cur_q_values_list[index]
            current_q_values[action] = new_q_value

            # Ajout dans le training set
            X.append(current_state)
            Y.append(current_q_values.tolist())

        # On entraine notre model
        self.model.fit(X, Y, batch_size=self.MINI_BATCH_SIZE, verbose=0, shuffle=False)

    def get_q_values(self, state: np.ndarray):
        """
        Obtient les q-values associées à l'état passé en params
        :return: Un vecteur de 2 q-values (voir val ACTION_SPACE_SIZE)
        """

        return self.model.predict(state.reshape((1, state.shape[0])))[0]

    def save_model(self, file_name: str) -> None:
        """
        Sauvegarde notre model
        :param file_name: Le nom du fichier à créer
        :return: None
        """

        self.model.save('model/' + file_name + 'h5', save_format='h5')

    def load_model(self, file_name: str) -> tf.keras.Model:
        """
        Charge un model depuis un fichier
        :param file_name: Le nom du fichier
        :return: Le model chargé
        """
        return tf.keras.models.load_model('model/' + file_name + '.h5')











