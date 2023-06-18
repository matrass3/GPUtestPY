import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
import math

pygame.init()

width, height = 1200, 900
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
texture = pygame.image.load("texture.jpg")  # Замените "texture.png" на путь к вашему изображению
texture_data = pygame.image.tostring(texture, "RGBA", 1)

vertex_shader = """
#version 330
in vec2 position;
in vec2 texcoord;
out vec2 frag_texcoord;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    frag_texcoord = texcoord;
}
"""

fragment_shader = """
#version 330
in vec2 frag_texcoord;
uniform sampler2D texture_sampler;
out vec4 frag_color;
void main()
{
    frag_color = texture(texture_sampler, frag_texcoord);
}
"""

shader_program = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

vertex_data = np.array([
    -1, -1, 0, 0,
    -1, 1, 0, 1,
    1, 1, 1, 1,
    1, -1, 1, 0
], dtype=np.float32)
vertex_buffer = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

index_data = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
index_buffer = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

position_loc = glGetAttribLocation(shader_program, "position")
texcoord_loc = glGetAttribLocation(shader_program, "texcoord")
glEnableVertexAttribArray(position_loc)
glEnableVertexAttribArray(texcoord_loc)
glVertexAttribPointer(position_loc, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
glVertexAttribPointer(texcoord_loc, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))

texture_id = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture_id)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture.get_width(), texture.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE,
             texture_data)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


clock = pygame.time.Clock()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(shader_program)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glUniform1i(glGetUniformLocation(shader_program, "texture_sampler"), 0)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    fps = clock.get_fps()
    fps_str = str(round(fps))
    pygame.display.set_caption(f"FPS: {fps_str}")
    pygame.display.flip()
    clock.tick()

pygame.quit()
