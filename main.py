import pygame
import random

# Инициализация Pygame
pygame.init()

# Создание окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GPU Load")

# Загрузка текстуры
texture = pygame.image.load("texture.jpg")  # Замените "texture.png" на путь к вашему изображению

# Создание поверхности для рендеринга с более высоким разрешением
render_width, render_height = 1600, 1200
if texture.get_width() > render_width or texture.get_height() > render_height:
    scale_factor = min(render_width / texture.get_width(), render_height / texture.get_height())
    texture = pygame.transform.scale(texture, (int(texture.get_width() * scale_factor),
                                               int(texture.get_height() * scale_factor)))
    render_width, render_height = texture.get_width(), texture.get_height()

render_surface = pygame.Surface((render_width, render_height))

# Создание объекта для отслеживания времени
clock = pygame.time.Clock()

# Бесконечный цикл для отрисовки
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Генерация случайных координат для отображения текстуры
    x = random.randint(0, render_width - texture.get_width())
    y = random.randint(0, render_height - texture.get_height())

    # Очистка поверхности для рендеринга
    render_surface.fill((0, 0, 0))

    # Отрисовка текстуры на поверхности для рендеринга
    render_surface.blit(texture, (x, y))

    # Масштабирование поверхности для рендеринга до размеров окна
    scaled_surface = pygame.transform.scale(render_surface, (width, height))

    # Отображение поверхности для рендеринга на экране
    screen.blit(scaled_surface, (0, 0))

    # Отображение FPS
    fps = int(clock.get_fps())
    font = pygame.font.Font(None, 36)
    fps_text = font.render("FPS: " + str(fps), True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()

    # Обновление времени
    clock.tick()

# Завершение работы Pygame
pygame.quit()
