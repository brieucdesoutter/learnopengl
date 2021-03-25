from OpenGL import GL


class Shader:
    def __init__(self, shader_type, src_path, **kwargs):
        self.ID = GL.glCreateShader(shader_type)
        with open(src_path) as shader_src:
            src = shader_src.read()
        if kwargs:
            src = src.format(**kwargs)
        GL.glShaderSource(self.ID, src, None)
        GL.glCompileShader(self.ID)
        status = GL.glGetShaderiv(self.ID, GL.GL_COMPILE_STATUS)
        if not status:
            raise Exception(GL.glGetShaderInfoLog(self.ID, 512, None))

    def delete(self):
        if self.ID:
            GL.glDeleteShader(self.ID)
            self.ID = 0


class ShaderProgram:
    def __init__(self, *args):
        self._ID = GL.glCreateProgram()
        for shader in args:
            GL.glAttachShader(self._ID, shader.ID)
        GL.glLinkProgram(self._ID)
        status = GL.glGetProgramiv(self._ID, GL.GL_LINK_STATUS)
        if not status:
            raise Exception(GL.glGetProgramInfoLog(self._ID, 512, None))

    def use(self):
        GL.glUseProgram(self._ID)

    def set_bool(self, name, value):
        GL.glUniform1i(GL.glGetUniformLocation(self._ID, name), value)

    def set_float(self, name, value):
        GL.glUniform1f(GL.glGetUniformLocation(self._ID, name), value)

    def set_float4(self, name, x, y, z, w):
        GL.glUniform4f(GL.glGetUniformLocation(self._ID, name), x, y, z, w)
