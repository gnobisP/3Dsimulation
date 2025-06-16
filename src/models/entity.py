import numpy as np
import pyrr
from constantes import GLOBAL_Y, GLOBAL_Z

class Entity:
    """
        A basic object in the world, with a position and rotation.
    """
    __slots__ = ("position", "eulers")

    def __init__(self, position: list[float], eulers: list[float]):
        """
            Initialize the entity.

            Parameters:

                position: the position of the entity.

                eulers: the rotation of the entity
                        about each axis.
        """

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

    def update(self, dt: float, camera_pos: np.ndarray) -> None:
        """
            Update the object, this is meant to be implemented by
            objects extending this class.

            Parameters:

                dt: framerate correction factor.

                camera_pos: the position of the camera in the scene
        """

        pass

    def get_model_transform(self) -> np.ndarray:
        """
            Returns the entity's model to world
            transformation matrix.
        """

        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = GLOBAL_Y,
                theta = np.radians(self.eulers[1]), 
                dtype = np.float32
            )
        )

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = GLOBAL_Z,
                theta = np.radians(self.eulers[2]), 
                dtype = np.float32
            )
        )

        return pyrr.matrix44.multiply(
            m1=model_transform, 
            m2=pyrr.matrix44.create_from_translation(
                vec=np.array(self.position),dtype=np.float32
            )
        )

class Cube(Entity):
    """
        A basic object in the world, with a position and rotation.
    """
    __slots__ = tuple()

    def __init__(self, position: list[float], eulers: list[float]):
        """
            Initialize the cube.

            Parameters:

                position: the position of the entity.

                eulers: the rotation of the entity
                        about each axis.
        """

        super().__init__(position, eulers)
    
    def update(self, dt: float, camera_pos: np.ndarray) -> None:
        """
            Update the cube.

            Parameters:

                dt: framerate correction factor.

                camera_pos: the position of the camera in the scene
        """

        self.eulers[2] += 0.25 * dt
        
        if self.eulers[2] > 360:
            self.eulers[2] -= 360

class Billboard(Entity):
    """
        An object which always faces towards the camera
    """
    __slots__ = tuple()

    def __init__(self, position: list[float]):
        """
            Initialize the billboard.

            Parameters:

                position: the position of the entity.
        """

        super().__init__(position, eulers=[0,0,0])
    
    def update(self, dt: float, camera_pos: np.ndarray) -> None:
        """
            Update the billboard.

            Parameters:

                dt: framerate correction factor.

                camera_pos: the position of the camera in the scene
        """

        self_to_camera = camera_pos - self.position
        self.eulers[2] = -np.degrees(np.arctan2(-self_to_camera[1], self_to_camera[0]))
        dist2d = pyrr.vector.length(self_to_camera)
        self.eulers[1] = -np.degrees(np.arctan2(self_to_camera[2], dist2d))

class PointLight(Billboard):
    """
        A simple pointlight.
    """
    __slots__ = ("color", "strength")


    def __init__(
        self, position: list[float], 
        color: list[float], strength: float):
        """
            Initialize the light.

            Parameters:

                position: position of the light.

                color: (r,g,b) color of the light.

                strength: strength of the light.
        """

        super().__init__(position)
        self.color = np.array(color, dtype=np.float32)
        self.strength = strength
