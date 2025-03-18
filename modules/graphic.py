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




class Graphic:
    """
    Parameters:
    - width (window width)
    - height (window height)
    - fir (choose a projection to fit everything on the screen)
    - antialiasing (smoother edges)
    - buffers (antialiasing buffers)
    - samples (antialiasing samples)

    Methods
    - clear_screen (clears the screen and fills it with a given color)
    - drawText (draws text on the screen given a pygame font)
    - get_mouse (returns mouse position in screen space)
    """

    def __init__(self, width: float, height: float, fit = False, antialiasing = False, buffers = 1, samples = 4):
        self.width = width
        self.height = height
        self.fit = fit

        # Multisampling (Anti-aliasing) settings
        self.antialiasing = antialiasing
        self.buffers = buffers
        self.samples = samples
        if antialiasing:
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, buffers)
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, samples)
        

        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | DOUBLEBUF | OPENGL)


        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        self.aspect_ratio = width / height
        if fit:
            if width < height: gluOrtho2D(-1, 1, -1 / self.aspect_ratio, 1 / self.aspect_ratio)
            else:              gluOrtho2D(-1 * self.aspect_ratio, 1 * self.aspect_ratio, -1, 1)
        else:
            if width > height: gluOrtho2D(-1, 1, -1 / self.aspect_ratio, 1 / self.aspect_ratio)
            else:              gluOrtho2D(-1 * self.aspect_ratio, 1 * self.aspect_ratio, -1, 1)
            


        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Enable multisampling
        glEnable(GL_MULTISAMPLE)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Standard alpha blending


        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    


    def clear_screen(self, color = (0.0, 0.0, 0.0, 0.0)):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glClearColor(*color)



    def drawText(self, font: pygame.font.Font, pos: tuple, size: float, text: str, anchor = (0.5, 0.5), color=(1.0, 1.0, 1.0, 1.0)):                                           
        textSurface = font.render(text, True, multiply(color, 255)).convert_alpha()
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        size = (textSurface.get_width() * size, textSurface.get_height() * size)
        
        glWindowPos2d(pos[0] + self.width / 2 - size[0] * anchor[0], pos[1] + self.height / 2 - size[1] * anchor[1])
        glDrawPixels(size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE, textData)
    

    def get_mouse_pos(self):
        pos = pygame.mouse.get_pos()
        pos = (-1.0 + 2.0 * pos[0] / self.width, 1.0 - 2.0 * pos[1] / self.height)
        if self.fit:
            if self.width < self.height:
                return (pos[0], pos[1] / self.aspect_ratio)
            else:
                return (pos[0] * self.aspect_ratio, pos[1])
        else:
            if self.width > self.height:
                return (pos[0], pos[1] / self.aspect_ratio)
            else:
                return (pos[0] * self.aspect_ratio, pos[1])



class Line:
    """
    Parameters:
    - graphic (graphics window)
    - pos (position)
    - a (point a)
    - b (point b)
    - angle (rotation angle)
    - color (color)
    """

    def __init__(self, graphic: Graphic, pos: tuple, a: tuple, b: tuple, angle = 0, color = (1.0, 1.0, 1.0, 1.0)):
        self.graphic = graphic

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
    """
    Parameters:
    - graphic (graphics window)
    - pos (position)
    - radius (radius)
    - segments (number og edges)
    - angle (rotation angle)
    - color (color)
    """

    def __init__(self, graphic: Graphic, pos: tuple, radius, segments = 3, angle = 0, color = (1.0, 1.0, 1.0, 1.0)):
        self.graphic = graphic

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
    """
    Parameters:
    - graphic (graphics window)
    - pos (position)
    - a (point a)
    - b (point b)
    - c (point c)
    - angle (rotation angle)
    - color (color)
    """

    def __init__(self, graphic: Graphic, pos: tuple, a: tuple, b: tuple, c: tuple, angle = 0, color = (1.0, 1.0, 1.0, 1.0)):
        self.graphic = graphic 

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
    """
    Parameters:
    - graphic (graphics window)
    - pos (position)
    - size (size)
    - angle (rotation angle)
    - color (color)

    Methods:
    - collidepoint (returns true if there is a point inside the rectangle)
    - colliderect (returns true if there is a rectangle collision /!\ (Does not work with rotation) /!\)
    """

    def __init__(self, graphic: Graphic, pos: tuple, size: tuple, angle = 0, color = (1.0, 1.0, 1.0, 1.0)):
        self.graphic = graphic

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
    
    
    def collidepoint(self, point: tuple) -> pygame.Rect:
        rel = (point[0] - self.pos[0], point[1] - self.pos[1])
        rel = (rel[0] * cos(self.angle * (-pi / 180)) - rel[1] * sin(self.angle * (-pi / 180)),
               rel[0] * sin(self.angle * (-pi / 180)) + rel[1] * cos(self.angle * (-pi / 180)))
        return (0 < rel[0] and rel[0] < self.size[0]) and (0 < rel[1] and rel[1] < self.size[1])
    

    def colliderect(self, other):
        rel = (other.pos[0] - self.pos[0], other.pos[1] - self.pos[1]) 
        return (other.size[0] > rel[0] + self.size[0]) and (rel[0] + 2 * self.size[0] > 0) and (rel[1] < self.size[1]) and (rel[1] + other.size[1] > 0)



class Image:
    """
    Parameters:
    - graphic (graphics window)
    - image_path (path to image file)
    - pos (position)
    - size (size)
    - angle (rotation angle)
    - anchor (anchorpoint of the image)
    - color (color)
    """

    def __init__(self, graphic: Graphic, image_path: str, pos: tuple, size: tuple, angle = 0, anchor = (0.5, 0.5), color = (1.0, 1.0, 1.0, 1.0)):
        self.graphic = graphic

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
        glTranslatef(self.pos[0] - self.size[0] * (self.anchor[0] - 0.5), self.pos[1] - self.size[1] * (self.anchor[1] - 0.5), 0)
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



class Text(Image):
    """
    Parameters:
    - graphic (graphics window)
    - text (text)
    - pos (position)
    - size (text height)
    - angle (rotation angle)
    - anchor (anchorpoint of the image)
    - antialiased (text antialiased)
    - color (color)
    """
    
    def __init__(self, graphic: Graphic, font: pygame.font.Font, text: str, pos: tuple, size: float, angle=0.0, anchor=(0.5, 0.5), antialiased = True, color=(1.0, 1.0, 1.0, 1.0)):
        self.graphic = graphic
        self.font = font
        self.text = text
        
        self.pos = pos
        self.text_size = size
        self.angle = angle
        self.anchor = anchor
        
        self.antialiased = antialiased
        self.color = color
        self.update()
    
    
    def set_size(self, size: float):
        self.text_size = size
        aspect_ratio = self.text_image.get_width() / self.text_image.get_height()
        self.size = (aspect_ratio * self.text_size, self.text_size)
    
    
    def update(self):
        self.text_image = self.font.render(self.text, self.antialiased, (255, 255, 255))
        self.set_size(self.text_size)
        
        texture_data = pygame.image.tostring(self.text_image, "RGBA", True)
        self.width, self.height = self.text_image.get_size()
        
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    