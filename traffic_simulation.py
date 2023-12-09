# traffic_simulation.py
import pygame
import random
from car import Car
from traffic_light import TrafficLight



class TrafficSimulation:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        #self.car_speed = 5
        self.car_position_lane1 = 0
        self.car_position_lane2 = -width // 2
        self.semaphore_interval = 5000
        self.last_semaphore_change = pygame.time.get_ticks()
        self.is_green_left = False
        self.is_green_right = True
        self.lane1_cars = []
        self.lane2_cars = []
        self.car_generation_chance = 0.2
        self.traffic_light_left = TrafficLight(self.screen, 200, 130 )
        self.traffic_light_right = TrafficLight(self.screen, 600, 130)
        

    def update(self):

        #self.handle_events()
        self.move_cars()
        self.update_traffic_lights()
        self.generate_cars()
        self.remove_invisible_cars()
        self.screen.fill((255, 255, 255))
        self.draw_bridge(self.height // 2 - 100)
        self.traffic_light_left.change_color(self.is_green_left)
        self.traffic_light_right.change_color(self.is_green_right)
        self.draw_cars()
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    # def handle_events(self):
    #     pass  # Handle events if needed

    def draw_bridge(self, y):
        pygame.draw.rect(self.screen, (128, 128, 128), (0, y, self.width, 100))

    def move_cars(self):
        for car in self.lane1_cars:
            car.position -= car.speed
            #print("1--",car.position)
            if car.position + car.width < 0:
                car.hide()
                print("se esconde")

        for car in self.lane2_cars:
            car.position += car.speed
            #print("2--",car.position)
            if car.position > self.width:
                car.hide()
                print("se esconde")


        # Actualizar las listas de acuerdo con las nuevas posiciones
        self.lane1_cars = [car for car in self.lane1_cars if car.position > 0]
        self.lane2_cars = [car for car in self.lane2_cars if car.position < self.width]

    def update_traffic_lights(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_semaphore_change >= self.semaphore_interval:
            self.last_semaphore_change = current_time
            self.is_green_left = not self.is_green_left
            self.is_green_right = not self.is_green_right

    def generate_cars(self):

        min_distance = 50
        if not self.is_green_left and random.random() < self.car_generation_chance:
            if not self.lane1_cars or self.lane1_cars[-1].position < self.width - min_distance:
                car_lane1 = Car()
                car_lane1.position = self.width
                #print(car_lane1.position)
                self.lane1_cars.append(car_lane1)

        if not self.is_green_right and random.random() < self.car_generation_chance:
            if not self.lane2_cars or self.lane2_cars[-1].position > min_distance:
                car_lane2 = Car()
                car_lane2.position = 0
                self.lane2_cars.append(car_lane2)



    def draw_cars(self):
        for car in self.lane1_cars:
            car.draw_car(self.screen, car.position, self.height // 3 + 10, 0)
            #print(car.position)
            

        for car in self.lane2_cars:
            car.draw_car(self.screen, car.position, self.height // 3 + 50, 180)
            #print(car.position)
    
    def remove_invisible_cars(self):
        self.lane1_cars = [car for car in self.lane1_cars if car.is_visible()]
        self.lane2_cars = [car for car in self.lane2_cars if car.is_visible()]