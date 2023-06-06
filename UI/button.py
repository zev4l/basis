import pygame

import pygame

class Button:
    def __init__(self, x, y, width, height, text, action, backgroundcolor=(0, 0, 0), textcolor=(255, 255, 255)):
        # Define the button surface space
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.backgroundcolor = backgroundcolor
        self.textcolor = textcolor

    # Draw the button on screen
    def draw(self, surface):
        pygame.draw.rect(surface, self.backgroundcolor, self.rect)
        font = pygame.font.Font(None, 24)
        text = font.render(self.text, True, self.textcolor)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    # Handle click event with action defined on initialization
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Checking if the user really clicked on the button
                if self.rect.collidepoint(event.pos):
                    # Return the action of the button, allowing it to be passed to the engine in case of human player input
                    return self.action()
