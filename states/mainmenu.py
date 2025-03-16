import pygame, socket, pickle
from modules.graphic import *
FRAMERATE = 60


class MainMenu:
    def __init__(self, app):
        self.app = app
        self.Aimage = Image("textures/shrek.png", (0, 0), 0.0, (200, 200))
        self.Bimage = Image("textures/sally.jpg", (-100, -100), 0.0, (160, 160))
        self.tri = Triangle((0, 0), (-10, 30), (100, 0), (0, 100), color=(1, 0.4, 0, 1))
        self.rec = Rectangle((40, 40), (90, 100), color=(1, 0.4, 0, 1))
        
        self.circle = Polygon((-100, 100), (67, 67), 3, color=(1.0, 0.5, 1.0, 1.0))
        
        self.line = Line((-200, 60), (0, 0), (100, 0), 30, color=(1, 0.4, 0, 1))
        self.font = pygame.font.SysFont('arial', 64)
        


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.app.quit()

            elif event.type == pygame.VIDEORESIZE:
                self.app.screen = init_graphics(event.w, event.h, self.app.zoom, True, 1, 4)



    def update(self):
        dt = self.app.clock.tick(FRAMERATE) / 1000

        self.Aimage.angle += 50 * dt
        self.Bimage.angle -= 30 * dt
    


    def render(self):
        clear_screen((0, 0, 0, 0))

        # Draw textured quad
        self.Aimage.render()
        self.Bimage.render()
        self.tri.render()
        self.rec.render()
        self.circle.render()
        self.line.render()

        #drawText(self.app.screen, self.font, (0, 0), "LOL")

        
        pygame.display.flip()