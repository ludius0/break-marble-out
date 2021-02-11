# libs
import pygame

class Render(): # rename to Render
    def __init__(self, size, bg_c=(0, 0, 0)):
        """Render entities, background, score, etc..."""
        if not isinstance(size, tuple): raise Exception(f"Error with size. Got {type(size)}")
        self.screen = pygame.display.set_mode(size)

        self.bg_c = bg_c # background color

    def __iter__(self):
        print("duh")
    
    def draw_bg(self):
        self.screen.fill(self.bg_c)
    
    def draw_entity(self, *entities):
        for ent in entities:
            pygame.draw.rect(self.screen, ent.get_color(), ent.get_rect())
    
    def update(self):
        pygame.display.update()
        pygame.display.flip()
        
