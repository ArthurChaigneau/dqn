import Agent
import Env
import tqdm
import numpy as np


class Game:
    """
    Principale classe chargée de lancer la partie
    """
    EPSILON_DECAY = 0.99975
    MIN_EPSILON = 0.001

    def __init__(self, episodes: int, height: int, width: int, save_model=False,
                 load_model_training=False, load_model_pred=False, model_file_name=""):
        """
        Init de la classe
        :param episodes: Nb de parties simulées pour l'entrainement
        :param height: Hauteur de la fenêtre
        :param width: Largeur de la fenêtre
        :param save_model: Bool pour indiquer si on doit sauvegarder le model entrainer à la fin
        :param load_model_training: Bool pour indiquer si on doit charger un model déjà existant pour l'entrainer
        :param load_model_pred: Bool pour indiquer si on doit charger un model déjà existant pour faire les prédictions
        :param model_file_name: Nom du fichier à charger
        """

        # Nombre d'épisodes pour train
        self.episodes = episodes

        # L'env dans lequel la partie va se dérouler
        self.env = Env.Env(height, width)

        # L'agent chargé de déterminer les actions du serpent
        self.agent = Agent.Agent(self.env, load_model_training=load_model_training, load_model_pred=load_model_pred,
                                 model_file_name=model_file_name)

        # Val pour choix entre action random et meilleure action possible
        self.epsilon = 1

        # épisode actuel
        self.cur_ep = 0

        # Temps entre chaque mouve
        self.time_btw_move = 0.0

        # Bool pour indiquer si la partie actuelle est finie
        self.done = True

        # État actuel
        self.cur_state = None

        # Bool pour indiquer que le partie a été restart
        self.restarted = False

        # Bool pour savoir si on sauvegarde le model
        self.save_model = save_model

        # Le nom du fichier dans lequel sauvegarder le model
        self.model_file_name = model_file_name

    def terminal_test(self):
        """
        Lance une partie en mode terminal
        :return:
        """

        for self.cur_ep in tqdm.tqdm(range(1, self.episodes + 1), ascii=True, unit='episodes'):

            # Nombre de passages dans la boucle principale
            step = 1

            cur_state = self.env.reset()

            done = False

            while not done:

                # Choix au hasard entre :
                if np.random.random() > self.epsilon:
                    # Action à partir de la q-table
                    action = np.argmax(self.agent.get_q_values(np.array(cur_state)))

                else:
                    # Action random
                    action = np.random.randint(0, self.env.ACTION_SPACE_SIZE)

                # On effectue une action avec le serpent
                new_state, reward, done = self.env.step(action)

                # Ajout d'un exemple dans la mémoire
                self.agent.update_training_set((cur_state, action, reward, new_state, done))

                # Entrainement éventuel
                self.agent.train()

                cur_state = new_state
                step += 1

            if self.epsilon > self.MIN_EPSILON:
                self.epsilon *= self.EPSILON_DECAY
                self.epsilon = max(self.MIN_EPSILON, self.epsilon)

        if self.save_model:
            self.agent.save_model(self.model_file_name)

    def graphic_test(self) -> None:
        """
        Méthode à utiliser si on affiche les graphiques lors de la partie
        :return: None
        """

        self.cur_ep = 0

        if self.done:
            self.cur_ep += 1

            self.cur_state = self.env.reset()

            self.restarted = True

            self.done = False

        action = int(np.argmax(self.agent.get_q_values(np.array(self.cur_state))))

        self.cur_state, _, self.done = self.env.step(action)






