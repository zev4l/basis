from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
import sys
from time import sleep
import pygame
from pygame_cards.abstract import AbstractCardGraphics
from pygame_cards.back import CardBackGraphics

from card import UICard, CardRank, CardSuit

@dataclass
class CardGraphics(AbstractCardGraphics):

       # Specify the type of card that this graphics accept
       card: UICard

       # This will be the file where the character is
       filepath: Path = None

       def __post_init__(self):
              self.filepath = "UI/deck-gui/cards/" + str(self.card.filename)

       @cached_property
       def surface(self) -> pygame.Surface:
              self.size = (80, 120)

              # Size is a property from AbstractCardGraphics
              x, y = self.size

              # Create the surface on which we will plot the card
              surf = pygame.Surface(self.size)

              if self.filepath is not None:
                     # Load the image of our character
                     picture = pygame.image.load(self.filepath)
                     # Rescale it to fit the surface
                     surf.blit(pygame.transform.scale(picture, self.size), (0, 0))
              return surf
       
@dataclass
class CardBackGraphics(CardBackGraphics):

       # Specify the type of card that this graphics accept
       card: UICard

       # This will be the file where the character is
       filepath: Path = "UI/deck-gui/cards-back.png"    

       @cached_property
       def surface(self) -> pygame.Surface:
              self.size = (80, 120)   

              # Size is a property from AbstractCardGraphics
              x, y = self.size

              # Create the surface on which we will plot the card
              surf = pygame.Surface(self.size)

              if self.filepath is not None:
                     # Load the image of our character
                     picture = pygame.image.load(self.filepath)
                     # Rescale it to fit the surface
                     surf.blit(pygame.transform.scale(picture, self.size), (0, 0))
              return surf
       
class CardGraphicsExtended(CardGraphics):
    def __init__(self, card):
        super().__init__(card)
        self.position = (0, 0)