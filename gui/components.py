import enum
import os
from pathlib import Path

import pygame

ASSET_DIR = "assets"

# SPRITES
CARDS_SPRITES = {}
OTHERS_SPRITES = {}
FONTS = {}

WIDTH, HEIGHT = 1280, 720
FPS = 60

ROWS = 4
COLS = 7

CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

COLORS = {
    "BORDEAUX": (90, 0, 44),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "BLUE": (0, 0, 255),
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
}

class FontSize(enum.IntEnum):
    Small = 0
    Medium = 1
    Large = 2

class Marker(enum.IntEnum):
    Dealer = 0
    Bet = 1

    def __str__(self):
        marker_str_dict = {Marker.Dealer: "dealer", Marker.Bet: "bet"}
        return marker_str_dict[self]

def load_assets():
    assets_cards_dir = Path(os.path.join(ASSET_DIR, "cards"))
    assets_others_dir = Path(os.path.join(ASSET_DIR, "others"))

    # load cards sprites
    for filename in os.listdir(assets_cards_dir):
        card_name = filename[:-4]
        card_sprite = pygame.image.load(os.path.join(assets_cards_dir, filename))
        card_sprite = pygame.transform.scale(
            card_sprite, (card_sprite.get_width() * 2, card_sprite.get_height() * 2)
        )
        CARDS_SPRITES[card_name] = card_sprite

    # load others sprites
    for filename in os.listdir(assets_others_dir):
        other_name = filename[:-4]
        other_sprite = pygame.image.load(os.path.join(assets_others_dir, filename))
        other_sprite = pygame.transform.scale(
            other_sprite, (other_sprite.get_width() * 2, other_sprite.get_height() * 2)
        )
        OTHERS_SPRITES[other_name] = other_sprite

    # load fonts
    pygame.font.init()
    # FONTS[FontSize.Small] = pygame.font.Font(
    #     os.path.join(assets_fonts_dir, "PixeloidMono-1G8ae.ttf"), 8
    # )
    # FONTS[FontSize.Medium] = pygame.font.Font(
    #     os.path.join(assets_fonts_dir, "PixeloidMono-1G8ae.ttf"), 16
    # )
    # FONTS[FontSize.Large] = pygame.font.Font(
    #     os.path.join(assets_fonts_dir, "PixeloidMono-1G8ae.ttf"), 32
    # )

    FONTS[FontSize.Small] = pygame.font.Font(
        None, 12
    )
    FONTS[FontSize.Medium] = pygame.font.Font(
        None, 24
    )
    FONTS[FontSize.Large] = pygame.font.Font(
        None, 32
    )

load_assets()


class TextGUI:
    def __init__(
        self,
        
        text,
        *,
        size=FontSize.Small,
        topleft=(0, 0),
        angle=0,
        color=(255, 255, 255)
    ):
        self.size = size
        self.color = color
        self.angle = angle

        self.text = pygame.transform.rotate(
            FONTS[self.size].render(text, True, self.color), self.angle
        )
        self.rect = self.text.get_rect()
        self.rect.topleft = topleft

    def update_text(self, text):
        self.text = pygame.transform.rotate(
            FONTS[self.size].render(text, True, self.color), self.angle
        )

    def draw(self, window):
        window.blit(self.text, self.rect)

class CardGUI:
    def __init__(self, card, *, covered=False, topleft=(0, 0), angle=0, scale=1):
        self.card = card
        self.angle = angle
        self.covered = covered  # use it in the future
        self.image = pygame.transform.rotate(CARDS_SPRITES[self.code(card)], angle)
        if covered:
            self.image = pygame.transform.rotate(CARDS_SPRITES["back"], angle)
        self.image = pygame.transform.smoothscale(
            self.image,
            (60 * scale, 87 * scale),
        )
        self.rect = self.image.get_rect()  # use the rect to move the card
        self.rect.topleft = topleft

    def discover(self):
        self.covered = False
        self.image = pygame.transform.rotate(
            CARDS_SPRITES[self.code(self.card)], self.angle
        )

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
    def code(self, card):
        if not card:
            return "back"
        
        match card[1]:
            case "♠":
                suit = "S"
            case "♥":
                suit = "H"
            case "♦":
                suit = "D"
            case "♣":
                suit = "C"

        return f"{card[0]}{suit}"


class PlayerInfoGUI:
    def __init__(self, player, state, *, color, width, height, centerx, bottom):
        self.state = state
        self.surface = pygame.Surface((width, height))  # the size of your rect
        self.color = color
        self.surface.set_alpha(128)  # alpha level
        self.surface.fill(color)
        self.rect = self.surface.get_rect(centerx=centerx, bottom=bottom)

        self.text_name = TextGUI(player.name, size=FontSize.Medium)
        self.text_name.rect.centerx = centerx
        self.text_name.rect.top = self.rect.top

        self.text_chips = TextGUI("$" + str(player.stack), size=FontSize.Medium)
        self.text_chips.rect.centerx = centerx
        self.text_chips.rect.bottom = self.rect.bottom

    def draw(self, window):
        window.blit(self.surface, (self.rect.x, self.rect.y))

        self.text_name.draw(window)
        self.text_chips.draw(window)

