import pygame
from pygame.locals import *
import random

pygame.init()

# Cargar imágenes
luz_roja = pygame.image.load("images/luz_roja.png")
luz_verde = pygame.image.load("images/luz_verde.png")
roja_apagada = pygame.image.load("images/luz_roja_apagada.png")
semaforo = pygame.image.load("images/semaforo.png")
verde_apagada = pygame.image.load("images/luz_verde_apagada.png")
carro_negro = pygame.image.load("images/carro_negro.png")
carro_rojo = pygame.image.load("images/carro_rojo.png")
carros = [carro_negro, carro_rojo]

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Simulación de Tráfico')

bridge_width = 200
car_width = carros[0].get_width() 
car_height = carros[0].get_height()
car_speed = 5
car_position_lane1 = 0
car_position_lane2 = -width // 2

# Variables para el control del semáforo y carros
semaphore_interval = 5000  # milisegundos
last_semaphore_change = pygame.time.get_ticks()
is_green_left = False
is_green_right = True
lane1_cars = []
lane2_cars = []
car_generation_chance = 0.05  # Probabilidad de generar un nuevo carro en cada iteración

def draw_bridge(y):
    pygame.draw.rect(screen, (128, 128, 128), (0, y, width, 100))

def draw_car(x, y, angle):
    
    rotated_and_scaled_image = pygame.transform.scale(pygame.transform.rotate(carro_negro, angle), (car_width * 1.5, car_height * 1.5))
    screen.blit(rotated_and_scaled_image, (x, y))  

def draw_traffic_light(x, y, is_green):
    #redimensionar imagenes
    green_light = pygame.transform.scale(luz_verde, (15, 15))
    red_light = pygame.transform.scale(luz_roja, (15, 15))
    red_light_off = pygame.transform.scale(roja_apagada, (15, 15))
    green_light_off = pygame.transform.scale(verde_apagada, (15, 15))

    screen.blit(semaforo, (width // 4.5, height // 4.5))
    screen.blit(semaforo, (3 * width // 4 - 22, height // 4.5))

    if is_green:
        screen.blit(red_light_off, (x // 4 - 5, y // 4 - 10))
        screen.blit(green_light, (x // 4 - 5, y // 3.6 - 10))
    else:
        screen.blit(red_light, (x // 4 - 5, y // 4 - 10))
        screen.blit(green_light_off, (x // 4 - 5, y // 3.6 - 10))

def draw_light(x, y):
    screen.blit(semaforo, (x, y))

def generate_car(lane):
    #random_car = random.choice(carros)
    min_distance_between_cars = 50  # Ajusta la distancia mínima entre carros
    if lane == 1 and (not lane1_cars or lane1_cars[-1] < width - min_distance_between_cars):
        lane1_cars.append(width)
    elif lane == 2 and (not lane2_cars or lane2_cars[-1] > min_distance_between_cars ):
        lane2_cars.append(0)


def move_cars():
    global lane1_cars, lane2_cars
    lane1_cars = [x - car_speed for x in lane1_cars]
    lane2_cars = [x + car_speed for x in lane2_cars]
    lane1_cars = [x for x in lane1_cars if x > 0]
    lane2_cars = [x for x in lane2_cars if x < width]

def draw_cars():
    
    for x in lane1_cars:
        draw_car(x, height // 3 + 10, 90)
    for x in lane2_cars:
        draw_car(x, height // 3 + 50, 270)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

    # Control de movimiento del coche
    car_position_lane1 += car_speed
    if car_position_lane1 > width:
        car_position_lane1 = -car_width

    car_position_lane2 += car_speed
    if car_position_lane2 > width:
        car_position_lane2 = -car_width

    # Control del semáforo
    current_time = pygame.time.get_ticks()
    if current_time - last_semaphore_change >= semaphore_interval:
        last_semaphore_change = current_time
        is_green_left = not is_green_left
        is_green_right = not is_green_right

    # Generación de carros
    if not is_green_left and random.random() < car_generation_chance:
        generate_car(1)

    if not is_green_right and random.random() < car_generation_chance:
        generate_car(2)

    # Movimiento de carros
    move_cars()

    screen.fill((255, 255, 255))

    draw_bridge(height // 2 - 100)
    draw_traffic_light(width, height, is_green_left)
    draw_traffic_light(3 * width, height, is_green_right)
    draw_cars()

    pygame.display.flip()

    pygame.time.Clock().tick(30)
