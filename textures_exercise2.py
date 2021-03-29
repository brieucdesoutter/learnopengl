import glfw
from OpenGL import GL
import numpy as np
import ctypes
from PIL import Image

from base import OpenGLApp
from gl_shaders import Shader, ShaderProgram
from gl_textures import Texture2D


class TexturesApp(OpenGLApp):
    def __init__(self):
        super().__init__("Textures Exercise 2")
        self._vao = 0
        self._texture = None
        self._shader_program = None

    def initialize(self):
        vertices = np.array([
            0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 2.0, 2.0,  # top right
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 2.0, 0.0,  # bottom right
            -0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # bottom left
            -0.5, 0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 2.0  # top left
        ], dtype=np.float32)

        indices = np.array([0, 1, 3, 1, 2, 3], dtype=np.uint32)

        self._vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao)

        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)

        float_size = ctypes.sizeof(ctypes.c_float)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 8 * float_size, ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(0)

        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 8 * float_size, ctypes.c_void_p(3 * float_size))
        GL.glEnableVertexAttribArray(1)

        GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, GL.GL_FALSE, 8 * float_size, ctypes.c_void_p(6 * float_size))
        GL.glEnableVertexAttribArray(2)

        ebo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ebo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices, GL.GL_STATIC_DRAW)

        GL.glBindVertexArray(0)

        self._texture = Texture2D("awesomeface.png", flip_y=True, wrap_s=GL.GL_REPEAT, wrap_t=GL.GL_REPEAT)

        vertex_shader = Shader(GL.GL_VERTEX_SHADER, "shaders_src/textures_vertex.glsl")
        fragment_shader = Shader(GL.GL_FRAGMENT_SHADER, "shaders_src/textures_frag.glsl")
        self._shader_program = ShaderProgram(vertex_shader, fragment_shader)
        vertex_shader.delete()
        fragment_shader.delete()

    def render(self):
        self._texture.use()
        GL.glBindVertexArray(self._vao)
        self._shader_program.use()
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)


if __name__ == "__main__":
    app = TexturesApp()
    app.run()

