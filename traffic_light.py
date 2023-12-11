from Constants.constants import LIGHTS_IMAGES
import pygame as pg

class TrafficLight:
    def __init__(self, screen, x, y ):
        self.red = True
        self.green = False
        self.screen = screen
        self.x = x
        self.y = y
        self.base = pg.image.load(LIGHTS_IMAGES["semaforo"])
        self.red_light = pg.transform.scale(pg.image.load(LIGHTS_IMAGES["luz roja"]), (15, 15))
        self.green_light = pg.transform.scale(pg.image.load(LIGHTS_IMAGES["luz verde"]), (15, 15))
        self.red_light_off = pg.transform.scale(pg.image.load(LIGHTS_IMAGES["luz roja apagada"]), (15, 15))
        self.green_light_off = pg.transform.scale(pg.image.load(LIGHTS_IMAGES["luz verde apagada"]), (15, 15))
        



    def change_color (self, is_green, together = False):
      self.screen.blit(self.base, (self.x, self.y))
        
      if is_green:
          self.red = True
          self.green = False

          self.screen.blit(self.red_light_off, (self.x + 17, self.y + 6))
          self.screen.blit(self.green_light, (self.x + 17, self.y + 24))
      elif together:  #Si dado el caso se quiere que los dos semaforos esten en rojo
          self.red = False
          self.green = False
          self.screen.blit(self.red_light_off, (self.x + 17, self.y + 6))
          self.screen.blit(self.green_light_off, (self.x + 17, self.y + 24))
      else:
          self.red = False
          self.green = True
          self.screen.blit(self.red_light, (self.x + 17, self.y + 6))
          self.screen.blit(self.green_light_off, (self.x + 17, self.y + 24))   