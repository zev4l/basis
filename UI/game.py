import sys
import os
import pygame
import random
from time import sleep
import threading
import copy

# Local UI imports
from graphics import CardGraphics, CardBackGraphics, CardGraphicsExtended
from button import Button
from card import UICard


# directory reach
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from engine.game import Game
from engine.players import Player, Human, RandomAgent, SimpleGreedyAgent
from engine.structures import State

class BiscaGameUI:
    def __init__(self):
        # Initialize the game
        pygame.init()

        # Set up the screen
        self.size = self.width, self.height = 1000, 800
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((0, 100, 0))  # Use dark green color

        # -----------------------------------------------------
        # -------------------- Variables ----------------------
        # -----------------------------------------------------

        # Define game state variables
        # self.current_player = 0
        # self.player_scores = [0 for x in range(self.num_players)]
        # self.player_takes_hand = 0
        # self.hands = [BiscaDeck[i * 3: (i + 1) * 3] for i in range(self.num_players)]
        # self.trump = BiscaDeck[-2]
        # self.deck = [card for card in BiscaDeck if card not in self.hands[self.current_player] and card != self.trump]
        # self.table = {player_num: None for player_num in range(self.num_players)}
        # self.no_more_cards = False

        self.last_clicked = pygame.time.get_ticks()

        # Initial screen selection of agents for game
        self.agent_count = dict()

        # Keep active buttons
        self.buttons = []
        self.play_again_button = Button(400, 500, 200, 50, "Play Again", self.play_again)
        self.player_takes_hand_text = ""

        # -----------------------------------------------------
        # ---------------------- Game -------------------------
        # -----------------------------------------------------

        self.game = Game()

        self.card_representations = dict()
        for card in self.game.deck.cards:
            uicard = UICard(name=card.__repr__(), rank=card.rank, suit=card.suit, filename=card.get_filename())
            uicard.graphics = CardGraphicsExtended(uicard)
            uicard.back_graphics = CardBackGraphics(uicard)
            self.card_representations[card] = uicard

        # Get all available agents
        agent_types = dict()
        agent_names = []
        for subclass in Player.__subclasses__():
            agent_types[subclass.__name__] = subclass
            agent_names.append(subclass.__name__)

        agent_count = self.showInitialScreen(agent_names)

        player_count = 1
        for agent in agent_count.keys():
            for playernr in range(agent_count[agent]):
                player = agent_types[agent](f'Player {str(player_count)} ({agent})')
                if (agent == "Human"):
                    player.register_input_handler(self.getUserSelectedCard)
                self.game.add_player(player)
                player_count += 1

        # -----------------------------------------------------
        # ------------------- Positioning ---------------------
        # -----------------------------------------------------

        # Define the number of players and their positions
        self.num_players = player_count
        position1 = (375, 50)
        position2 = (725, 200)
        position3 = (725, 450)
        position4 = (375, 600)
        position5 = (25, 450)
        position6 = (25, 200)
        if self.num_players == 2:
            self.player_positions = [position1, position4]
        if self.num_players == 3:
            self.player_positions = [position1, position3, position5]
        if self.num_players == 4:
            self.player_positions = [position1, position2, position4, position5]
        if self.num_players == 5:
            self.player_positions = [position1, position2, position3, position4, position5]
        if self.num_players == 6:
            self.player_positions = [position1, position2, position3, position4, position5, position6]

        # Set up card positions for each player
        self.hand_positions = [[(position[0] + i * (CardGraphicsExtended.size[0] - 25), position[1]) for i in range(3)] for position in self.player_positions]

        # Set up deck and trump positions
        self.deck_position = (412, 350)
        self.trump_position = (512, 350)

        self.cardbuttons = []

        self.trick_hands = []

        self.game.player_pool.register_callback(self.drawCurrentStatus)
        self.game.start_match()
        self.startGame()

        #print("GAME DONE")

    def showInitialScreen(self, agents):
        while self.game.state == State.INIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        button.handle_event(event)

            # Draw background
            self.screen.fill((0, 100, 0))

            self.buttons = []  # Initialize the list of buttons

            for agentnr in range(len(agents)):
                agent = copy.deepcopy(agents[agentnr])

                if agent not in self.agent_count.keys():
                    self.agent_count[agent] = 0

                # Render and display the agent text
                self.drawText(agent, 500, 200 + agentnr * 40, alignment="right")

                # Create and display the minus button
                minus_button = Button(520 - 10, 200 + agentnr * 40 - 10, 20, 20, "-", lambda agent=agent: self.removeAgent(agent), backgroundcolor=(0, 100, 0))
                minus_button.draw(self.screen)
                self.buttons.append(minus_button)

                # Render and display the agent count text
                font = pygame.font.Font(None, 24)
                agent_count_label = font.render(f"{self.agent_count[agent]}", True, pygame.Color("white"))
                agent_count_rect = agent_count_label.get_rect(center=(535, 200 + agentnr * 40))
                self.screen.blit(agent_count_label, agent_count_rect)

                # Create and display the plus button
                plus_button = Button(542, 200 + agentnr * 40 - 10, 20, 20, "+", lambda agent=agent: self.addAgent(agent), backgroundcolor=(0, 100, 0))
                plus_button.draw(self.screen)
                self.buttons.append(plus_button)

            start_game_button = Button(425, 200 + len(agents) * 40 + 5, 150, 50, "Start Game", self.endInit)
            start_game_button.draw(self.screen)
            self.buttons.append(start_game_button)

            self.drawText("Maximum number of Players is 6", 500, 200 + len(agents) * 40 + 75)

            pygame.display.flip()

            # Limit the frame rate
            sleep(0.1)

        self.buttons = []
        return self.agent_count
    
    def startGame(self):
        self.trick_hands = [copy.deepcopy(player.get_hand()) for player in self.game.player_pool.players]

        # Main game loop
        while not self.game.is_over():
            self.screen.fill((0, 100, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.drawCurrentStatus()

            if len(self.game.tricks) > 0: 
                self.show_player_takes_hand(self.game.tricks[-1].get_winner())
            
            self.game.next_round()
            self.trick_hands = [copy.deepcopy(player.get_hand()) for player in self.game.player_pool.players]

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

            self.drawCurrentStatus()

            pygame.display.flip()

            # Limit the frame rate
            sleep(0.1)

    def drawCurrentStatus(self, new_player=None):
        self.screen.fill((0, 100, 0))
        played_cards = []
        if self.game.current_trick != None:
            played_cards = self.game.current_trick.get_cards()
        for playernr in range(len(self.game.player_pool.get_players())):
            player = self.game.player_pool.get_players()[playernr]
            for cardnr in range(len(self.trick_hands[playernr])):
                card = self.trick_hands[playernr][cardnr]
                cardUI = self.card_representations[card]
                if card not in played_cards:
                    cardUI.graphics.position = self.hand_positions[playernr][cardnr]
                else:
                    cardUI.graphics.position = (self.hand_positions[playernr][cardnr][0], self.hand_positions[playernr][cardnr][1] - 25)  # Move the card up by 50 pixels
                cardUI.button = Button(cardUI.graphics.position[0], cardUI.graphics.position[1], CardGraphicsExtended.size[0], CardGraphicsExtended.size[1], "", lambda c=card: self.handleCardClick(c))
                self.cardbuttons.append(cardUI.button)
                self.screen.blit(cardUI.graphics.surface, cardUI.graphics.position)

            # Draw player label
            font = pygame.font.Font(None, 22)
            label = font.render(player.name, True, pygame.Color("white"))
            label_rect = label.get_rect(center=(self.player_positions[playernr][0] + 125, self.player_positions[playernr][1] + 140))
            self.screen.blit(label, label_rect)

            # Draw player score
            score_label = font.render(f"Score: {sum([card.points for card in player.pile])} points", True, pygame.Color("white"))
            score_rect = score_label.get_rect(center=(self.player_positions[playernr][0] + 125, self.player_positions[playernr][1] + 160))
            self.screen.blit(score_label, score_rect)

        # # Draw deck
        if len(self.game.deck.cards) > 0:
            top_deck_card = self.game.deck.cards[-1]
            top_deck_card_graphics = self.card_representations[top_deck_card]
            self.screen.blit(top_deck_card_graphics.back_graphics.surface, self.deck_position)

        # # Draw trump card
        if self.game.trump_card:
            trump_card_graphics = self.card_representations[self.game.trump_card]
            self.screen.blit(trump_card_graphics.graphics.surface, self.trump_position)

        # Draw current player text
        current_player_label = font.render(f"{self.game.player_pool.get_current_player()} is playing", True, pygame.Color("white"))
        current_player_rect = current_player_label.get_rect(center=(self.width // 2, self.height - 300))
        self.screen.blit(current_player_label, current_player_rect)

        # Draw player takes hand text
        player_takes_hand_label = font.render(self.player_takes_hand_text, True, pygame.Color("white"))
        player_takes_hand_rect = player_takes_hand_label.get_rect(center=(self.width // 2, self.height - 275))
        self.screen.blit(player_takes_hand_label, player_takes_hand_rect)

        pygame.display.flip()

        # Limit the frame rate
        sleep(0.1)

    def drawEndScreen(self):
        self.buttons = [self.play_again_button]

        while self.game.state == State.OVER:
            self.screen.fill((0, 100, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.play_again_button.handle_event(event)

            # Render and display the agent text
            self.drawText(f"Game Over", 500, 200, size=45)
            self.drawText(f"Winner is {self.game.winner.name} with {sum([card.points for card in self.game.winner.pile])} points", 500, 250)

            self.drawText(f"Points per player", 500, 300)

            for playernr in range(len(self.game.player_pool.players)):
                player = self.game.player_pool.players[playernr]
                self.drawText(f"{player.name}: {sum([card.points for card in player.pile])}", 500, 330 + 30*playernr)

            self.play_again_button.draw(self.screen)
            
            pygame.display.flip()

            # Limit the frame rate
            sleep(0.1)

    def endInit(self):
        if sum(self.agent_count.values()) > 1:
            self.buttons = []
            self.game.state = State.RUNNING

    def removeAgent(self, agent):
        if self.agent_count[agent] > 0:
            self.agent_count[agent] -= 1

    def addAgent(self, agent):
        if sum(self.agent_count.values()) < 6:
            self.agent_count[agent] += 1

    def drawText(self, text, x, y, alignment="center", size=24, color=pygame.Color("white")):
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

    # Define Play Again Button
    def play_again(self):
        print("here")
        BiscaGameUI()
    
    def isTableFull(self):
        return all(value is not None for value in self.table.values())
    
    def isTableNotEmpty(self):
        return any(value is not None for value in self.table.values())

    def handleCardClick(self, card):
        if pygame.time.get_ticks() - self.last_clicked >= 500:
            # This condition checks the card against the player's playable cards, thus avoiding illegal plays
            if card in self.game.player_pool.get_current_player().playable_cards(self.game):       
                self.last_clicked = pygame.time.get_ticks()
                    
                return self.trick_hands[self.game.player_pool.current_player_index].index(card)
    
    def remove_cards_from_hands(self):
        positions = []
        for playernum in range(self.num_players):
            positions.append((self.table[playernum].graphics.position[0], self.table[playernum].graphics.position[1] + 25))
            self.hands[playernum].remove(self.table[playernum])
            self.cardbuttons.remove(self.table[playernum].button)
        self.table = {player_num: None for player_num in range(self.num_players)}
        return positions

    def deal_cards(self, empty_positions):
        for playernum in range(self.num_players):
            if len(self.deck) > 0:
                self.hands[playernum].append(self.deck[0])
                dealtcard = self.hands[playernum][-1]
                dealtcard.graphics.position = empty_positions[playernum]
                dealtcard.button = Button(dealtcard.graphics.position[0], dealtcard.graphics.position[1], CardGraphicsExtended.size[0], CardGraphicsExtended.size[1], "", lambda c=dealtcard: self.handleCardClick(c))
                self.cardbuttons.append(dealtcard.button)
                self.deck.pop(0)
            else:
                if not self.no_more_cards:
                    self.hands[playernum].append(self.trump)
                    dealtcard = self.hands[playernum][-1]
                    dealtcard.graphics.position = empty_positions[playernum]
                    dealtcard.button = Button(dealtcard.graphics.position[0], dealtcard.graphics.position[1], CardGraphicsExtended.size[0], CardGraphicsExtended.size[1], "", lambda c=dealtcard: self.handleCardClick(c))
                    self.cardbuttons.append(dealtcard.button)
                else:
                    self.no_more_cards = True
            
    def show_player_takes_hand(self, player):
        self.player_takes_hand_text = player.name+" takes trick"
        timer = threading.Timer(2, self.reset_player_takes_hand)
        timer.start()

    def reset_player_takes_hand(self):
        self.player_takes_hand_text = ""

BiscaGameUI()