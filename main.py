import App

WIDTH = 1200
HEIGHT = 800
EPISODES = 1500
TRAINING = False
SAVE_MODEL = False
LOAD_MODEL_4_TRAINING = False
LOAD_MODEL_4_PREDICTION = True
NAME_FILE = "model_plane_v1"

app = App.App(EPISODES, HEIGHT, WIDTH, save_model=SAVE_MODEL, load_model_training=LOAD_MODEL_4_TRAINING,
              load_model_pred=LOAD_MODEL_4_PREDICTION, model_file_name=NAME_FILE)

app.run(training=TRAINING)