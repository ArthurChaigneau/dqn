import Plane
import Env
import GameView

e = Env.Env(1200, 800)

g = GameView.GameView(1200, 800, e)

g.run()