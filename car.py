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

    def draw_car(self, screen, x, y, angle):
        if self.visible:
            car = pg.transform.rotate(self.car, angle)
            screen.blit(car, (x, y))

    