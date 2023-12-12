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
        self.semaphore_interval = 8000#2000
        self.last_semaphore_change = pygame.time.get_ticks() # Tiempo en milisegundos
        self.is_green_left = True
        self.is_green_right = False
        self.lane1_cars = []
        self.lane2_cars = []
        self.car_generation_chance = 0.2
        self.traffic_light_left = TrafficLight(self.screen, 300, 130 )
        self.traffic_light_right = TrafficLight(self.screen, 700, 130)
        self.font = pygame.font.Font(None, 36)
        self.restart_button = Button(screen, 100, height - 120, 120, 50, (0, 0, 255), "Restart", self.restart_game)
        self.pause_resume_button = Button(screen,250, height - 120, 180, 50, (255, 165, 0), "Pause/Resume", self.toggle_pause)
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
        self.draw_bridge(self.height // 2 - 100)
        self.traffic_light_left.change_color(self.is_green_left)
        self.traffic_light_right.change_color(self.is_green_right)
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
        self.screen.blit(status_font, (10, 10))

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
        print("Game restarted")


    def toggle_pause(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pause_toggle_time >= 500:  
            self.is_paused = not self.is_paused
            self.last_pause_toggle_time = current_time
            print("Pause/Resume toggled. Is paused:", self.is_paused)
            if self.is_paused:
                self.game_clock.tick() 

    def draw_bridge(self, y):
        pygame.draw.rect(self.screen, (128, 128, 128), (0, y, self.width, 100))

    def move_cars(self):
        for car in self.lane1_cars:
            if self.is_green_right:
                car.position -= car.speed

            if not self.is_green_right and car.position < self.traffic_light_right.x :
                car.position -= car.speed
                

        for car in self.lane2_cars:
            if self.is_green_left:
                car.position += car.speed
            
            if not self.is_green_left and car.position > self.traffic_light_left.x:
                car.position += car.speed


        # Actualizar las listas de acuerdo con las nuevas posiciones
        self.lane1_cars = [car for car in self.lane1_cars if car.position > 0]
        self.lane2_cars = [car for car in self.lane2_cars if car.position < self.width]  # Mover el carro detenido al final de la cola


    def update_traffic_lights(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_semaphore_change >= self.semaphore_interval:
            self.last_semaphore_change = current_time

            if self.is_green_left and not self.is_green_right:
                # Izquierda verde, derecha rojo (8 segundos)
                #pasa a rojo/rojo
                self.is_green_left = False
                self.is_green_right = False
                self.semaphore_interval = 3000
                self.fase = 2
            elif not self.is_green_left and  not self.is_green_right:
                # Ambos rojos (3 segundos)
                if self.fase == 2:
                    #pasa a rojo/verde
                    self.is_green_left = False
                    self.is_green_right = True
                    self.semaphore_interval = 5000
                    self.fase = 3
                elif self.fase == 0:
                    #pasa a verde/rojo
                    self.is_green_left = True
                    self.is_green_right = False
                    self.semaphore_interval = 8000
                    self.fase = 1
            elif not self.is_green_left and self.is_green_right:
                # Izquierda rojo, derecha verde (5 segundos)
                #pasa a rojo/rojo
                self.is_green_left = False
                self.is_green_right = False
                self.semaphore_interval = 3000
                self.fase = 0

            # Reiniciar el tiempo restante
            self.remaining_semaphore_time = self.semaphore_interval

        if not self.is_paused:
            self.remaining_semaphore_time -= self.delta_time * 1000  # Convertir segundos a milisegundos

            if self.remaining_semaphore_time <= 0:
                self.remaining_semaphore_time = self.semaphore_interval
                    
    def generate_cars(self):
       
        # if len(self.lane1_cars) > 0 and len(self.lane2_cars) > 0:
        #     return
        min_distance = 50
        if random.random() < self.car_generation_chance:
            if not self.lane1_cars or self.lane1_cars[-1].position < self.width - min_distance:
                car_lane1 = Car(1)
                car_lane1.position = self.width
                self.lane1_cars.append(car_lane1)

        if random.random() < self.car_generation_chance:
            if not self.lane2_cars or self.lane2_cars[-1].position > min_distance:
                car_lane2 = Car(2)
                car_lane2.position = 0
                self.lane2_cars.append(car_lane2)




    def draw_cars(self):
        for car in self.lane1_cars:
            car.draw_car(self.screen, car.position, self.height // 3 + 10, 0)
            

        for car in self.lane2_cars:
            car.draw_car(self.screen, car.position, self.height // 3 + 50, 180)