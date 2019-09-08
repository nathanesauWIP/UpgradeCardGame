from enum import Enum
import os
import sys

GAMENAME = 'Upgrade'

DEBUG_MODE = True
TEST_MODE = False

WINDOWXPOS = 0
WINDOWYPOS = 0

CARDWIDTH_DEFAULT = 150
CARDHEIGHT_DEFAULT = 150
GAMEWIDTH_DEFAULT = 800
GAMEHEIGHT_DEFAULT = 775
TOP_BORDER_GAP_DEFAULT = 25
BOTTOM_BORDER_GAP_DEFAULT = 75
LEFT_BORDER_GAP_DEFAULT = 20
RIGHT_BORDER_GAP_DEFAULT = 50
HEIGHT_OFFSET_DEFAULT = 75
LABEL_FONT_SIZE_DEFAULT = 14
DEAL_LABEL_POS_DEFAULT = [325, 500]
PLAY_LABEL_POS_DEFAULT = [400, 500]
CARDGAP_DEFAULT = 25  # how far the cards are spaced apart
DISCARD_LABEL_POS_DEFAULT = [475, 500]

# should be 6 in middle
SIZEHAND = 13  # should be 12


class ScreenDirection(Enum):
    SOUTH = 1
    WEST = 2
    NORTH = 3
    EAST = 4
    CENTER_SELECT_PHASE = 5


class StatusBarSlot(Enum):
    COL1 = 1
    COL2 = 2
    COL3 = 3
    COL4 = 4
    COL5 = 5


class Phase(Enum):  # see manual/rules.md
    NO_PHASE = -1
    DEAL_PHASE = 0
    SELECT_PHASE = 1
    PLAY_PHASE = 2


class Suit(Enum):
    NONE = 0
    HEARTS = 1
    SPADES = 2
    DIAMONDS = 3
    CLUBS = 4


class Value(Enum):
    NONE = 0
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    BLACKJOKER = 15
    REDJOKER = 16
