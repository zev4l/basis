import sys
from time import sleep
import pygame
from deck import BiscaDeck
from graphics import CardGraphics, CardBackGraphics

# Initialize the game
pygame.init()

# Set up the screen
size = width, height = 800, 700
screen = pygame.display.set_mode(size)
screen.fill("green")

# Create card graphics
for card in BiscaDeck:
    card.graphics = CardGraphics(card)
    card.back_graphics = CardBackGraphics(card)

# Create players' hands
player1_hand = BiscaDeck[:3]
player2_hand = BiscaDeck[3:6]

# Set up card positions
player1_hand_positions = [(200 + i * (player1_hand[i].graphics.size[0]), 500) for i in range(3)]
player2_hand_positions = [(200 + i * (player2_hand[i].graphics.size[0]), 50) for i in range(3)]
deck_position = (265, 275)
trump_position = (385, 275)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Draw background
    screen.fill((0, 100, 0))

    # Draw player 1's hand
    for card, position in zip(player1_hand, player1_hand_positions):
        screen.blit(card.graphics.surface, position)

    # Draw player 2's hand
    for card, position in zip(player2_hand, player2_hand_positions):
        screen.blit(card.graphics.surface, position)

    # Draw deck
    screen.blit(BiscaDeck[-1].back_graphics.surface, deck_position)

    # Draw trump card
    screen.blit(BiscaDeck[-2].graphics.surface, trump_position)

    pygame.display.flip()

    # Limit the frame rate
    sleep(0.1)
