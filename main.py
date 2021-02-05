import App

WIDTH = 1200
HEIGHT = 800
EPISODES = 10_000
TRAINING = True
SAVE_MODEL = True
NAME_FILE = "test"

app = App.App(EPISODES, HEIGHT, WIDTH, save_model=SAVE_MODEL, model_file_name=NAME_FILE)

app.run(training=True)