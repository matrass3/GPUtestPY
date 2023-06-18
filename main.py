import pygame
import random
# Инициализация Pygame
pygame.init()

# Создание окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GPU Load")

# Бесконечный цикл для отрисовки
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Отрисовка прямоугольника на экране
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, width, height))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
