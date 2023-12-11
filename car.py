# car.py

import random
import pygame as pg
from Constants.constants import CARS_IMAGES


class Car:
    
    def __init__(self, lane):
        self.car_name = random.choice(list(CARS_IMAGES.keys()))
        self.image = pg.image.load(CARS_IMAGES[self.car_name])
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.position = 0
        self.speed = 5
        self.visible = True
        self.stop = False
        self.car = pg.transform.scale(self.image, (self.width // 2, self.height // 2))
        # ###########
        # self.stop_position = 0
        # self.distance_to_stop = 30
        # self.lane = lane
        # ###########

    def draw_car(self, screen, x, y, angle):
        if self.visible:

            # if not self.stop and angle == 180:
                
            #     if self.position > self.stop_position:
            #         self.position -= self.speed

            # if self.stop and self.lane == 2:  
            #     print("Carro en lane2 se detiene")
            #     if self.position < self.stop_position:
            #         self.position += self.speed
            #         print("Carro en lane2 se mueve")
            car = pg.transform.rotate(self.car, angle)
            screen.blit(car, (x, y))

    