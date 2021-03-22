import glfw
from OpenGL import GL
import numpy as np
import ctypes
from PIL import Image


vao = 0
texture1 = 0
shader_program = 0


def initialize(window, width, height):
    print(_opengl_info())
    vertices = np.array([
        0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0,  # top right
        0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0,  # bottom right
        -0.5, -0.5, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,  # bottom left
        -0.5, 0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0  # top left
    ], dtype=np.float32)

    indices = np.array([0, 1, 3, 1, 2, 3], dtype=np.uint32)

    global vao
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)

    vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)

    float_size = ctypes.sizeof(ctypes.c_float)
    GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 8 * float_size, ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(0)

    GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 8 * float_size, ctypes.c_void_p(3 * float_size))
    GL.glEnableVertexAttribArray(1)

    GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, GL.GL_FALSE, 8 * float_size, ctypes.c_void_p(6 * float_size))
    GL.glEnableVertexAttribArray(2)

    ebo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ebo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices, GL.GL_STATIC_DRAW)

    GL.glBindVertexArray(0)

    global texture1
    texture1 = GL.glGenTextures(1)
    GL.glActiveTexture(GL.GL_TEXTURE0)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture1)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

    im = Image.open("img.png")
    rgb_im = im.convert('RGB')
    width, height = rgb_im.size
    tex_bytes = np.array(rgb_im)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE, tex_bytes)
    GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

    vertex_shader_src = """#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;

out vec3 ourColor;
out vec2 texCoord;

void main() {
    gl_Position = vec4(aPos, 1.0);
    ourColor = aColor;
    texCoord = aTexCoord;
}
"""

    vertex_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
    GL.glShaderSource(vertex_shader, vertex_shader_src, None)
    GL.glCompileShader(vertex_shader)
    status = GL.glGetShaderiv(vertex_shader, GL.GL_COMPILE_STATUS)
    if not status:
        print(GL.glGetShaderInfoLog(vertex_shader, 512, None))

    fragment_shader_src = """#version 330 core
uniform sampler2D ourTexture;

in vec3 ourColor;
in vec2 texCoord;

out vec4 FragColor;
void main() {
    FragColor = texture(ourTexture, texCoord) * vec4(ourColor, 1.0);
}"""

    fragment_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
    GL.glShaderSource(fragment_shader, fragment_shader_src, None)
    GL.glCompileShader(fragment_shader)
    status = GL.glGetShaderiv(vertex_shader, GL.GL_COMPILE_STATUS)
    if not status:
        print(GL.glGetShaderInfoLog(vertex_shader, 512, None))

    global shader_program
    shader_program = GL.glCreateProgram()
    GL.glAttachShader(shader_program, vertex_shader)
    GL.glAttachShader(shader_program, fragment_shader)
    GL.glLinkProgram(shader_program)

    GL.glDeleteShader(vertex_shader)
    GL.glDeleteShader(fragment_shader)


def resize(window, width, height):
    GL.glViewport(0, 0, width, height)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def render(window):
    # Render here
    GL.glClearColor(0.6, 0.6, 0.6, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    GL.glUseProgram(shader_program)
    GL.glActiveTexture(GL.GL_TEXTURE0)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture1)
    GL.glBindVertexArray(vao)
    GL.glDrawElements(GL.GL_TRIANGLES, 6, GL.GL_UNSIGNED_INT, None)
    GL.glBindVertexArray(0)


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

    initialize(window, w, h)

    while not glfw.window_should_close(window):
        process_input(window)
        render(window)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()

