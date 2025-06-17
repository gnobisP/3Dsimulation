from OpenGL.GL import *
import pyrr
import numpy as np

from views.material import Material
from views.mesh import Mesh, ObjMesh, RectMesh
from views.shaders import Shader
from models.camera import Camera
from models.entity import Entity

UNIFORM_TYPE = {
    "MODEL": 0,
    "VIEW": 1,
    "PROJECTION": 2,
    "CAMERA_POS": 3,
    "LIGHT_COLOR": 4,
    "LIGHT_POS": 5,
    "LIGHT_STRENGTH": 6,
    "TINT": 7,
}
ENTITY_TYPE = {
    "CUBE": 0,
    "POINTLIGHT": 1,
    "MEDKIT": 2,
    "STATION": 3,
}
PIPELINE_TYPE = {
    "Standard": 0,
}

class GraphicsEngine:
    """
        Draws entities and stuff.
    """
    __slots__ = ("meshes", "materials", "shaders")


    def __init__(self):
        """
            Initializes the rendering system.
        """

        self._set_up_opengl()

        self._create_assets()

        self._set_onetime_uniforms()

        self._get_uniform_locations()
    
    def _set_up_opengl(self) -> None:
        """
            Configure any desired OpenGL options
        """

        glClearColor(0.0, 0.0, 0.0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    def _create_assets(self) -> None:
        """
            Create all of the assets needed for drawing.
        """

        self.meshes: dict[int, Mesh] = {
            ENTITY_TYPE["CUBE"]: ObjMesh("../assets/models/cube.obj"),
            ENTITY_TYPE["MEDKIT"]: RectMesh(w = 0.6, h = 0.5),
            ENTITY_TYPE["POINTLIGHT"]: RectMesh(w = 0.2, h = 0.2),
        }

        self.materials: dict[int, Material] = {
            ENTITY_TYPE["CUBE"]: Material("../assets/gfx/wood.jpeg"),
            ENTITY_TYPE["MEDKIT"]: Material("../assets/gfx/wood.jpeg"),
            ENTITY_TYPE["POINTLIGHT"]: Material("../assets/gfx/wood.jpeg"),
        }
        
        self.shaders: dict[int, Shader] = {
            PIPELINE_TYPE["Standard"]: Shader(
                "../assets/shaders/vertex.txt", "../assets/shaders/fragment.txt"),
        }

    def _set_onetime_uniforms(self) -> None:
        """
            Some shader data only needs to be set once.
        """

        shader = self.shaders[PIPELINE_TYPE["Standard"]]
        shader.use()
        glUniform1i(glGetUniformLocation(shader.program, "imageTexture"), 0)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = 45, aspect = 640/480, 
            near = 0.1, far = 50, dtype=np.float32
        )
        glUniformMatrix4fv(
            glGetUniformLocation(shader.program,"projection"),
            1, GL_FALSE, projection_transform
        )
    
    def _get_uniform_locations(self) -> None:
        """
            Query and store the locations of shader uniforms
        """

        shader = self.shaders[PIPELINE_TYPE["Standard"]]
        shader.use()

        shader.cache_single_location(
            UNIFORM_TYPE["CAMERA_POS"], "cameraPosition")
        shader.cache_single_location(UNIFORM_TYPE["MODEL"], "model")
        shader.cache_single_location(UNIFORM_TYPE["VIEW"], "view")
        shader.cache_single_location(UNIFORM_TYPE["TINT"], "tint")

        for i in range(8):

            shader.cache_multi_location(
                UNIFORM_TYPE["LIGHT_COLOR"], f"Lights[{i}].color")
            shader.cache_multi_location(
                UNIFORM_TYPE["LIGHT_POS"], f"Lights[{i}].position")
            shader.cache_multi_location(
                UNIFORM_TYPE["LIGHT_STRENGTH"], f"Lights[{i}].strength")
    
    def render(self, 
        camera: Camera, renderables: dict[int, list[Entity]]) -> None:
        """
            Draw everything.

            Parameters:

                camera: the scene's camera

                renderables: all the entities to draw
        """

        #refresh screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        shader = self.shaders[PIPELINE_TYPE["Standard"]]
        shader.use()

        glUniformMatrix4fv(
            shader.fetch_single_location(UNIFORM_TYPE["VIEW"]),
            1, GL_FALSE, camera.get_view_transform())

        glUniform3fv(
            shader.fetch_single_location(UNIFORM_TYPE["CAMERA_POS"]),
            1, camera.position)

        for i,light in enumerate(renderables[ENTITY_TYPE["POINTLIGHT"]]):

            glUniform3fv(
                shader.fetch_multi_location(UNIFORM_TYPE["LIGHT_POS"], i),
                1, light.position)
            glUniform3fv(
                shader.fetch_multi_location(UNIFORM_TYPE["LIGHT_COLOR"], i),
                1, light.color)
            glUniform1f(
                shader.fetch_multi_location(UNIFORM_TYPE["LIGHT_STRENGTH"], i),
                light.strength)
        
        for entity_type, entities in renderables.items():

            if entity_type not in self.materials:
                continue

            material = self.materials[entity_type]
            material.use()
            mesh = self.meshes[entity_type]
            mesh.arm_for_drawing()
            
            color = np.array([1,1,1], dtype = np.float32)
            for entity in entities:

                if entity_type == ENTITY_TYPE["POINTLIGHT"]:
                    color = entity.color

                glUniform3fv(
                    shader.fetch_single_location(UNIFORM_TYPE["TINT"]), 
                    1, color)
                glUniformMatrix4fv(
                    shader.fetch_single_location(UNIFORM_TYPE["MODEL"]),
                    1, GL_FALSE, entity.get_model_transform())

                mesh.draw()

        glFlush()

    def destroy(self) -> None:
        """ free any allocated memory """

        for mesh in self.meshes.values():
            mesh.destroy()
        for material in self.materials.values():
            material.destroy()
        for shader in self.shaders.values():
            shader.destroy()

