from direct.showbase.ShowBase import ShowBase
from models.player_model import PlayerModel
from views.game_view import GameView
from controllers.player_controller import PlayerController
import time
from controllers.camera_controller import CameraController
import sys

class MyApp(ShowBase):
    def __init__(self):
        super().__init__()
        self.disableMouse()

        # MVC
        self.view = GameView(self, self.render, self.loader)
        self.player_model = PlayerModel()
        

        # 🎮 Controle de teclas
        self.key_map = {
            "w": False, "s": False,
            "a": False, "d": False,
            "space": False, "control": False,
            "p": False,
            "arrow-up": False, "arrow-down": False, "arrow-left": False, "arrow-right": False
        }

        self.controller = PlayerController(self.key_map, self.player_model)
        self.camera_controller = CameraController(self, self.key_map)

        # ⌨️ Mapear teclas
        for key in ["w","s","a","d","space", "control", "p", "arrow_up", "arrow_down", "arrow_left", "arrow_right"]:
            self.accept(key, self.update_key, [key.replace("_", "-"), True])
            self.accept(f"{key}-up", self.update_key, [key.replace("_", "-"), False])    

        # ⎋ Fechar
        self.accept("escape", sys.exit)

        # Tempo
        self.last_time = time.perf_counter()

        # Tasks
        self.taskMgr.add(self.game_loop, "game_loop")

    def update_key(self, key, value):
        self.key_map[key] = value

    def game_loop(self, task):
        now = time.perf_counter()
        dt = now - self.last_time
        self.last_time = now

        dt = min(dt, 0.05)
        self.camera_controller.update(dt)
        self.controller.update(dt)

        
        self.view.update_player(self.player_model, self.view.players[0])

        return task.cont

app = MyApp()
app.run()
