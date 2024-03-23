import pygame
import sys

WIDTH = 512
HEIGHT = 512
FRAMERATE = 30


class Main():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Game of life")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
        self.clock = pygame.time.Clock()
        

    def run(self):
        while (True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()    

            pygame.display.update()
            self.clock.tick(FRAMERATE)

m = Main()
m.run()