class MarkerGUI:
    cell_offsets = {
        (2, 1): (100, -100),
        (1, 0): (100, 0),
        (0, 1): (100, 100),
        (0, 3): (0, 100),
        (0, 5): (-100, 100),
        (1, 6): (-100, 0),
        (2, 5): (-100, -100),
    }

    def __init__(self, marker, player, state, cell, *, angle=0):
        self.marker = marker
        self.player = player
        self.state = state

        self.image = pygame.transform.rotate(OTHERS_SPRITES[str(marker)], angle)
        self.rect = self.image.get_rect()
        center = None
        if cell is None:
            center = WIDTH // 2, 480
        else:
            center = PlayerGUI.cell_centers[cell]
            center = tuple(
                map(sum, zip(center, self.cell_offsets[cell]))
            )  # add the offset to the marker center
        self.rect.center = center

    def draw(self, window):
        off_x, off_y = 0, 0
        if self.marker is Marker.Dealer:
            off_x, off_y = 10, 10
        if self.marker is Marker.Bet:
            txt_gui = TextGUI(
                "$" + str(self.player.bet), size=FontSize.Medium
            )
            txt_gui.rect.centerx = self.rect.x + 10
            txt_gui.rect.centery = self.rect.y + 40
            txt_gui.draw(window)

        window.blit(self.image, (self.rect.x + off_x, self.rect.y + off_y))


class PlayerGUI:
    player_cells = {
        2: [(0, 3)],
        3: [(1, 0), (1, 6)],
        4: [(1, 0), (0, 3), (1, 6)],
        5: [(1, 0), (0, 1), (0, 5), (1, 6)],
        6: [(1, 0), (0, 1), (0, 3), (0, 5), (1, 6)],
        7: [(2, 1), (1, 0), (0, 1), (0, 5), (1, 6), (2, 5)],
        8: [(2, 1), (1, 0), (0, 1), (0, 3), (0, 5), (1, 6), (2, 5)],
    }

    cell_centers = {}

    for cell in player_cells[8]:
        centerx = WIDTH // COLS * cell[1] + CELL_WIDTH // 2
        centery = HEIGHT // ROWS * cell[0] + CELL_HEIGHT // 2
        cell_centers[cell] = (centerx, centery)

    """Manage the entire presence of a player on the screen (cards, info, objects)
    """

    def __init__(
        self,
        player,
        state,
        n_players: int,
        playing_player,
        place
    ):
        self.player = player
        self.state = state
        self.playing_player = playing_player
        self.is_current_player = False
        self.folded = False
        self.is_winner = False
        self.place = place

        self.card_guis = {}
        self.marker_guis = {}
        self.player_info_gui = None
        self.is_you = False

        # assign correct cell to player and build cards
        self.cell = None

        if self.place > 0:
            self.cell = self.player_cells[n_players][self.place - 1]
            self.__build_cards()
        else:
            self.is_you = True
            self.__build_your_cards()

        self.__update_player_info()

    def discover_cards(self):
        if not self.is_you:
            for card in self.card_guis.values():
                card.discover()

    def __build_cards(self):
        x, y = self.cell_centers[self.cell]

        card1, card2 = self.player.hand
        card1_gui = CardGUI(card1, scale=1)
        card2_gui = CardGUI(card2, scale=1)
        #card2_gui = CardGUI(card2, scale=2)
        card1_gui.rect.right = x - 1
        card2_gui.rect.left = x + 1
        card1_gui.rect.centery = y
        card2_gui.rect.centery = y

        self.card_guis[card1] = card1_gui
        self.card_guis[card2] = card2_gui

    def __build_your_cards(self):
        x, y = WIDTH // 2, 640

        card1, card2 = self.player.hand
        card1_gui = CardGUI(card1, scale=2)
        card2_gui = CardGUI(card2, scale=2)
        card1_gui.rect.midright = (x, y)
        card2_gui.rect.midleft = (x, y)

        self.card_guis
        self.card_guis[card1] = card1_gui
        self.card_guis[card2] = card2_gui


    def __build_player_info(self, color):
        x, y = 0, 0
        if self.is_you:
            x, y = WIDTH // 2 - 218, 720
        else:
            x, y = self.cell_centers[self.cell]
            y += CELL_HEIGHT // 2
        self.player_info_gui = PlayerInfoGUI(
            self.player,
            self.state,
            color=color,
            width=CELL_WIDTH - 20,
            height=40,
            centerx=x,
            bottom=y,
        )

    def __build_markers(self):
        if self.player.bet > 0:
            self.marker_guis[Marker.Bet] = MarkerGUI(
                Marker.Bet, self.player, self.state, self.cell
            )

        if self.place == self.state["dealer"]:
            self.marker_guis[Marker.Dealer] = MarkerGUI(
                Marker.Dealer, self.player, self.state, self.cell
            )

    def __update_player_info(self, color=COLORS["BLACK"]):
        self.marker_guis.clear()

        self.__build_player_info(color)
        self.__build_markers()

    def draw(self, window):
        for card_gui in self.card_guis.values():
            card_gui.draw(window)

        self.player_info_gui.draw(window)

        for marker_gui in self.marker_guis.values():
            marker_gui.draw(window)

    def update_state(self, state):
        self.state = state

        color=COLORS["BLACK"]
        if self.player.hasFolded:
            color=COLORS["RED"]
        # elif self.state.winners is not None:
        #     if self.player in self.state.winners:
        #         color = COLORS["YELLOW"]
        elif self.place == self.playing_player:
            color=COLORS["BLUE"]

        self.__update_player_info(color)
