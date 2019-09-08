import random
from enum import Enum
from gameLogic import *
from globalVariables import *

class ActionType(Enum):
    NONE = 0
    PLAY = 1

# pylint: disable=too-few-public-methods


class Action:
    def __init__(self, action, cards=None):
        self.action = action
        self.cards = cards

    def __eq__(self, other):
        if self.action != other.action:
            return False
        if self.cards is None and other.cards is None:
            return True # ActionType.NONE
        if len(self.cards) != len(other.cards):
            return False
        for i in range(len(self.cards)):
            if self.cards[i] != other.cards[i]:
                return False
        return True

class AI:  # see manual/ai.md
    def __init__(self, dealer, hand):
        self.dealer = dealer
        self.hand = hand

    def getActionDealPhase(self, playerNo):
        player = self.dealer.getPlayer(playerNo)
        cards = player.cardArray
        specialNumber = gv.specialNumber
        for card in cards:
            if card.number == specialNumber:
                return Action(ActionType.PLAY, [card])
        return Action(ActionType.NONE)

    def getActionPlayPhase(self, playerNo):
        player = self.dealer.getPlayer(playerNo)
        cards = self.hand.getPlayableCards(player.cardArray)
        #cardNo = 0
        cardNo = random.randint(0, len(cards) - 1) if len(cards) == 1 else 0
        cards = self.hand.getPlayableCards(player.cardArray)
        return Action(ActionType.PLAY, [cards[cardNo]])

    def getAction(self, playerNo):  # main info
        if gv.phase is Phase.DEAL_PHASE:
            return self.getActionDealPhase(playerNo)
        return self.getActionPlayPhase(playerNo)
