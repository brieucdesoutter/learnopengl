import glfw
from imgui.integrations.glfw import GlfwRenderer
import imgui
from OpenGL import GL
import numpy as np
import ctypes


def resize(window, width, height):
    print(f"Resizing to {width}x{height}...")
    GL.glViewport(0, 0, width, height)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def render(window):
    # Render here
    GL.glClearColor(0.6, 0.6, 0.6, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    vertices = np.array([-0.5, -0.5, 0.0, 0.5, -0.5, 0.0, 0.0, 0.5, 0.0], dtype=np.float32)

    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)

    vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)

    vertex_shader_src = """#version 330 core
layout (location = 0) in vec3 aPos;
void main() {
    gl_Position = vec4(aPos, 1.0);
}
"""

    vertex_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
    GL.glShaderSource(vertex_shader, vertex_shader_src, None)
    GL.glCompileShader(vertex_shader)

    fragment_shader_src = """#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);
}"""

    fragment_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
    GL.glShaderSource(fragment_shader, fragment_shader_src, None)
    GL.glCompileShader(fragment_shader)

    shader_program = GL.glCreateProgram()
    GL.glAttachShader(shader_program, vertex_shader)
    GL.glAttachShader(shader_program, fragment_shader)
    GL.glLinkProgram(shader_program)

    GL.glDeleteShader(vertex_shader)
    GL.glDeleteShader(fragment_shader)

    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 3 * ctypes.sizeof(ctypes.c_float), None)
    GL.glEnableVertexAttribArray(0)

    GL.glUseProgram(shader_program)
    GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)


def _opengl_info():
    renderer = GL.glGetString(GL.GL_RENDERER).decode('utf-8')
    opengl_version = GL.glGetString(GL.GL_VERSION).decode('utf-8')
    shader_version = GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('utf-8')
    return f"Renderer: {renderer}\nOpenGL Version: {opengl_version}\nShader Version: {shader_version}"


def main():


    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
    
    w, h = (800, 600)
    window = glfw.create_window(w, h, "Learn Modern OpenGL", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_window_size_callback(window, resize)
    
    glfw.make_context_current(window)

    print(_opengl_info())

    GL.glViewport(0, 0, w, h)

    imgui.create_context()
    ui = GlfwRenderer(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        process_input(window)
        ui.process_inputs()

        render(window)

        imgui.new_frame()

        # imgui.show_demo_window()

        imgui.style_colors_light()
        imgui.begin("Custom window", False, imgui.WINDOW_MENU_BAR)
        if imgui.begin_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            imgui.end_menu_bar()
        imgui.text("Bar")
        imgui.text_ansi("B\033[31marA\033[mnsi ")
        imgui.text_ansi_colored("Eg\033[31mgAn\033[msi ", 0.2, 1., 0.)
        imgui.extra.text_ansi_colored("Eggs", 0.2, 1., 0.)
        imgui.end()

        imgui.render()
        ui.render(imgui.get_draw_data())

        glfw.swap_buffers(window)

    ui.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()

