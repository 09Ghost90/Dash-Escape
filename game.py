import pygame
from pygame.locals import *
from random import randint
from sys import exit

pygame.init()

width = 800
height = 600

# Player:
player_x = int(width/4)
player_y = int(height/4)
player_width = 20
player_height = 20

speed_player = 0
x_controle = speed_player
y_controle = 0

# Chão
floor_width = 0
floor_height = 0

# Obstaculos:
x_obs = randint(0, width)
y_obs = 570

# Pontuação do Player:
pontos = 0

font = pygame.font.SysFont('arial', 40, bold=True, italic=True)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

died = False

# def died():
#     if player_x and player_y == pos_obstaculo

def player_move():
    global player_x, player_y, x_controle, y_controle
    player_x += x_controle
    player_y += y_controle

while True:
    clock.tick(120)
    screen.fill((255, 255, 255))

    distancia_msg = f'Distancia: {pontos}'
    texto_formatado = font.render(distancia_msg, True, (0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == KEYDOWN:
            if event.key  == K_d:
                x_coontrole = speed_player + 10
                y_controle = 0
                player_move()
            if event.key == K_a:
                x_controle = -speed_player - 10
                y_controle = 0
                player_move()
            
    

    player = pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, player_width, player_height))
    
    for _ in range(10):
        floor = pygame.draw.rect(screen, (124, 252, 0), (0, 500, floor_width, floor_height))
        floor_width += 100
        floor_height += 100

    obstacle = pygame.draw.rect(screen, (255, 0, 0), (x_obs, y_obs, 20, 20))

    if player.colliderect(obstacle):
        print('Game Over')
        pygame.quit()
        exit()

    screen.blit(texto_formatado, (450, 50))

    pygame.display.update()





