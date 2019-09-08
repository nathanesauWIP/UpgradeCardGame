import functools
from enum import Enum
import random

from globalVariables import *
# backend does not include frontend (gameInterface)

# todo: program logic for 4 of a kind
class Hand:
    def __init__(self):
        self.clear()

    def clear(self):
        self.cards = [[] for i in range(4)]
        self.points = 0
        self.color = None
        self.winningPlayerNo = None

    def getNumPlayers(self): # num players that played cards this hand
        numPlayers = 0
        for cardArray in self.cards:
            if cardArray:
                numPlayers += 1
        return numPlayers

    @staticmethod
    def hasSuit(color, cards):
        for card in cards:
            if card.getSuit() == color:
                return True
        return False

    @staticmethod
    def getPoints(cards):
        points = 0
        for card in cards:
            points += card.points
        return points

    @staticmethod
    def sameSuit(cards):
        color = cards[0].getSuit()
        for i in range(1, len(cards)):
            if cards[i].getSuit() != color:
                return False
        return True

    @staticmethod
    def getNumberCards(cards, color):  # num cards matching suit
        numCards = 0
        for card in cards:
            if card.getSuit() == color:
                numCards += 1
        return numCards

    def getPlayableCards(self, cards):
        if self.color is None:
            return cards
        if Hand.hasSuit(self.color, cards): # follow suit
            playableCards = []
            for card in cards:
                if card.getSuit() == self.color:
                    playableCards.append(card)
            return playableCards
        return cards

    # pylint: disable=R0911
    def isPlayable(self, selectedCards, cards):
        if self.color is None:  # no cards played yet
            if not selectedCards:
                return False
            if not Hand.sameSuit(selectedCards):
                return False
            return True
        winningCards = self.cards[self.winningPlayerNo]
        winningColor = winningCards[0].color
        if len(selectedCards) != len(winningCards):
            return False
        if Hand.sameSuit(selectedCards):
            color = selectedCards[0].color
            if color == winningColor:
                return True
            return Hand.hasSuit(winningColor, selectedCards)
        numSelectedCardsThisColor = Hand.getNumberCards(cards, winningColor)
        numCardsThisColor = Hand.getNumberCards(cards, winningColor)
        return numCardsThisColor == numSelectedCardsThisColor

    @staticmethod
    def compareCards(card1, card2, currentSuit = None):  # less than
        if card1.color == gv.trump and card2.color != gv.trump:
            return False
        return card1.number.value < card2.number.value

    def getCenterCards(self):
        centerCards = []
        for cardArray in self.cards:
            for card in cardArray:
                centerCards.append(card)
        return centerCards

    def update(self, selectedCards, playerNo):  # selectedCards are playable
        selectedCards = sorted(selectedCards, key=CardKey.getNumberKey)
        selectedCards = sorted(selectedCards, key=CardKey.getSuitKey)
        self.cards[playerNo] = selectedCards
        self.points += Hand.getPoints(selectedCards)
        selectedColor = selectedCards[0].color
        if self.color is None:
            self.color = selectedColor
            self.winningPlayerNo = playerNo
        else:  # all cards must be greater than winning cards
            winningCards = self.cards[self.winningPlayerNo]
            # pylint: disable=C0200
            for i in range(len(selectedCards)):
                if Hand.compareCards(selectedCards[i], winningCards[i]):
                    return
            self.winningPlayerNo = playerNo


class Card:
    def __init__(self, whichSuit, whichValue):
        self.color = whichSuit
        self.number = whichValue
        self.selected = False
        self.points = Card.getPoints(self.number)

    def getSuit(self):
        if self.isJoker() or self.isSpecialNumber():
            return gv.trump
        return self.color

    def __eq__(self, other):
        return self.color == other.color and self.number == other.number

    @staticmethod
    def getPoints(whichValue):
        if whichValue is Value.FIVE:
            return 5
        if whichValue is Value.TEN:
            return 10
        if whichValue is Value.KING:
            return 10
        return 0

    def isSpecialNumber(self):
        return self.number == gv.specialNumber

    def isJoker(self):
        return self.number == Value.BLACKJOKER or self.number == Value.REDJOKER

    def isTrump(self):
        if self.color == gv.trump:
            return True
        if self.number == Value.BLACKJOKER or \
                self.number == Value.REDJOKER:
            return True
        return False


class Deck:
    def __init__(self):
        self.cardArray = []
        suits = [Suit.HEARTS, Suit.SPADES, Suit.DIAMONDS, Suit.CLUBS]
        values = [Value.ACE, Value.TWO, Value.THREE, Value.FOUR, Value.FIVE,
                  Value.SIX, Value.SEVEN, Value.EIGHT, Value.NINE, Value.TEN,
                  Value.JACK, Value.QUEEN, Value.KING]

        for whichSuit in suits:
            for whichValue in values:
                self.cardArray.append(Card(whichSuit, whichValue))

        self.cardArray.append(Card(Suit.NONE, Value.REDJOKER))
        self.cardArray.append(Card(Suit.NONE, Value.BLACKJOKER))

    def getSize(self):
        return len(self.cardArray)

    def shuffle(self):
        random.shuffle(self.cardArray)

    def pop(self):
        return self.cardArray.pop()


class CardKey:
    @staticmethod
    def getNumberKey(card):
        return int(card.number.value)

    @staticmethod
    def getSuitKey(card):
        return int(card.color.value)


class Player:
    def __init__(self):
        self.cardArray = []

    def getCardArray(self):
        return self.cardArray

    def getSelectedCards(self):
        selectedCards = []
        for card in self.cardArray:
            if card.selected:
                selectedCards.append(card)
        return selectedCards

    def takeCard(self, card):
        self.cardArray.append(card)
        self.cardArray = sorted(self.cardArray, key=CardKey.getNumberKey)
        self.cardArray = sorted(self.cardArray, key=CardKey.getSuitKey)


class Dealer:
    def __init__(self):
        self.cardDeck = None
        self.playerArray = [Player() for i in range(4)]
        self.currentPlayer = 0
        gv.specialNumber = Value.TWO
        self.specialPlayer = None  # gets to select cards

    def isComputerTurn(self):
        return self.currentPlayer != 0

    def getCurrentPlayerNumber(self):
        return self.currentPlayer

    def getPlayer(self, playerNo):
        return self.playerArray[playerNo]

    def incrementPlayer(self):
        if self.currentPlayer == 0:
            self.currentPlayer = 1
        elif self.currentPlayer == 1:
            self.currentPlayer = 2
        elif self.currentPlayer == 2:
            self.currentPlayer = 3
        else:
            self.currentPlayer = 0

    def initializeDeck(self, useSeed=False, seed=1000):
        self.cardDeck = Deck()
        if useSeed:
            random.seed(seed)
        self.cardDeck.shuffle()
        for player in self.playerArray:
            player.cardArray = []

    def deal(self):
        if gv.phase is Phase.DEAL_PHASE:
            if self.cardDeck.getSize() > 6:
                currentPlayer = self.getPlayer(self.currentPlayer)
                currentCard = self.cardDeck.pop()
                currentPlayer.takeCard(currentCard)
                self.incrementPlayer()
        else:  # gv.phase is Phase.SELECT_PHASE:
            if self.cardDeck.getSize() > 0:
                currentPlayer = self.getPlayer(self.specialPlayer)
                currentCard = self.cardDeck.pop()
                currentPlayer.takeCard(currentCard)
