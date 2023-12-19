# traffic_simulation.py
import pygame
import random
from button import Button
from car import Car
from traffic_light import TrafficLight


class TrafficSimulation:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.car_position_lane1 = 0
        self.car_position_lane2 = -width // 2
        self.semaphore_interval = 8000
        self.last_semaphore_change = pygame.time.get_ticks() # Tiempo en milisegundos
        self.is_green_left = False
        self.is_green_right = True
        self.is_green_top = False
        self.is_green_bottom = False
        self.lane1_cars = []
        self.lane2_cars = []
        self.lane3_cars = []
        self.lane4_cars = []
        self.car_generation_chance = 0.2
        self.traffic_light_left = TrafficLight(self.screen, 300, 130)
        self.traffic_light_right = TrafficLight(self.screen, 700, 325)
        self.traffic_light_top = TrafficLight(self.screen, 300, 325)
        self.traffic_light_bottom = TrafficLight(self.screen, 700, 130)
        self.font = pygame.font.Font(None, 36)
        self.restart_button = Button(screen, 100, height - 120, 120, 50, (0, 0, 255), "Restart", self.restart_game)
        self.pause_resume_button = Button(screen, 250, height - 120, 180, 50, (255, 165, 0), "Pause/Resume", self.toggle_pause)
        self.is_paused = False
        self.last_pause_toggle_time = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.main_clock = pygame.time.Clock()
        self.game_clock = pygame.time.Clock()
        self.delta_time = 0.0
        self.remaining_semaphore_time = self.semaphore_interval
        self.fase = 1
        

    def update(self):
        self.handle_events()
        self.delta_time = self.game_clock.tick(60) / 1000.0  
        if not self.is_paused:
            self.move_cars()
            self.update_traffic_lights()
            self.generate_cars()
        self.screen.fill((255, 255, 255))
        self.draw_bridge(0, self.height // 2 - 100, is_vertical=False)
        self.draw_bridge(self.width // 2 - 50, 0, is_vertical=True)
        self.traffic_light_left.change_color(self.is_green_left)
        self.traffic_light_right.change_color(self.is_green_right)
        self.traffic_light_top.change_color(self.is_green_top)
        self.traffic_light_bottom.change_color(self.is_green_bottom)
        self.draw_cars()
        self.draw_traffic_light_status()
        self.draw_instructions()
        self.restart_button.draw()
        self.pause_resume_button.draw()
        pygame.display.flip()
        self.main_clock.tick(60)  
        

    def draw_traffic_light_status(self):
        status_font = self.font.render(
            f"Left Light: {'Green' if self.is_green_left else 'Red'}   "
            f"Right Light: {'Green' if self.is_green_right else 'Red'}",
            True, (0, 0, 0)
        )

        status_font2 = self.font.render(
            f"Top Light: {'Green' if self.is_green_top else 'Red'}   "
            f"Bottom Light: {'Green' if self.is_green_bottom else 'Red'}",
            True, (0, 0, 0)
        )

        self.screen.blit(status_font, (10, 10))
        self.screen.blit(status_font2, (10, 40))

    def draw_instructions(self):
        instructions_font = self.font.render(
            "Press 'Q' to quit the game", True, (0, 0, 0)
        )
        self.screen.blit(instructions_font, (10, self.height - 40))

    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            # Pass events to the buttons
            self.restart_button.handle_event(event)
            self.pause_resume_button.handle_event(event)

    def quit_game(self):
        pygame.quit()
        quit()

    def restart_game(self):
        self.lane1_cars = []
        self.lane2_cars = []
        self.lane3_cars = []
        self.lane4_cars = []
        print("Game restarted")


    def toggle_pause(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pause_toggle_time >= 500:  
            self.is_paused = not self.is_paused
            self.last_pause_toggle_time = current_time
            print("Pause/Resume toggled. Is paused:", self.is_paused)
            if self.is_paused:
                self.game_clock.tick()

    def draw_bridge(self, x, y, is_vertical=True):
        if is_vertical:
            pygame.draw.rect(self.screen, (128, 128, 128), (x, 0, 100, self.height))
        else:
            pygame.draw.rect(self.screen, (128, 128, 128), (0, y, self.width, 100))

    def move_cars(self):
        # Mover los autos en la calle de la derecha

        for car in self.lane1_cars:
            if self.is_green_right or car not in self.lane1_cars[-3:]:
                car.position -= car.speed

            if not self.is_green_right and car.position < self.traffic_light_right.x and car not in self.lane1_cars[-3:]:
                car.position -= car.speed
            
            if self.is_green_right or car.position < self.traffic_light_right.x or car not in self.lane1_cars[-3:]:
                car.position -= car.speed

        # Mover los autos en la calle de la izquierda
                
        for car in self.lane2_cars:
            if self.is_green_left or car not in self.lane2_cars[-3:]:
                car.position += car.speed

            if not self.is_green_left and car.position > self.traffic_light_left.x and car not in self.lane2_cars[-3:]:
                car.position += car.speed

            if self.is_green_left or car.position > self.traffic_light_left.x or car not in self.lane2_cars[-3:]:
                car.position += car.speed

        # Mover los autos en la calle de arriba
                
        for car in self.lane3_cars:
            if self.is_green_bottom or car not in self.lane3_cars[-3:]:
                car.position += car.speed

            if not self.is_green_bottom and car.position < self.traffic_light_bottom.y and car not in self.lane3_cars[-3:]:
                car.position += car.speed

            if self.is_green_bottom or car.position > self.traffic_light_bottom.y or car not in self.lane3_cars[-3:]:
                car.position += car.speed

        # Mover los autos en la calle de abajo
                
        for car in self.lane4_cars:
            if self.is_green_top or car not in self.lane4_cars[-3:]:
                car.position -= car.speed

            if not self.is_green_top and car.position > self.traffic_light_top.y and car not in self.lane4_cars[-3:]:
                car.position -= car.speed

            if self.is_green_top or car.position < self.traffic_light_top.y or car not in self.lane4_cars[-3:]:
                car.position -= car.speed

        # Actualizar las listas de acuerdo con las nuevas posiciones
        self.lane1_cars = [car for car in self.lane1_cars if car.position > 0]
        self.lane2_cars = [car for car in self.lane2_cars if car.position < self.width]
        self.lane3_cars = [car for car in self.lane3_cars if car.position < self.height]
        self.lane4_cars = [car for car in self.lane4_cars if car.position > 0]

    def update_traffic_lights(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_semaphore_change >= self.semaphore_interval:
            self.last_semaphore_change = current_time

            if self.is_green_left and not self.is_green_right:
                # Izquierda verde, derecha rojo (8 segundos)
                #pasa a rojo/rojo
                self.is_green_left = False
                self.is_green_right = False
                self.is_green_bottom = True
                self.is_green_top = False

                self.semaphore_interval = 8000
                self.fase = 2
            elif not self.is_green_left and  not self.is_green_right:
                # Ambos rojos (5 segundos)
                if self.fase == 2:
                    #pasa a rojo/verde
                    self.is_green_left = False
                    self.is_green_right = True
                    self.is_green_bottom = False
                    self.is_green_top = False
                    self.semaphore_interval = 8000
                    self.fase = 3
                elif self.fase == 0:
                    #pasa a verde/rojo
                    self.is_green_left = True
                    self.is_green_right = False
                    self.is_green_top = False
                    self.is_green_bottom = False
                    self.semaphore_interval = 8000
                    self.fase = 1
            elif not self.is_green_left and self.is_green_right:
                # Izquierda rojo, derecha verde (5 segundos)
                #pasa a rojo/rojo
                self.is_green_left = False
                self.is_green_right = False
                self.is_green_top = True
                self.semaphore_interval = 8000
                self.fase = 0

            # Reiniciar el tiempo restante
            self.remaining_semaphore_time = self.semaphore_interval

        if not self.is_paused:
            self.remaining_semaphore_time -= self.delta_time * 1000  # Convertir segundos a milisegundos

            if self.remaining_semaphore_time <= 0:
                self.remaining_semaphore_time = self.semaphore_interval

    def generate_cars(self):

            min_distance = 50

            if not self.is_green_left and len(self.lane1_cars) < 3 and random.random() < self.car_generation_chance:
                if not self.lane1_cars or self.lane1_cars[-1].position < self.width - min_distance:
                    car_lane1 = Car(1)
                    car_lane1.position = self.width
                    self.lane1_cars.append(car_lane1)

            if not self.is_green_right and len(self.lane2_cars) < 5 and random.random() < self.car_generation_chance:
                if not self.lane2_cars or self.lane2_cars[-1].position > min_distance:
                    car_lane2 = Car(2)
                    car_lane2.position = 0
                    self.lane2_cars.append(car_lane2)

            #Generar autos en la calle de arriba
            if not self.is_green_top and len(self.lane3_cars) < 3 and random.random() < self.car_generation_chance:
                if not self.lane3_cars or self.lane3_cars[-1].position > min_distance:
                    car_lane3 = Car(3)
                    car_lane3.position = 0
                    self.lane3_cars.append(car_lane3)

            #Generar autos en la calle de abajo
            if not self.is_green_bottom and len(self.lane4_cars) < 3 and random.random() < self.car_generation_chance:
                if not self.lane4_cars or self.lane4_cars[-1].position < self.width - min_distance:
                    car_lane4 = Car(4)
                    car_lane4.position = self.width
                    self.lane4_cars.append(car_lane4)



    def draw_cars(self):
        for car in self.lane1_cars:
            car.draw_car(self.screen, car.position, self.height // 3 + 10, 0)

        for car in self.lane2_cars:
            car.draw_car(self.screen, car.position, self.height // 3 + 50, 180)

        # Dibuja los autos en la calle de arriba
        for car in self.lane3_cars:
            car.draw_car(self.screen, self.width // 3 + 120, car.position, 90)

        # Dibuja los autos en la calle de abajo
        for car in self.lane4_cars:
            car.draw_car(self.screen, self.width // 3 + 190, car.position, 270)
