from panda3d.core import Vec3

class PlayerModel:
    def __init__(self):
        self.position = Vec3(0, 0, 1500)
        self.direction = Vec3(0, 0, 0)
        self.speed = 500
        self.rotation = 0
        self.anim_name = None
