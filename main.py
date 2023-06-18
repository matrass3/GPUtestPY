import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
import math

pygame.init()

width, height = 1200, 900
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)

vertex_shader = """
#version 330
in vec2 position;
out vec2 frag_texcoord;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    frag_texcoord = (position + vec2(1.0)) / 2.0;  // Преобразуем положение вершины в текстурные координаты
}
"""

fragment_shader = """
#version 330
in vec2 frag_texcoord;
out vec4 frag_color;
uniform float time;

void main()
{
    float speed = 1.0;  // Скорость изменения цвета
    float r = (sin(time * speed) + 1.0) * 0.5;  // Изменение красного компонента
    float g = (cos(time * speed) + 1.0) * 0.5;  // Изменение зеленого компонента
    float b = (sin(time * speed * 0.7) + 1.0) * 0.5;  // Изменение синего компонента

    frag_color = vec4(r, g, b, 1.0);  // Устанавливаем цвет фрагмента
}
"""

shader_program = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

vertex_data = np.array([
    -1, -1,
    -1, 1,
    1, 1,
    1, -1
], dtype=np.float32)
vertex_buffer = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

index_data = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)
index_buffer = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, index_buffer)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

position_loc = glGetAttribLocation(shader_program, "position")

glEnableVertexAttribArray(position_loc)
glVertexAttribPointer(position_loc, 2, GL_FLOAT, GL_FALSE, 8, ctypes.c_void_p(0))

time_loc = glGetUniformLocation(shader_program, "time")

clock = pygame.time.Clock()
fps_update_interval = 1000  # Интервал обновления FPS в миллисекундах
fps_timer = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(shader_program)
    glUniform1f(time_loc, pygame.time.get_ticks() / 1000.0)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    pygame.display.flip()

    # Обновляем FPS раз в секунду
    current_time = pygame.time.get_ticks()
    if current_time - fps_timer >= fps_update_interval:
        fps = clock.get_fps()
        pygame.display.set_caption(f"OpenGL Example | FPS: {int(fps)}")
        fps_timer = current_time

    clock.tick()

pygame.quit()
