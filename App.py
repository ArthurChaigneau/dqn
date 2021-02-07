import Game
import GameView


class App:
    """
    Classe principale lançant la partie
    """

    def __init__(self, episodes: int, height: int, width: int, save_model=False,
                 load_model_training=False, load_model_pred=False, model_file_name=""):
        """
        Initialisation de la classe
        :param episodes: Nb de parties diff
        :param width: Largeur fenêtre
        :param height: Hauteur fenêtre
        :param save_model: Bool pour indiquer si on veut sauvegarder le model à la fin de l'entrainement
        :param load_model_training: Bool pour indiquer si on doit charger un model déjà existant pour l'entrainer
        :param load_model_pred: Bool pour indiquer si on doit charger un model déjà existant pour faire les prédictions
        :param model_file_name: Nom du fichier dans lequel sauvegarder le model
        """

        # Une partie
        self.game = Game.Game(episodes, height, width, save_model=save_model, load_model_training=load_model_training,
                              load_model_pred=load_model_pred, model_file_name=model_file_name)

        # Les graphiques
        self.renders = None

        # Largeur
        self.width = width

        # Hauteur
        self.height = height

    def run(self, training=True) -> None:
        """"
        Méthode principale jouant une partie
        :param training: Bool pour indiquer qu'on veut entrainer un model
        :return: None
        """
        if training:
            # Training
            self.game.terminal_test()

        else:
            self.renders = GameView.GameView(self.height, self.width, self.game)

            self.renders.run()