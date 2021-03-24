import glfw
from OpenGL import GL
import numpy as np
import ctypes


def error(err, desc):
    print(f"Error({err}: {desc}")


def process_key(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def render(window):
    # Render here
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
    glfw.set_error_callback(error)

    if not glfw.init():
        exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

    w, h = (800, 600)
    window = glfw.create_window(w, h, "Learn Modern OpenGL", None, None)
    if not window:
        glfw.terminate()
        exit(1)

    glfw.set_key_callback(window, process_key)
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        width, height = glfw.get_framebuffer_size(window)
        GL.glViewport(0, 0, width, height)
        GL.glClearColor(0.6, 0.6, 0.6, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        render(window)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()

