import pygame, socket, pickle, time
from modules.graphic import *
FRAMERATE = 60


class MainMenu:
    def __init__(self, app):
        self.app = app
        self.Aimage = Image(self.app.screen, "textures/shrek.png", (0, 0), (1080, 1080))
        self.Bimage = Image(self.app.screen, "textures/sally.jpg", (-100, -100), (160, 160))
        self.tri = Triangle(self.app.screen, (0, 0), (-10, 30), (100, 0), (0, 100), color=(1, 0.4, 0, 1))
        self.rec = Rectangle(self.app.screen, (40, 40), (90, 100), color=(1, 0.4, 0, 1))
        
        self.circle = Polygon(self.app.screen, (-100, 100), (67, 67), 3, color=(1.0, 0.5, 1.0, 1.0))
        
        self.line = Line(self.app.screen, (-200, 60), (0, 0), (100, 0), 30, color=(1, 0.4, 0, 1))
        self.font = pygame.font.SysFont('arial', 999)
        
        self.text = Text(self.app.screen, self.font, "LOL", (0, 0), 64, color=(1.0, 1.0, 0.4, 1.0))
        


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.app.quit()

            elif event.type == pygame.VIDEORESIZE:
                self.app.screen.__init__(event.w, event.h, True, 1, 4)



    def update(self):
        dt = self.app.clock.tick(FRAMERATE) / 1000

        self.Aimage.angle += 50 * dt
        self.Bimage.angle -= 30 * dt
        self.text.set_size(600 + 400 * sin(time.time()))
        self.text.angle += 250 * dt

        pos = pygame.mouse.get_pos()
        if self.rec.get_rect().collidepoint(pos):
            print(time.time())
    


    def render(self):
        self.app.screen.clear_screen((0, 0, 0, 0))

        
        # Draw textured quad
        self.Aimage.render()
        self.Bimage.render()
        self.tri.render()
        self.rec.render()
        self.circle.render()
        self.line.render()
        
        self.text.render()
        
        
        pygame.display.flip()