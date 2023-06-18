import pygame
import random

# Инициализация Pygame
pygame.init()

# Создание окна
width, height = 1200, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GPU Load")

# Бесконечный цикл для отрисовки
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Генерация случайного цвета
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = (r, g, b)

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отрисовка прямоугольника на экране с случайным цветом
    pygame.draw.rect(screen, color, (0, 0, width, height))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
