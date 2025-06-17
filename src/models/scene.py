import numpy as np


from models.entity import Entity, Cube, Billboard, PointLight, Station
from models.camera import Camera


ENTITY_TYPE = {
    "CUBE": 0,
    "POINTLIGHT": 1,
    "MEDKIT": 2,
    "STATION": 3,
}

class Scene:
    """
        Manages all objects and coordinates their interactions.
    """
    __slots__ = ("entities", "player")


    def __init__(self):
        """
            Initialize the scene.
        """

        self.entities: dict[int, list[Entity]] = {
            ENTITY_TYPE["CUBE"]: [
                #Cube(position = [6,0,0], eulers = [0,0,0]),
            ],

            ENTITY_TYPE["MEDKIT"]: [
                #Billboard(position = [3,0,-0.5])
            ],
            
            ENTITY_TYPE["POINTLIGHT"]: [
                PointLight(
                    position = [
                        np.random.uniform(low=3.0, high=9.0), 
                        np.random.uniform(low=-2.0, high=2.0), 
                        np.random.uniform(low=0.0, high=4.0)],
                    color = [
                        np.random.uniform(low=0.5, high=1.0), 
                        np.random.uniform(low=0.5, high=1.0), 
                        np.random.uniform(low=0.5, high=1.0)],
                    strength = 3)
                for _ in range(8)
            ],

            ENTITY_TYPE["STATION"]: [
                Station(position = [6,0,0], eulers = [0,0,0]),
            ],
        }

        self.player = Camera(
            position = [0,0,2]
        )

    def update(self, dt: float) -> None:
        """
            Update all objects in the scene.

            Parameters:

                dt: framerate correction factor
        """

        for entities in self.entities.values():
            for entity in entities:
                entity.update(dt, self.player.position)

        self.player.update(dt)

    def move_player(self, d_pos: list[float]) -> None:
        """
            move the player by the given amount in the 
            (forwards, right, up) vectors.
        """

        self.player.move(d_pos)
    
    def spin_player(self, d_eulers: list[float]) -> None:
        """
            spin the player by the given amount
            around the (x,y,z) axes
        """

        self.player.spin(d_eulers)
