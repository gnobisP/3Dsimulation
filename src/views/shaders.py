from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader

class Shader:
    """
        A shader.
    """
    __slots__ = ("program", "single_uniforms", "multi_uniforms")


    def __init__(self, vertex_filepath: str, fragment_filepath: str):
        """
            Initialize the shader.

            Parameters:

                vertex_filepath: filepath to the vertex source code.

                fragment_filepath: filepath to the fragment source code.
        """

        self.program = create_shader(vertex_filepath, fragment_filepath)

        self.single_uniforms: dict[int, int] = {}
        self.multi_uniforms: dict[int, list[int]] = {}
    
    def cache_single_location(self, 
        uniform_type: int, uniform_name: str) -> None:
        """
            Search and store the location of a uniform location.
            This is for uniforms which have one location per variable.
        """

        self.single_uniforms[uniform_type] = glGetUniformLocation(
            self.program, uniform_name)
    
    def cache_multi_location(self, 
        uniform_type: int, uniform_name: str) -> None:
        """
            Search and store the location of a uniform location.
            This is for uniforms which have multiple locations per variable.
            e.g. Arrays
        """

        if uniform_type not in self.multi_uniforms:
            self.multi_uniforms[uniform_type] = []
        
        self.multi_uniforms[uniform_type].append(
            glGetUniformLocation(
            self.program, uniform_name)
        )
    
    def fetch_single_location(self, uniform_type: int) -> int:
        """
            Returns the location of a uniform location.
            This is for uniforms which have one location per variable.
        """

        return self.single_uniforms[uniform_type]
    
    def fetch_multi_location(self, 
        uniform_type: int, index: int) -> int:
        """
            Returns the location of a uniform location.
            This is for uniforms which have multiple locations per variable.
            e.g. Arrays
        """

        return self.multi_uniforms[uniform_type][index]

    def use(self) -> None:
        """
            Use the program.
        """

        glUseProgram(self.program)
    
    def destroy(self) -> None:
        """
            Free any allocated memory.
        """

        glDeleteProgram(self.program)

def create_shader(vertex_filepath: str, fragment_filepath: str) -> int:
    """
        Compile and link shader modules to make a shader program.

        Parameters:

            vertex_filepath: path to the text file storing the vertex
                            source code
            
            fragment_filepath: path to the text file storing the
                                fragment source code
        
        Returns:

            A handle to the created shader program
    """

    with open(vertex_filepath,'r') as f:
        vertex_src = f.readlines()

    with open(fragment_filepath,'r') as f:
        fragment_src = f.readlines()
    
    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))
    
    return shader
