import glfw
from OpenGL import GL
from OpenGL.arrays import vbo
import numpy as np
import ctypes
from ctypes import c_void_p

from base import OpenGLApp
from gl_shaders import Shader, ShaderProgram


class ShadersEx2(OpenGLApp):
    def __init__(self):
        super().__init__("Shaders Exercise 2")
        self._vao = 0
        self._shader_program = None

    def initialize(self):
        vertices = np.array([
            # position       # color
            0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            -0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0],
            dtype=np.float32)

        self._vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao)

        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)

        # position vertex attribute
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 6 * ctypes.sizeof(ctypes.c_float), c_void_p(0))
        GL.glEnableVertexAttribArray(0)
        # color vertex attribute
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 6 * ctypes.sizeof(ctypes.c_float), c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
        GL.glEnableVertexAttribArray(1)

        GL.glBindVertexArray(0)

        vertex_shader = Shader(GL.GL_VERTEX_SHADER, "shaders_src/shaders_ex2_vertex.glsl")
        fragment_shader = Shader(GL.GL_FRAGMENT_SHADER, "shaders_src/shaders_ex1_frag.glsl")
        self._shader_program = ShaderProgram(vertex_shader, fragment_shader)

    def render(self):
        self._shader_program.use()
        self._shader_program.set_float4("pos_offset", 0.5, 0.0, 0.0, 0.0)
        GL.glBindVertexArray(self._vao)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)


if __name__ == "__main__":
    app = ShadersEx2()
    app.run()

