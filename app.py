import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *


pygame.init()


width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
glOrtho(0, width, 0, height, -1, 1)
glClearColor(0.7, 0.7, 1.0, 1.0) 


bridge_width = 200
car_width = 50
car_speed = 5
car_position_lane1 = 0
car_position_lane2 = -width // 2


def draw_bridge(y):
    glColor3f(0.5, 0.5, 0.5) 
    glBegin(GL_QUADS)
    glVertex2f(0, y)
    glVertex2f(width, y)
    glVertex2f(width, y + 50)
    glVertex2f(0, y + 50)
    glEnd()


def draw_car(x, y):
    glColor3f(1.0, 0.0, 0.0)  
    glBegin(GL_QUADS)
    glVertex2f(x, y + 10)
    glVertex2f(x + car_width, y + 10)
    glVertex2f(x + car_width, y + 40)
    glVertex2f(x, y + 40)
    glEnd()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    
    car_position_lane1 += car_speed
    if car_position_lane1 > width:
        car_position_lane1 = -car_width

    car_position_lane2 += car_speed
    if car_position_lane2 > width:
        car_position_lane2 = -car_width

    
    glClear(GL_COLOR_BUFFER_BIT)

    
    draw_bridge(height // 2)
    draw_car(car_position_lane1, height // 2)

    
    draw_bridge(height // 2 - 100)
    draw_car(car_position_lane2, height // 2 - 100)

    
    pygame.display.flip()

    
    pygame.time.Clock().tick(30)
