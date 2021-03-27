import numpy as np
from OpenGL import GL
from PIL import Image


class Texture2D:
    def __init__(self, image_file, flip_y=False, unit=GL.GL_TEXTURE0, wrap_s=GL.GL_REPEAT, wrap_t=GL.GL_REPEAT, min_filter=GL.GL_LINEAR, max_filter=GL.GL_LINEAR, generate_mipmaps=True):
        self._ID = GL.glGenTextures(1)
        self._unit = unit
        GL.glActiveTexture(self._unit)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._ID)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap_s)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap_t)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, min_filter)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, max_filter)

        im = Image.open(image_file)
        if im.mode == 'RGBA':
            internal_format = GL.GL_RGBA8
            image_format = GL.GL_RGBA
        else:
            im = im.convert('RGB')
            internal_format = GL.GL_RGB8
            image_format = GL.GL_RGB
        if flip_y:
            im = im.transpose(Image.FLIP_TOP_BOTTOM)
        width, height = im.size
        tex_bytes = np.array(im)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, internal_format, width, height, 0, image_format, GL.GL_UNSIGNED_BYTE, tex_bytes)
        if generate_mipmaps:
            GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

    def use(self):
        GL.glActiveTexture(self._unit)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._ID)
