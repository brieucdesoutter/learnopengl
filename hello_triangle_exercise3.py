import glfw
from OpenGL import GL
import numpy as np
import ctypes

from base import OpenGLApp
from gl_shaders import Shader, ShaderProgram


class HelloTriangleEx3(OpenGLApp):
    def __init__(self):
        super().__init__("Hello Triangle Exercise 2")
        self._vao_a = 0
        self._vao_b = 0
        self._shader_program_orange = None
        self._shader_program_pink = None

    def initialize(self):
        vertices_a = np.array([
            -0.6, -0.5, 0.0,
            0.4, -0.5, 0.0,
            -0.1, 0.5, 0.0], dtype=np.float32)

        vertices_b = np.array([
            0.1, 0.5, 0.0,
            0.6, -0.5, 0.0,
            1.0, 0.5, 0.0
        ], dtype=np.float32)

        self._vao_a = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao_a)

        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices_a, GL.GL_STATIC_DRAW)

        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), None)
        GL.glEnableVertexAttribArray(0)

        GL.glBindVertexArray(0)

        self._vao_b = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao_b)

        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices_b, GL.GL_STATIC_DRAW)

        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), None)
        GL.glEnableVertexAttribArray(0)

        GL.glBindVertexArray(0)

        vertex_shader = Shader(GL.GL_VERTEX_SHADER, "shaders_src/hello_triangle_vertex.glsl")
        fragment_shader_orange = Shader(GL.GL_FRAGMENT_SHADER, "shaders_src/hello_triangle_ex3_frag.glsl.template", color="1.0, 0.6, 0.2, 1.0")
        fragment_shader_pink = Shader(GL.GL_FRAGMENT_SHADER, "shaders_src/hello_triangle_ex3_frag.glsl.template", color="1.0, 0.75, 0.8, 1.0")

        self._shader_program_orange = ShaderProgram(vertex_shader, fragment_shader_orange)
        self._shader_program_pink = ShaderProgram(vertex_shader, fragment_shader_pink)

        vertex_shader.delete()
        fragment_shader_orange.delete()
        fragment_shader_pink.delete()

    def render(self):
        self._shader_program_orange.use()
        GL.glBindVertexArray(self._vao_a)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        self._shader_program_pink.use()
        GL.glBindVertexArray(self._vao_b)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)


if __name__ == "__main__":
    app = HelloTriangleEx3()
    app.run()

