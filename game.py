import pygame
from pygame.locals import *
from random import randint
from sys import exit

pygame.init()

width = 800
height = 600

player_imgs = [pygame.image.load(f'player_{i}.png') for i in range(8)]
player_imgs = [pygame.transform.scale(image, (100, 100)) for image in player_imgs]

# Player:
player_x = int(width / 4)
player_y = height - 120
player_width = 100
player_height = 100
jump_height = 15
gravity = 1
y_velocity = 0
x_velocity = 1
jumping = False

# Animação
player_speed_img = 0.3
player_counter = 0 

# Chão
floor_width = width
floor_height = 20
floor_y = height - floor_height

# Obstáculos:
obstacle_width = 20
obstacle_height = 20
x_obs = randint(0, width)
y_obs = floor_y - obstacle_height
obs_speed = 1.5

# Pontuação do Player:
pontos = 0

font = pygame.font.SysFont('arial', 40, bold=True, italic=True)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

died = False

def player_move():
    global player_x, player_y, y_velocity, jumping
    
    if jumping:
        y_velocity += gravity
        player_y += y_velocity
        
        # Verificar se o jogador atingiu o chão
        if player_y >= floor_y - player_height:
            player_y = floor_y - player_height
            jumping = False
            y_velocity = 0

def move_obstacles_1():
    global x_obs, pontos, obs_speed

    x_obs -= obs_speed

    if x_obs < -obstacle_width:
        x_obs = width + randint(0, 400)
        pontos += 1
        obs_speed += 0.25


while True:
    clock.tick(60)
    screen.fill((255, 255, 255))

    distancia_msg = f'Distancia: {pontos}'
    texto_formatado = font.render(distancia_msg, True, (0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            if event.key == K_w and not jumping:
                jumping = True
                y_velocity = -jump_height

    player_move()
    move_obstacles_1()

    player_counter += player_speed_img
    if player_counter >= len(player_imgs):
        player_counter = 0
    player_index = int(player_counter)
    
    player = screen.blit(player_imgs[player_index], (player_x, player_y))

    floor = pygame.draw.rect(screen, (124, 252, 0), (0, floor_y, floor_width, floor_height))

    obstacle = pygame.draw.rect(screen, (255, 0, 0), (x_obs, y_obs, obstacle_width, obstacle_height))

    if player.colliderect(obstacle):
        print('Game Over')
        pygame.quit()
        exit()

    screen.blit(texto_formatado, (450, 50))

    pygame.display.update()
