import pygame, time, random
from modules.graphic import *
FRAMERATE = 60


class MainMenu:
    def __init__(self, app):
        self.app = app
        self.last_time = time.time()
        
        self.image = Image(self.app.screen, "textures/shrek.png", (0, 0), (1.0, 1.0))
        self.rect = Rectangle(self.app.screen, (-0.5, 0), (0.2, 0.3), 0, color=(random.random(), random.random(), random.random(), 1.0))
        self.mouse_rect = Rectangle(self.app.screen, (0, 0), (0.4, 0.4), 0, color=(1.0, 1.0, 1.0, 0.3))


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.app.quit()

            elif event.type == pygame.VIDEORESIZE:
                self.app.screen.__init__(event.w, event.h, False, self.app.screen.antialiasing, self.app.screen.buffers, self.app.screen.samples)



    def update(self):
        dt = time.time() - self.last_time
        self.last_time = time.time()

        self.image.angle += 40 * dt

        self.mouse_rect.pos = self.app.screen.get_mouse_pos()
        if self.rect.colliderect(self.mouse_rect):
            print(time.time())
    


    def render(self):
        self.app.screen.clear_screen((0, 0, 0, 0))

        
        self.image.render()
        self.rect.render()
        self.mouse_rect.render()
        
        
        pygame.display.flip()