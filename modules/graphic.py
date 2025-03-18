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
    - zoom (zoom)
    - antialiasing (smoother edges)
    - buffers (antialiasing buffers)
    - samples (antialiasing samples)

    Methods
    - clear_screen (clears the screen and fills it with a given color)
    - drawText (draws text on the screen given a pygame font)
    """

    def __init__(self, width, height, antialiasing = False, buffers = 1, samples = 4):
        self.width = width
        self.height = height

        # Multisampling (Anti-aliasing) settings
        if antialiasing:
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, buffers)
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, samples)
        

        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE | DOUBLEBUF | OPENGL)


        glViewport(0, 0, width, height)  # Set viewport to cover new window
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()


        self.aspect_ratio = width / height if height > 0 else 1
        
        # Maintain aspect ratio in orthographic projection
        gluOrtho2D(-width, width, -width / self.aspect_ratio, width / self.aspect_ratio)
        
        

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
    - get_rect (returns a pygame rect of the rectangle)
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
    
    
    def get_rect(self) -> pygame.Rect:
        height, width, aspect_ratio = self.graphic.height, self.graphic.width, self.graphic.aspect_ratio
        size = (self.size[0] * width/(width * 2), self.size[1] * height / ((width / aspect_ratio) * 2))

        pos = (self.pos[0] * width/(width * 2), -self.pos[1] * height / ((width / aspect_ratio) * 2))

        return pygame.Rect((pos[0] + (width / 2), pos[1] + (height / 2) - size[1]), size)




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

    def __init__(self, graphic: Graphic, image_path: str, pos: tuple, size: tuple, angle = 0, anchor = (0.0, 0.0), color = (1.0, 1.0, 1.0, 1.0)):
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



class Text(Image):
    def __init__(self, graphic: Graphic, font: pygame.font.Font, text: str, pos: tuple, size: float, angle=0.0, anchor=(0.0, 0.0), antialiased = True, color=(1.0, 1.0, 1.0, 1.0)):
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
    