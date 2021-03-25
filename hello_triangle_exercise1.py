from OpenGL import GL
import numpy as np
import ctypes

from base import OpenGLApp
from gl_shaders import Shader, ShaderProgram


class HelloTriangleEx1(OpenGLApp):

    def __init__(self):
        super().__init__("Hello Triangle Exercise 1")
        self._vao = 0
        self._shader_program = None

    def initialize(self):
        vertices = np.array([
            -0.6, -0.5, 0.0,
            0.4, -0.5, 0.0,
            -0.1, 0.5, 0.0,
            0.1, 0.5, 0.0,
            0.6, -0.5, 0.0,
            1.0, 0.5, 0.0
        ], dtype=np.float32)

        self._vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao)

        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)

        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), None)
        GL.glEnableVertexAttribArray(0)

        vertex_shader = Shader(GL.GL_VERTEX_SHADER, "shaders_src/hello_triangle_vertex.glsl")
        fragment_shader = Shader(GL.GL_FRAGMENT_SHADER, "shaders_src/hello_triangle_frag.glsl")
        self._shader_program = ShaderProgram(vertex_shader, fragment_shader)
        vertex_shader.delete()
        fragment_shader.delete()

    def render(self):
        self._shader_program.use()
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)


if __name__ == "__main__":
    app = HelloTriangleEx1()
    app.run()

