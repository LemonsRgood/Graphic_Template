"""
Code by: 
- Stian Møinichen Strøm
- Andreas Pettersen Sanila
"""



import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from numpy import pi, sin, cos, multiply



class Grapichs:
    def __init__(self, width, height, zoom = None, antialiasing = False, buffers = 1, samples = 4):
        self.width = width
        self.height = height
        self.zoom = zoom

        # Multisampling (Anti-aliasing) settings
        if antialiasing:
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, buffers)
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, samples)
        
        screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | DOUBLEBUF | OPENGL)

        glViewport(0, 0, width, height)  # Set viewport to cover new window
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if zoom:
            aspect_ratio = width / height if height > 0 else 1
            
            # Maintain aspect ratio in orthographic projection
            if aspect_ratio >= 1:
                gluOrtho2D(-zoom, zoom, -zoom / aspect_ratio, zoom / aspect_ratio)
            else:
                gluOrtho2D(-zoom * aspect_ratio, zoom * aspect_ratio, -zoom, zoom)
                
        else:
            gluOrtho2D(-width // 2, width // 2, -height // 2, height // 2)
        

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Enable multisampling
        glEnable(GL_MULTISAMPLE)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Standard alpha blending


        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        return screen



    def clear_screen(self, color = (0.0, 0.0, 0.0, 0.0)):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glClearColor(*color)



def drawText(screen: pygame.Surface, font: pygame.font.Font, pos: tuple, text: str, anchor = (0.5, 0.5), color=(1.0, 1.0, 1.0, 1.0)):                                           
    textSurface = font.render(text, True, multiply(color, 255)).convert_alpha()
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(screen.get_width() / 2 + pos[0] - anchor[0] * textSurface.get_width(), screen.get_height() / 2 + pos[1] - anchor[1] * textSurface.get_height())
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)



class Line:
    def __init__(self, pos: tuple, a: tuple, b: tuple, angle = 0, color = (1.0, 1.0, 1.0, 1.0)):
        self.color = color
        self.pos = pos
        self.a = a
        self.b = b
        self.angle = angle
    

    def render(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glRotatef(self.angle, 0, 0, 1)


        glBegin(GL_LINES)
        
        glColor4f(*self.color)
        glVertex2f(self.a[0], self.a[1])
        glVertex2f(self.b[0], self.b[1])
        glColor4f(1.0, 1.0, 1.0, 1.0)

        glEnd()
        glPopMatrix()



class Polygon:
    def __init__(self, pos: tuple, radius, segments = 3, angle = 0, color = (1.0, 1.0, 1.0, 1.0)):
            if type(radius) == float or type(radius) == int:
                self.radius = (radius, radius)
            else:
                self.radius = radius

            self.color = color
            self.pos = pos
            self.segments = segments
            self.angle = angle
    

    def render(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glRotatef(self.angle, 0, 0, 1)


        glBegin(GL_TRIANGLE_FAN)

        glColor4f(*self.color)
        glVertex2f(0, 0)
        for n in range(self.segments + 1):
            angle = 2 * pi * n / self.segments
            glVertex2f(self.radius[0] * sin(angle), self.radius[1] * cos(angle))
        glColor4f(1.0, 1.0, 1.0, 1.0)

        glEnd()
        glPopMatrix()

        



class Triangle:
    def __init__(self, pos: tuple, a: tuple, b: tuple, c: tuple, angle = 0, color = (1.0, 1.0, 1.0, 1.0)):
        self.color = color
        self.pos = pos
        self.a = a
        self.b = b
        self.c = c
        self.angle = angle
    

    def render(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glRotatef(self.angle, 0, 0, 1)


        glBegin(GL_TRIANGLES)
        
        glColor4f(*self.color)
        glVertex2f(self.a[0], self.a[1])
        glVertex2f(self.b[0], self.b[1])
        glVertex2f(self.c[0], self.c[1])

        glEnd()
        glPopMatrix()

        glColor4f(1.0, 1.0, 1.0, 1.0)



class Rectangle:
    def __init__(self, pos: tuple, size: tuple, angle = 0, color = (1.0, 1.0, 1.0, 1.0)):
        self.color = color
        self.pos = pos
        self.size = size
        self.angle = angle
    

    def render(self):
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], 0)
        glRotatef(self.angle, 0, 0, 1)


        glBegin(GL_QUADS)
        
        glColor4f(*self.color)
        glVertex2f(0, 0)  
        glVertex2f(self.size[0], 0)  
        glVertex2f(self.size[0], self.size[1])  
        glVertex2f(0, self.size[1])  

        glEnd()
        glPopMatrix()

        glColor4f(1.0, 1.0, 1.0, 1.0)
    
    
    def get_rect(self, screen) -> pygame.Rect:
        global aspect_ratio, true_zoom, true_width, true_height
        size = (self.size[0] * true_width/(true_zoom * 2), self.size[1] * true_height / ((true_zoom / aspect_ratio) * 2))
        pos = (self.pos[0] * true_width/(true_zoom * 2), self.pos[1] * true_height / ((true_zoom/aspect_ratio) * 2))
        return pygame.Rect((pos[0] + (screen.get_width() / 2), pos[1] + (screen.get_height() / 2) - size[1]), size)



class Image:
    def __init__(self, image_path: str, pos: tuple, angle: float, size: tuple, anchor = (0.0, 0.0), color = (1.0, 1.0, 1.0, 1.0)):
        self.color = color
        self.pos = pos
        self.angle = angle
        self.size = size
        self.anchor = anchor
        
        texture_surface = pygame.image.load(image_path)
        texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
        self.width, self.height = texture_surface.get_size()

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    


    def render(self):
        # Apply rotation
        glPushMatrix()
        glTranslatef(self.pos[0] - self.size[0] * self.anchor[0], self.pos[1] - self.size[1] * self.anchor[1], 0)
        glRotatef(self.angle, 0, 0, 1)
        

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        
        
        glColor4f(*self.color)
        glTexCoord2f(0, 0); glVertex2f(-self.size[0] * 0.5, -self.size[1] * 0.5)
        glTexCoord2f(1, 0); glVertex2f( self.size[0] * 0.5, -self.size[1] * 0.5)
        glTexCoord2f(1, 1); glVertex2f( self.size[0] * 0.5,  self.size[1] * 0.5)
        glTexCoord2f(0, 1); glVertex2f(-self.size[0] * 0.5,  self.size[1] * 0.5)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        
        
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()


