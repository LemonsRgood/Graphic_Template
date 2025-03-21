import pygame, time, random
from modules.graphic import *
FRAMERATE = 60


class MainMenu:
    def __init__(self, app):
        self.app = app
        self.last_time = time.time()
        self.hit_rect = Rectangle(self.app.screen, (0, 0), (0.02, 0.02), color=(1.0, 0.0, 0.0, 1.0))
        
        self.image = Image(self.app.screen, "textures/shrek.png", (0, 0), (1.0, 1.0))
        self.line = Line(self.app.screen, (0, 0), (-0.1, -0.1), (0.3, 0.5), color=(random.random(), random.random(), random.random(), 1.0))
        self.mouse_line = Line(self.app.screen, (0, 0), (0.1, -0.2), (-0.2, 0.5), color=(1.0, 1.0, 1.0, 0.3))


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.app.quit()

            elif event.type == pygame.VIDEORESIZE:
                self.app.screen.__init__(event.w, event.h, False, self.app.screen.antialiasing, self.app.screen.buffers, self.app.screen.samples)



    def update(self):
        dt = time.time() - self.last_time
        self.last_time = time.time()

        self.image.angle += 40 * dt

        self.mouse_line.pos = self.app.screen.get_mouse_pos()
        hit, hit_pos = self.line.collideline(self.mouse_line)
        
        if hit:
            self.hit_rect.pos = (hit_pos[0] - self.hit_rect.size[0] * 0.5, hit_pos[1] - self.hit_rect.size[1] * 0.5)
        else:
            self.hit_rect.pos = (999, 999)
    


    def render(self):
        self.app.screen.clear_screen((0, 0, 0, 0))

        
        self.image.render()
        self.line.render()
        self.mouse_line.render()
        self.hit_rect.render()
        
        
        pygame.display.flip()