# main.py
import pygame as pg
from traffic_simulation import TrafficSimulation

def main():
    pg.init()

    width, height = 800, 600
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption('Simulación de Tráfico')

    simulation = TrafficSimulation(screen, width, height)
    
    clock = pg.time.Clock()  # Create a clock object for controlling the frame rate

    while True:
        simulation.update()
        pg.display.flip()
        clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    main()