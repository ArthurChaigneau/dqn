import Plane
import Env
import GameView

e = Env.Env(800, 1200)

g = GameView.GameView(800, 1200, e)

g.run()