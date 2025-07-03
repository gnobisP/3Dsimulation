from panda3d.core import Vec3

class PlayerController:
    def __init__(self, key_map, player_model):
        self.key_map = key_map
        self.model = player_model

    def update(self, dt):
        direction = Vec3(0, 0, 0)
        if self.key_map.get("arrow-up"): direction += Vec3(0, -1, 0)
        if self.key_map.get("arrow-down"): direction += Vec3(0, 1, 0)
        if self.key_map.get("arrow-left"): direction += Vec3(1, 0, 0)
        if self.key_map.get("arrow-right"): direction += Vec3(-1, 0, 0)

        if direction.length() > 0:
            direction.normalize()
            new_position = self.model.position + direction * self.model.speed * dt
            self.model.position = new_position
            angle = direction.signedAngleDeg(Vec3(0, -1, 0), Vec3(0, 0, -1))
            self.model.rotation = angle
