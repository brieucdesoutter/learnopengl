import glfw
from OpenGL import GL as GL


class OpenGLApp:
    def __init__(self, app_title, window_width=800, window_height=600):
        glfw.set_error_callback(self.error)

        if not glfw.init():
            raise Exception("glfw failed to initialize!")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

        self._window = glfw.create_window(window_width, window_height, app_title, None, None)
        if not self._window:
            glfw.terminate()
            raise Exception("Failed to create glfw window.")

        glfw.set_key_callback(self._window, self.process_key)

    def _opengl_info(self):
        renderer = GL.glGetString(GL.GL_RENDERER).decode('utf-8')
        opengl_version = GL.glGetString(GL.GL_VERSION).decode('utf-8')
        shader_version = GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('utf-8')
        return f"Renderer: {renderer}\nOpenGL Version: {opengl_version}\nShader Version: {shader_version}"

    def process_key(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def initialize(self):
        pass

    def render(self):
        # Render here
        pass

    def render_ui(self):
        pass

    def error(self, err, desc):
        print(f"Error({err}: {desc}")

    def run(self):

        glfw.make_context_current(self._window)
        glfw.swap_interval(1)

        print(self._opengl_info())

        self.initialize()

        while not glfw.window_should_close(self._window):

            width, height = glfw.get_framebuffer_size(self._window)
            GL.glViewport(0, 0, width, height)
            GL.glClearColor(0.6, 0.6, 0.6, 1.0)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.render()

            self.render_ui()

            glfw.swap_buffers(self._window)
            glfw.poll_events()

        glfw.destroy_window(self._window)
        glfw.terminate()


if __name__ == "__main__":
    app = OpenGLApp("Learn OpenGL", 800, 600)
    app.run()

