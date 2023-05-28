import sys
import pygame
from time import sleep
from deck import BiscaDeck
from graphics import CardGraphics, CardBackGraphics

# Initialize the game
pygame.init()

# Set up the screen
size = width, height = 1000, 800
screen = pygame.display.set_mode(size)
screen.fill((0, 100, 0))  # Use dark green color

# Create card graphics
for card in BiscaDeck:
    card.graphics = CardGraphics(card)
    card.back_graphics = CardBackGraphics(card)

# Define the number of players and their positions
num_players = 6
player_positions = [(375, 50), (375, 600), (25, 200), (725, 450), (25, 450), (725, 200)]

# Create players' hands
hands = [BiscaDeck[i * 3: (i + 1) * 3] for i in range(num_players)]

# Set up card positions for each player
hand_positions = [[(position[0] + i * (card.graphics.size[0] - 25), position[1]) for i in range(3)] for position in player_positions]


# Set up deck and trump positions
deck_position = (412, 350)
trump_position = (512, 350)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Draw background
    screen.fill((0, 100, 0))

    # Draw players' hands and labels
    for i, (hand, position) in enumerate(zip(hands, player_positions)):
        # Draw cards in hand
        for card, card_position in zip(hand, hand_positions[i]):
            screen.blit(card.graphics.surface, card_position)

        # Draw player label
        font = pygame.font.Font(None, 24)
        label = font.render(f"Player {i+1}", True, pygame.Color("white"))
        label_rect = label.get_rect(center=(position[0] + 125, position[1] + 140))
        screen.blit(label, label_rect)

        # Draw player score
        score = 0  # Replace with the actual score of the player
        score_label = font.render(f"Score: {score} points", True, pygame.Color("white"))
        score_rect = score_label.get_rect(center=(position[0] + 125, position[1] + 160))
        screen.blit(score_label, score_rect)

    # Draw deck
    screen.blit(BiscaDeck[-1].back_graphics.surface, deck_position)

    # Draw trump card
    screen.blit(BiscaDeck[-2].graphics.surface, trump_position)

    pygame.display.flip()

    # Limit the frame rate
    sleep(0.1)

