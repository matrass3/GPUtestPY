import pygame
import random

# Инициализация Pygame
pygame.init()

# Создание окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GPU Load")

# Определение цветовой палитры
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Пример палитры из трех цветов: красный, зеленый, синий

# Создание объекта для отслеживания времени
clock = pygame.time.Clock()

# Бесконечный цикл для отрисовки
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Генерация случайного индекса цвета из палитры
    color_index = random.randint(0, len(colors) - 1)
    color = colors[color_index]

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отрисовка прямоугольника на экране с случайным цветом
    pygame.draw.rect(screen, color, (0, 0, width, height))

    # Отображение FPS
    fps = int(clock.get_fps())
    font = pygame.font.Font(None, 36)
    fps_text = font.render("FPS: " + str(fps), True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()

    # Ограничение FPS до 60
    clock.tick(60)

# Завершение работы Pygame
pygame.quit()
