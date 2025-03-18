import pygame, socket, pickle, time
from modules.graphic import *
FRAMERATE = 60


class MainMenu:
    def __init__(self, app):
        self.app = app
        self.last_time = time.time()
        self.avg_fps = [0 for x in range(50)]
        self.avg_fps_len = len(self.avg_fps)
        
        self.Aimage = Image(self.app.screen, "textures/shrek.png", (0, 0), (1080, 1080))
        self.Bimage = Image(self.app.screen, "textures/sally.jpg", (-100, -100), (160, 160))
        self.tri = Triangle(self.app.screen, (0, 0), (-10, 30), (100, 0), (0, 100), color=(1, 0.4, 0, 1))
        self.rec = Rectangle(self.app.screen, (40, 40), (90, 100), color=(1, 0.4, 0, 1))
        
        self.circle = Polygon(self.app.screen, (-100, 100), (67, 67), 3, color=(1.0, 0.5, 1.0, 1.0))
        
        self.line = Line(self.app.screen, (-200, 60), (0, 0), (100, 0), 30, color=(1, 0.4, 0, 1))
        self.font = pygame.font.SysFont('arial', 128)
        
        self.text = Text(self.app.screen, self.font, "LOL", (0, 0), 64, color=(1.0, 1.0, 0.4, 1.0))
        self.fps_box = Text(self.app.screen, self.font, "fps: ", (0, 0), 96, antialiased=False, anchor=(0.0, 1.0))
        


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.app.quit()

            elif event.type == pygame.VIDEORESIZE:
                self.app.screen.__init__(event.w, event.h, True, 1, 4)



    def update(self):
        dt = time.time() - self.last_time
        self.last_time = time.time()
        self.avg_fps.append(dt)
        self.avg_fps.pop(0)
        

        self.Aimage.angle += 50 * dt
        self.Bimage.angle -= 30 * dt
        self.text.set_size(600 + 400 * sin(time.time()))
        self.text.angle += 250 * dt
        
        self.fps_box.text = f"fps: {round(1 / max(1e-5, sum(self.avg_fps) / self.avg_fps_len), -1)}"
        self.fps_box.pos = (-self.app.screen.width / 2, self.app.screen.height / 2)
        self.fps_box.update()
        
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
        self.fps_box.render()
        
        
        pygame.display.flip()