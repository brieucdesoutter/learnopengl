from OpenGL import GL
import numpy as np
import ctypes

from base import OpenGLApp
from gl_shaders import Shader, ShaderProgram


class HelloTriangleIndexed(OpenGLApp):
    def __init__(self):
        super().__init__("Hello Triangle Indexed")
        self._vao = 0
        self._shader_program = None

    def initialize(self):
        vertices = np.array([0.5, 0.5, 0.0,
                             0.5, -0.5, 0.0,
                             -0.5, -0.5, 0.0,
                             -0.5, 0.5, 0.0], dtype=np.float32)

        indices = np.array([0, 1, 3, 1, 2, 3], dtype=np.uint32)

        self._vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao)

        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)

        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), None)
        GL.glEnableVertexAttribArray(0)

        ebo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ebo)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices, GL.GL_STATIC_DRAW)

        GL.glBindVertexArray(0)

        vertex_shader = Shader(GL.GL_VERTEX_SHADER, "shaders_src/hello_triangle_vertex.glsl")
        fragment_shader = Shader(GL.GL_FRAGMENT_SHADER, "shaders_src/hello_triangle_frag.glsl")

        self._shader_program = ShaderProgram(vertex_shader, fragment_shader)

        vertex_shader.delete()
        fragment_shader.delete()

    def render(self):
        self._shader_program.use()
        GL.glBindVertexArray(self._vao)
        GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)


if __name__ == "__main__":
    app = HelloTriangleIndexed()
    app.run()

