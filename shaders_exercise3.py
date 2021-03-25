import ctypes
from ctypes import c_void_p

import numpy as np
from OpenGL import GL

from base import OpenGLApp
from gl_shaders import Shader, ShaderProgram


class ShadersEx3(OpenGLApp):
    def __init__(self):
        super().__init__("Shaders Exercise 3")
        self._vao = 0
        self._shader_program = None

    def initialize(self):
        vertices = np.array([
            # position
            0.5, -0.5, 0.0,
            -0.5, -0.5, 0.0,
            0.0, 0.5, 0.0],
            dtype=np.float32)

        self._vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao)

        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)

        # position vertex attribute
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), c_void_p(0))
        GL.glEnableVertexAttribArray(0)

        GL.glBindVertexArray(0)

        vertex_shader = Shader(GL.GL_VERTEX_SHADER, "shaders_src/shaders_ex3_vertex.glsl")
        fragment_shader = Shader(GL.GL_FRAGMENT_SHADER, "shaders_src/shaders_ex3_frag.glsl")
        self._shader_program = ShaderProgram(vertex_shader, fragment_shader)

    def render(self):
        self._shader_program.use()
        GL.glBindVertexArray(self._vao)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)


if __name__ == "__main__":
    app = ShadersEx3()
    app.run()

