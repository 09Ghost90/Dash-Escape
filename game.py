import pygame
from pygame.locals import *
from random import randint
from sys import exit

pygame.init()

width = 800
height = 600

player_imgs = [pygame.image.load(f'imagens//player_{i}.png') for i in range(8)]
player_imgs = [pygame.transform.scale(image, (100, 100)) for image in player_imgs]

bg_img = pygame.image.load('bg_imagens//bg.png')
bg_img = pygame.transform.scale(bg_img, (width, height))

# Player:
player_x = int(width / 4)
player_y = height - 120
player_width = 80  
player_height = 85 
jump_height = 15
gravity = 1
y_velocity = 0
x_velocity = 1
jumping = False
attacking = False
attacking_flyers = False

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
x_obs = randint(400, width)
y_obs = floor_y - obstacle_height
obs_speed = 4

# Obstáculos Voadores:
height_obs_flyers = 20

obstacles_flyers_width = 30
obstacle_flyers_height = 20
x_obs_flyers = randint(400, width)
y_obs_flyers = floor_y - obstacle_flyers_height - height_obs_flyers
obs_speed_flyers = 2

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
        
        if player_y >= floor_y - player_height:
            player_y = floor_y - player_height
            jumping = False
            y_velocity = 0

def player_attack():
    global attacking, x_obs

    attack_rect = pygame.Rect(player_x + player_width, player_y, 50, player_height)

    if attack_rect.colliderect(pygame.Rect(x_obs, y_obs, obstacle_width, obstacle_height)):
        x_obs = width + randint(0, 400)
        attacking = False

def player_attack_flyers():
    global attacking_flyers, x_obs_flyers

    attack_flyers_rect = pygame.Rect(player_x + player_width, player_y, 50, player_height)

    if attack_flyers_rect.colliderect(pygame.Rect(x_obs_flyers, y_obs_flyers, obstacles_flyers_width, obstacle_flyers_height)):
        x_obs_flyers = width + randint(0, 400)
        attacking_flyers = False

def move_obstacles():
    global x_obs, pontos, obs_speed

    x_obs -= obs_speed

    if x_obs < -obstacle_width:
        x_obs = width + randint(0, 400)
        pontos += 1
        obs_speed += 0.25

def move_obstacles_flyers():
    global x_obs_flyers, pontos, obs_speed_flyers

    x_obs_flyers -= obs_speed_flyers  # Corrigido aqui

    if x_obs_flyers < -obstacles_flyers_width:
        x_obs_flyers = width + randint(0, 400)
        pontos += 1
        obs_speed_flyers += 0.25

def check_collision(player_x, player_y, player_width, player_height, x_obs, y_obs, obstacle_width, obstacle_height, margin=5):
    if (player_x + margin < x_obs + obstacle_width and
        player_x + player_width - margin > x_obs and
        player_y + margin < y_obs + obstacle_height and
        player_y + player_height - margin > y_obs):
        return True
    return False

def check_collision_flyers(player_x, player_y, player_width, player_height, x_obs_flyers, y_obs_flyers, obstacle_flyers_width, obstacle_flyers_height, margin=5):
    if (player_x + margin < x_obs_flyers + obstacle_flyers_width and
        player_x + player_width - margin > x_obs_flyers and
        player_y + margin < y_obs_flyers + obstacle_flyers_height and
        player_y + player_height - margin > y_obs_flyers):
        return True
    return False

while True:
    clock.tick(60)
    screen.blit(bg_img, (0, 0))

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
            elif event.key == K_SPACE and not attacking:
                attacking = True
            elif event.key == K_f and not attacking:
                attacking_flyers = True

    player_move()
    move_obstacles()
    move_obstacles_flyers()

    player_counter += player_speed_img
    if player_counter >= len(player_imgs):
        player_counter = 0
    player_index = int(player_counter)
    
    # Atualizar a posição do jogador e criar a "hit box"
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    screen.blit(player_imgs[player_index], (player_x, player_y))

    floor = pygame.draw.rect(screen, (124, 252, 0), (0, floor_y, floor_width, floor_height))

    obstacle_rect = pygame.Rect(x_obs, y_obs, obstacle_width, obstacle_height)
    pygame.draw.rect(screen, (255, 0, 0), obstacle_rect)

    obstacle_flyers_rect = pygame.Rect(x_obs_flyers, y_obs_flyers, obstacles_flyers_width, obstacle_flyers_height)
    pygame.draw.rect(screen, (0, 0, 255), obstacle_flyers_rect)

    if attacking:
        player_attack()
        attack_rect = pygame.Rect(player_x + player_width, player_y, 50, player_height)
        pygame.draw.rect(screen, (255, 255, 0), attack_rect)

    if attacking_flyers:
        player_attack_flyers()
        attack_flayers_rect = pygame.Rect(player_x + player_width, player_y, 50, player_height)
        pygame.draw.rect(screen, (255, 0, 255), attack_flayers_rect)
        
    # Verificar colisão com margem de erro
    if check_collision(player_x, player_y, player_width, player_height, x_obs, y_obs, obstacle_width, obstacle_height) or check_collision_flyers(player_x, player_y, player_width, player_height, x_obs_flyers, y_obs_flyers, obstacles_flyers_width, obstacle_flyers_height):
        print('Game Over')
        pygame.quit()
        exit()

    screen.blit(texto_formatado, (450, 50))

    pygame.display.update()
