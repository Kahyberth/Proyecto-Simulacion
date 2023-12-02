# main.py
import pygame as pg
from traffic_simulation import TrafficSimulation

def main():
    pg.init()

    width, height = 800, 600
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption('Simulación de Tráfico')

    simulation = TrafficSimulation(screen, width, height)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        simulation.update()

if __name__ == "__main__":
    main()
