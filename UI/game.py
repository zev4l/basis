import sys
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import random
from time import sleep
import threading
import copy

# Engine imports
from engine.game import Game
from engine.players import Player
from engine.structures import State

# Local UI imports
from UI.graphics import CardGraphics, CardBackGraphics
from UI.button import Button
from UI.card import UICard

SCREEN_BACKGROUND_COLOR = (0, 100, 0)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

CARD_WIDTH = 80
CARD_HEIGHT = 120

PLAYER_POSITION_1 = (375, 50)
PLAYER_POSITION_2 = (725, 200)
PLAYER_POSITION_3 = (725, 450)
PLAYER_POSITION_4 = (375, 600)
PLAYER_POSITION_5 = (25, 450)
PLAYER_POSITION_6 = (25, 200)

DECK_POSITION = (412, 350)
TRUMP_POSITION = (512, 350)

SPACE_BETWEEN_CARDS = 15


class BiscaGameUI:
    def __init__(self):
        # Initialize the game
        pygame.init()
        pygame.display.set_caption("BASIS Platform")
        icon = pygame.image.load("UI/deck-gui/card-game.png")
        pygame.display.set_icon(icon)

        # Set up the screen
        self.size = self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(SCREEN_BACKGROUND_COLOR)  # Use dark green color

        self.last_clicked = pygame.time.get_ticks()

        # Initial screen selection of agents for game
        self.agent_count = dict()

        # Keep active buttons
        self.buttons = []
        self.play_again_button = Button(400, 500, 200, 50, "Play Again", self.playAgain)
        self.player_takes_hand_text = ""

        # -----------------------------------------------------
        # ---------------------- Game -------------------------
        # -----------------------------------------------------

        self.game = Game()

        self.card_representations = dict()
        for card in self.game.deck.cards:
            uicard = UICard(
                name=card.__repr__(),
                rank=card.rank,
                suit=card.suit,
                filename=card.get_filename(),
            )
            uicard.graphics = CardGraphics(uicard)
            uicard.back_graphics = CardBackGraphics(uicard)
            self.card_representations[card] = uicard

        # Get all available agents
        agent_types = dict()
        agent_names = []
        for subclass in Player.__subclasses__():
            agent_types[subclass.__name__] = subclass
            agent_names.append(subclass.__name__)

        # Let the user select the players
        agent_count = self.showInitialScreen(agent_names)

        # Register the players
        player_count = 0
        self.human_game = False
        for agent in agent_count.keys():
            for playernr in range(agent_count[agent]):
                player = agent_types[agent](f"Player {str(player_count + 1)} ({agent})")
                if agent == "Human":
                    self.human_game = True
                    player.register_input_handler(self.getUserSelectedCard)
                self.game.add_player(player)
                player_count += 1

        # -----------------------------------------------------
        # ------------------- Positioning ---------------------
        # -----------------------------------------------------

        # Define the number of players and their positions
        self.num_players = player_count
        if self.num_players == 2:
            self.player_positions = [PLAYER_POSITION_1, PLAYER_POSITION_4]
        if self.num_players == 3:
            self.player_positions = [
                PLAYER_POSITION_1,
                PLAYER_POSITION_3,
                PLAYER_POSITION_5,
            ]
        if self.num_players == 4:
            self.player_positions = [
                PLAYER_POSITION_1,
                PLAYER_POSITION_2,
                PLAYER_POSITION_4,
                PLAYER_POSITION_5,
            ]
        if self.num_players == 5:
            self.player_positions = [
                PLAYER_POSITION_1,
                PLAYER_POSITION_2,
                PLAYER_POSITION_3,
                PLAYER_POSITION_4,
                PLAYER_POSITION_5,
            ]
        if self.num_players == 6:
            self.player_positions = [
                PLAYER_POSITION_1,
                PLAYER_POSITION_2,
                PLAYER_POSITION_3,
                PLAYER_POSITION_4,
                PLAYER_POSITION_5,
                PLAYER_POSITION_6,
            ]

        # Set up card positions for each player
        self.hand_positions = [
            [
                (position[0] + i * (CARD_WIDTH + SPACE_BETWEEN_CARDS), position[1])
                for i in range(3)
            ]
            for position in self.player_positions
        ]

        # Set up deck and trump positions
        self.deck_position = DECK_POSITION
        self.trump_position = TRUMP_POSITION

        # Keep track of available card buttons and the hands at the start of the trick
        self.cardbuttons = []
        self.trick_hands = []

        self.game.player_pool.register_callback(self.drawCurrentStatus)
        self.game.start_match()
        self.startGame()

    # Displays the initial screen that allows the user to select
    # which and how many agents will play
    def showInitialScreen(self, agents):
        while self.game.state == State.INIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle button clicks
                    for button in self.buttons:
                        button.handle_event(event)

            # Draw background
            self.screen.fill(SCREEN_BACKGROUND_COLOR)

            self.buttons = []  # Initialize the list of buttons

            for agentnr in range(len(agents)):
                agent = copy.deepcopy(agents[agentnr])

                if agent not in self.agent_count.keys():
                    self.agent_count[agent] = 0

                # Render and display the agent text
                self.drawText(agent, 500, 200 + agentnr * 40, alignment="right")

                # Create and display the minus button
                minus_button = Button(
                    520 - 10,
                    200 + agentnr * 40 - 10,
                    20,
                    20,
                    "-",
                    lambda agent=agent: self.removeAgent(agent),
                    backgroundcolor=SCREEN_BACKGROUND_COLOR,
                )
                minus_button.draw(self.screen)
                self.buttons.append(minus_button)

                # Render and display the agent count text
                font = pygame.font.Font(None, 24)
                agent_count_label = font.render(
                    f"{self.agent_count[agent]}", True, pygame.Color("white")
                )
                agent_count_rect = agent_count_label.get_rect(
                    center=(535, 200 + agentnr * 40)
                )
                self.screen.blit(agent_count_label, agent_count_rect)

                # Create and display the plus button
                plus_button = Button(
                    542,
                    200 + agentnr * 40 - 10,
                    20,
                    20,
                    "+",
                    lambda agent=agent: self.addAgent(agent),
                    backgroundcolor=SCREEN_BACKGROUND_COLOR,
                )
                plus_button.draw(self.screen)
                self.buttons.append(plus_button)

            # Render and display start game button
            start_game_button = Button(
                425, 200 + len(agents) * 40 + 5, 150, 50, "Start Game", self.endInit
            )
            start_game_button.draw(self.screen)
            self.buttons.append(start_game_button)

            # Render and display informative max player text
            self.drawText(
                "Maximum number of Players is 6", 500, 200 + len(agents) * 40 + 75
            )

            pygame.display.flip()

            # Limit the frame rate
            sleep(0.1)

        self.buttons = []
        return self.agent_count

    # Starts a game and enters the program into a loop for each trick
    def startGame(self):
        self.trick_hands = [
            copy.deepcopy(player.get_hand()) for player in self.game.player_pool.players
        ]

        # Main game loop
        while not self.game.is_over():
            self.screen.fill(SCREEN_BACKGROUND_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Draw most recent display status of the game
            self.drawCurrentStatus()

            if len(self.game.tricks) > 0:
                self.showPlayerTakesHand(self.game.tricks[-1].get_winner())

            # Advance to next round and keep track of players hands at the beginning of the round
            self.game.next_round()
            self.trick_hands = [
                copy.deepcopy(player.get_hand())
                for player in self.game.player_pool.players
            ]

        self.drawEndScreen()

    def getUserSelectedCard(self):
        # This function is called by the Human agent when it needs to select a card
        while True:
            # Checks for all events so as not to block the UI
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Having each button check if it was clicked. If it was, return its own index to the game engine
                    for button in self.cardbuttons:
                        cardIndex = button.handle_event(event)
                        if cardIndex != None:
                            return cardIndex

            # Updates the display status
            self.drawCurrentStatus()

            pygame.display.flip()

            # Limit the frame rate
            sleep(0.1)

    # Displays the current status of the game
    def drawCurrentStatus(self, new_player=None):
        self.screen.fill(SCREEN_BACKGROUND_COLOR)
        played_cards = []
        self.cardbuttons = []
        self.buttons = []

        # Get already played cards to display them above the rest of the hand
        if self.game.current_trick != None:
            played_cards = self.game.current_trick.get_cards()

        for playernr in range(len(self.game.player_pool.get_players())):
            player = self.game.player_pool.get_players()[playernr]
            for cardnr in range(len(self.trick_hands[playernr])):
                card = self.trick_hands[playernr][cardnr]
                cardUI = self.card_representations[card]

                # Chack if card has been played and display accordingly
                if card not in played_cards:
                    cardUI.graphics.position = self.hand_positions[playernr][cardnr]
                else:
                    cardUI.graphics.position = (
                        self.hand_positions[playernr][cardnr][0],
                        self.hand_positions[playernr][cardnr][1] - 25,
                    )  # Move the card up by 50 pixels
                cardUI.button = Button(
                    cardUI.graphics.position[0],
                    cardUI.graphics.position[1],
                    cardUI.graphics.size[0],
                    cardUI.graphics.size[1],
                    "",
                    lambda c=card: self.handleCardClick(c),
                )
                # Keep track of active buttons
                self.cardbuttons.append(cardUI.button)

                if not self.human_game:
                    # Display card on screen
                    self.screen.blit(cardUI.graphics.surface, cardUI.graphics.position)
                else:
                    if type(player).__name__ == "Human":
                        self.screen.blit(
                            cardUI.graphics.surface, cardUI.graphics.position
                        )
                    else:
                        if card not in played_cards:
                            self.screen.blit(
                                cardUI.back_graphics.surface, cardUI.graphics.position
                            )
                        else:
                            self.screen.blit(
                                cardUI.graphics.surface, cardUI.graphics.position
                            )

            # Draw player label
            font = pygame.font.Font(None, 22)
            label = font.render(player.name, True, pygame.Color("white"))
            label_rect = label.get_rect(
                center=(
                    self.player_positions[playernr][0] + 125,
                    self.player_positions[playernr][1] + 140,
                )
            )
            self.screen.blit(label, label_rect)

            # Draw player score
            score_label = font.render(
                f"Score: {sum([card.points for card in player.pile])} points",
                True,
                pygame.Color("white"),
            )
            score_rect = score_label.get_rect(
                center=(
                    self.player_positions[playernr][0] + 125,
                    self.player_positions[playernr][1] + 160,
                )
            )
            self.screen.blit(score_label, score_rect)

        # Draw deck
        if len(self.game.deck.cards) > 0:
            top_deck_card = self.game.deck.cards[-1]
            top_deck_card_graphics = self.card_representations[top_deck_card]
            self.screen.blit(
                top_deck_card_graphics.back_graphics.surface, self.deck_position
            )

        # Draw trump card
        if self.game.trump_card:
            trump_card_graphics = self.card_representations[self.game.trump_card]
            self.screen.blit(trump_card_graphics.graphics.surface, self.trump_position)

        # Draw current player text
        current_player_label = font.render(
            f"{self.game.player_pool.get_current_player()} is playing",
            True,
            pygame.Color("white"),
        )
        current_player_rect = current_player_label.get_rect(
            center=(self.width // 2, self.height - 300)
        )
        self.screen.blit(current_player_label, current_player_rect)

        # Draw player takes hand text
        player_takes_hand_label = font.render(
            self.player_takes_hand_text, True, pygame.Color("white")
        )
        player_takes_hand_rect = player_takes_hand_label.get_rect(
            center=(self.width // 2, self.height - 275)
        )
        self.screen.blit(player_takes_hand_label, player_takes_hand_rect)

        pygame.display.update()

        # Limit the frame rate
        sleep(0.1)

    # Displays the end screen for the user with each players points and the winner
    def drawEndScreen(self):
        self.buttons = [self.play_again_button]

        while self.game.state == State.OVER:
            self.screen.fill(SCREEN_BACKGROUND_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.play_again_button.handle_event(event)

            # Render and display end of the game information
            self.drawText(f"Game Over", 500, 200, size=45)
            self.drawText(
                f"Winner is {self.game.winner.name} with {sum([card.points for card in self.game.winner.pile])} points",
                500,
                250,
            )

            self.drawText(f"Points per player", 500, 300)

            for playernr in range(len(self.game.player_pool.players)):
                player = self.game.player_pool.players[playernr]
                self.drawText(
                    f"{player.name}: {sum([card.points for card in player.pile])}",
                    500,
                    330 + 30 * playernr,
                )

            self.play_again_button.draw(self.screen)

            pygame.display.flip()

            # Limit the frame rate
            sleep(0.1)

    # Checks if the agent count is valid and if so starts a game
    def endInit(self):
        if sum(self.agent_count.values()) > 1:
            self.buttons = []
            self.game.state = State.RUNNING

    # Remove an agent in the initial screen
    def removeAgent(self, agent):
        if self.agent_count[agent] > 0:
            self.agent_count[agent] -= 1

    # Add an agent in the initial screen
    def addAgent(self, agent):
        # Only one human allowed per game
        if agent == "Human":
            if sum(self.agent_count.values()) < 6 and self.agent_count["Human"] == 0:
                self.agent_count[agent] += 1
        else:
            if sum(self.agent_count.values()) < 6:
                self.agent_count[agent] += 1

    # Utils function to make it easier to draw text
    def drawText(
        self, text, x, y, alignment="center", size=24, color=pygame.Color("white")
    ):
        font = pygame.font.Font(None, size)
        label = font.render(text, True, color)
        if alignment == "center":
            label_rect = label.get_rect(center=(x, y))
        elif alignment == "right":
            label_rect = label.get_rect(right=x, centery=y)
        elif alignment == "left":
            label_rect = label.get_rect(left=x, centery=y)
        self.screen.blit(label, label_rect)
        return label

    # Play Again Button Action
    def playAgain(self):
        BiscaGameUI()

    # Handles the click on a displayed card
    def handleCardClick(self, card):
        if pygame.time.get_ticks() - self.last_clicked >= 500:
            print(card)
            # This condition checks the card against the player's playable cards, thus avoiding illegal plays
            if card in self.game.player_pool.get_current_player().playable_cards(
                self.game
            ):
                self.last_clicked = pygame.time.get_ticks()

                self.drawCurrentStatus()

                return self.trick_hands[
                    self.game.player_pool.current_player_index
                ].index(card)

    # Displays informative text about which player won the last trick
    def showPlayerTakesHand(self, player):
        self.player_takes_hand_text = player.name + " takes trick"
        timer = threading.Timer(2, self.resetPlayerTakesHand)
        timer.start()

    # Hides informative text about which player won the last trick
    def resetPlayerTakesHand(self):
        self.player_takes_hand_text = ""
