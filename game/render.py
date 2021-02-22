# libs
import pygame

class Render(): # rename to Render
    def __init__(self, size: tuple, bg_c=(0, 0, 0)) -> None:
        """Render entities, background, score, etc..."""
        assert isinstance(size, tuple) and len(size) == 2
        self.screen = pygame.display.set_mode(size)

        self.bg_c = bg_c # background color

    def __iter__(self) -> str:
        return f"Render({self.screen})"
    
    def draw_bg(self) -> None:
        self.screen.fill(self.bg_c)
    
    def draw_entity(self, *entities) -> None:
        for ent in entities:
            pygame.draw.rect(self.screen, ent.get_color(), ent.rect)
    
    def update(self) -> None:
        pygame.display.update()
        pygame.display.flip()