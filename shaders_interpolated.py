import glfw
from OpenGL import GL
from OpenGL.arrays import vbo
import numpy as np
import ctypes
from ctypes import c_void_p

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

    vertices = np.array([
        # position       # color
        0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
        -0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
        0.0, 0.5, 0.0, 0.0, 0.0, 1.0],
        dtype=np.float32)

    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)

    vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)

    # position vertex attribute
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 6 * ctypes.sizeof(ctypes.c_float), c_void_p(0))
    GL.glEnableVertexAttribArray(0)
    # color vertex attribute
    GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 6 * ctypes.sizeof(ctypes.c_float), c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
    GL.glEnableVertexAttribArray(1)

    vertex_shader_src = """#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
out vec3 ourColor;
void main() {
    gl_Position = vec4(aPos, 1.0);
    ourColor = aColor;
}
"""

    vertex_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
    GL.glShaderSource(vertex_shader, vertex_shader_src, None)
    GL.glCompileShader(vertex_shader)

    fragment_shader_src = """#version 330 core
in vec3 ourColor;
out vec4 FragColor;
void main() {
    FragColor = vec4(ourColor, 1.0);
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

    while not glfw.window_should_close(window):
        process_input(window)
        render(window)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()

