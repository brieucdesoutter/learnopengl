from imgui.integrations.glfw import GlfwRenderer
import imgui
from OpenGL import GL
import numpy as np
import ctypes

from base import OpenGLApp
from gl_shaders import Shader, ShaderProgram


class HelloTriangleImgui(OpenGLApp):
    def __init__(self):
        super().__init__("Hello Triangle with ImGui")
        self._vao = 0
        self._shader_program = None
        self._ui = None

    def initialize(self):
        vertices = np.array([-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.0, 0.5, 0.0], dtype=np.float32)

        self._vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self._vao)

        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)

        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), None)
        GL.glEnableVertexAttribArray(0)

        GL.glBindVertexArray(0)

        vertex_shader = Shader(GL.GL_VERTEX_SHADER, "shaders_src/hello_triangle_vertex.glsl")
        fragment_shader = Shader(GL.GL_FRAGMENT_SHADER, "shaders_src/hello_triangle_frag.glsl")
        self._shader_program = ShaderProgram(vertex_shader, fragment_shader)
        vertex_shader.delete()
        fragment_shader.delete()

        imgui.create_context()
        self._ui = GlfwRenderer(self._window, False)

    def render(self):
        self._shader_program.use()
        GL.glBindVertexArray(self._vao)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

    def render_ui(self):
        imgui.new_frame()
        imgui.show_demo_window()
        imgui.render()
        self._ui.render(imgui.get_draw_data())
        self._ui.process_inputs()


if __name__ == "__main__":
    app = HelloTriangleImgui()
    app.run()

