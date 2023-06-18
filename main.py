import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
import random

pygame.init()

width, height = 1200, 900
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("блять сука нахуй ебать")

vertex_shader = """
#version 330
in vec2 position;
out vec2 frag_texcoord;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    frag_texcoord = (position + vec2(1.0)) / 2.0;
}
"""

fragment_shader = """
#version 330
in vec2 frag_texcoord;
out vec4 frag_color;
uniform float time;

float random(float seed) {
    return fract(sin(seed) * 43758.5453);
}

vec3 randomColor(float seed) {
    return vec3(random(seed), random(seed + 1.0), random(seed + 2.0));
}

void main()
{
    vec2 center = vec2(0.5);
    float radius = 0.5;

    float distance = length(frag_texcoord - center);
    float gradient = smoothstep(radius - 0.02, radius + 0.02, distance);

    float transitionSpeed = 0.001; // Скорость перехода между цветами

    float seed1 = floor(time * transitionSpeed);
    float seed2 = seed1 + 1.0;

    vec3 color1 = randomColor(seed1);
    vec3 color2 = randomColor(seed2);

    vec3 finalColor = mix(color1, color2, gradient);

    frag_color = vec4(finalColor, 1.0);
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
time_loc = glGetUniformLocation(shader_program, "time")

glEnableVertexAttribArray(position_loc)
glVertexAttribPointer(position_loc, 2, GL_FLOAT, GL_FALSE, 0, None)

glClearColor(0.0, 0.0, 0.0, 1.0)
glViewport(0, 0, width, height)

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    _time = (pygame.time.get_ticks() - start_time) / 1000.0
    glUseProgram(shader_program)
    glUniform1f(time_loc, _time)

    glClear(GL_COLOR_BUFFER_BIT)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    pygame.display.set_caption(f"блять сука нахуй (FPS: {clock.get_fps():.2f})")
    pygame.display.flip()
    clock.tick(1000000)
