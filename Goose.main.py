import random
import os

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

FONT = pygame.font.SysFont("Verdana", 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)

main_display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bg = pygame.transform.scale(pygame.image.load("background.png"),(SCREEN_WIDTH, SCREEN_HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3


ENEMY_IMAGE = pygame.image.load('enemy.png').convert_alpha()
BONUS_IMAGE = pygame.image.load('bonus.png').convert_alpha()
IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)


player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha() #pygame.Surface(player_size)
# player.fill(COLOR_BLACK)
player_rect = player.get_rect(center=(100, 300))
# player_rect.top = 1
# player_rect.left = 1
# player_speed = [1, 1]
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]


def create_enemy(width: int, height: int, offset: int):
# Определяем координаты 
    object_x = SCREEN_WIDTH
    object_y_min = offset
    object_y_max = SCREEN_HEIGHT - height - offset
    object_y = random.randint(object_y_min, object_y_max)
# Создаем физический обьект
    physical_object = pygame.Rect(object_x, object_y, width, height)
# Задаем вектор движения физического обьекта
    physical_object_move_vector = [random.randint(-6, -3), 0]
# Создаем графический обьект
    graphic_object = pygame.transform.scale(ENEMY_IMAGE, (width, height))
# Возвращаем результат
    return [graphic_object, physical_object, physical_object_move_vector]

def create_bonus(width: int, height: int, offset: int):
# Определяем координаты 
    object_x_min = offset
    object_x_max = SCREEN_WIDTH - width - offset
    object_x = random.randint(object_x_min, object_x_max)
    object_y = 0
# Создаем физический обьект
    physical_object = pygame.Rect(object_x, object_y, width, height)
# Задаем вектор движения физического обьекта
    physical_object_move_vector_x = 0
    physical_object_move_vector_y = random.randint(1, 8)
    physical_object_move_vector = [physical_object_move_vector_x, physical_object_move_vector_y]
# Создаем графический обьект
    graphic_object = pygame.transform.scale(BONUS_IMAGE, (width, height))
# Возвращаем результат
    return [graphic_object, physical_object, physical_object_move_vector]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0

image_index = 0

playing = True

while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy(100, 50, 20))
            enemies.append(create_enemy(50, 20, 20))
            bonuses.append(create_bonus(150, 270, 70))
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0   

    # main_display.fill(COLOR_BLACK)
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < SCREEN_HEIGHT:
        player_rect = player_rect.move(player_move_down)
    
    if keys[K_RIGHT] and player_rect.right < SCREEN_WIDTH:
        player_rect = player_rect.move(player_move_right)
    
    if keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(player_move_up)
    
    if keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (SCREEN_WIDTH-50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > SCREEN_HEIGHT:
            bonuses.pop(bonuses.index(bonus))