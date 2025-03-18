"""
Code by: 

"""



import pygame

from states.state import State
from states.mainmenu import MainMenu
from modules.graphic import *



class App:
    def __init__(self, width, height):

        # Initialize pygame
        pygame.init()

        self.clock = pygame.time.Clock()
        
        self.screen = Graphic(width, height, False, True, 1, 4)
        pygame.display.set_caption("Very gud gem")


        # States
        self.states = {
            "mainmenu" : MainMenu
        }
        self.state : State = State(self)
        self.change_state("mainmenu")        

    
    def change_state(self, state: str):
        self.state = self.states[state](self)



    def start(self):
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.render()
    

    def quit(self):
        self.running = False
    


    def events(self):
        self.state.events()


    def update(self):
        self.state.update()


    def render(self):
        self.state.render()


app = App(1080, 720)
app.start()




