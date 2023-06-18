import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
import math
import time

# Инициализация Pygame
pygame.init()

# Создание окна
width, height = 1200, 900
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

# Загрузка текстуры
texture = pygame.image.load("texture.jpg")  # Замените "texture.png" на путь к вашему изображению
texture_data = pygame.image.tostring(texture, "RGBA", 1)

# Создание шейдеров
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

# Создание вершинного буфера и настройка вершинных данных
vertex_data = np.array([
    -1, -1, 0, 0,
    -1, 1, 0, 1,
    1, 1, 1, 1,
    1, -1, 1, 0
], dtype=np.float32)
vertex_buffer = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

# Создание индексного буфера и настройка индексных данных
index_data = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
index_buffer = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

# Настройка атрибутов вершинного шейдера
position_loc = glGetAttribLocation(shader_program, "position")
texcoord_loc = glGetAttribLocation(shader_program, "texcoord")
glEnableVertexAttribArray(position_loc)
glEnableVertexAttribArray(texcoord_loc)
glVertexAttribPointer(position_loc, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
glVertexAttribPointer(texcoord_loc, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))

# Создание и настройка текстуры
texture_id = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture_id)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture.get_width(), texture.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE,
             texture_data)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# Создание объекта для отслеживания времени
clock = pygame.time.Clock()


# Бесконечный цикл для отрисовки
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка буфера
    glClear(GL_COLOR_BUFFER_BIT)

    # Использование шейдеров
    glUseProgram(shader_program)

    # Активация текстурного юнита и привязка текстуры
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glUniform1i(glGetUniformLocation(shader_program, "texture_sampler"), 0)

    # Отрисовка треугольников
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    # Отображение FPS
    fps = clock.get_fps()

    fps_str = str(round(fps))

    pygame.display.set_caption(f"FPS: {fps_str}")



    # Обновление экрана
    pygame.display.flip()

    # Обновление времени
    clock.tick()

# Завершение работы Pygame
pygame.quit()
