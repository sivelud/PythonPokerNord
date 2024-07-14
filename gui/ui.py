
import pygame
import time

from gui.components import *

OBJECT_GUIS = {}
PLAYER_GUIS = {}
COMMUNITY_CARD_GUIS = {}
SLEEP_TIME = 0.5

class GuiObjects(enum.IntEnum):
    BetText = 0
    Pot = 1
    WinnerText = 2

class UI:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Poker Bots Competition")
        self.bg = pygame.image.load(os.path.join(ASSET_DIR, "background.jpg"))
        self.running = True
        pygame.init()

    def render(self, state, players, playing_player):
        if not self.running:
            return
        
        time.sleep(SLEEP_TIME)

        self.state = state
        self.players = players
        self.playing_player = playing_player

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        if not self.running:
            pygame.quit()
            return

        """Draw everything"""
        self.screen.fill((0, 128, 0))  # Green background for poker table
        self.screen.blit(self.bg, (0, 0))

        # Create UI elements
        self.buildPotUI()
        self.buildCommunityCards()
        self.buildPlayerUIs()

        for guiObject in OBJECT_GUIS:
            OBJECT_GUIS[guiObject].draw(self.screen)

        # Show community cards
        for card_gui in COMMUNITY_CARD_GUIS.values():
            card_gui.draw(self.screen)

        # show player guis
        for player_gui in PLAYER_GUIS.values():
            player_gui.draw(self.screen)

        pygame.display.update()

        self.reset()

    def reset(self):
        """Stuff to do at the end of a play"""
        COMMUNITY_CARD_GUIS.clear()
        OBJECT_GUIS.clear()
        PLAYER_GUIS.clear()
    
    def getPot(self):
        return sum([player["bet"] for player in self.state["players"]])
    
    def getNumberOfPlayers(self):
        return len(self.state["players"])

    def buildPotUI(self):
        self.pot = self.getPot()

        OBJECT_GUIS[GuiObjects.Pot] = TextGUI(
            text=f"${self.pot}",
            size=FontSize.Large,
            topleft=(600, 240),
            color=(255, 255, 0),
        )

    def buildCommunityCards(self):
        """Create the community cards"""
        offset_x = 0
        x, y = 449, 313

        print(self.state["table_cards"])

        i = 0
        for card in self.state["table_cards"]:
            card_gui = CardGUI(card, topleft=(x + offset_x, y))
            COMMUNITY_CARD_GUIS[i] = card_gui
            i += 1
            offset_x += card_gui.image.get_width() + 8

    def buildPlayerUIs(self):
        """Build the player guis dictionary

        Each player has a player GUI object associated in components
        that will show everything related to the player (name, cards, etc.)
        """
        
        i = 0
        for player in self.players:
            PLAYER_GUIS[i] = PlayerGUI(
                player, self.state, self.getNumberOfPlayers(), self.playing_player, i
            )

            i += 1

        for player_gui in PLAYER_GUIS.values():
            player_gui.update_state(self.state)
