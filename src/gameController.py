import copy

from gameLogic import *
from gameInterface import *
from ai import *


def getCardName(card):
    return str(card.number)[6:].lower() + " of " + str(card.color)[5:].lower()


class GameController:  # can access private variables of other classes
    def __init__(self):
        self.dealer = Dealer()
        self.hand = Hand()
        self.interface = Interface()  # bind to action
        self.interface.dealLabel.setAction(self.dealCard)
        self.interface.playLabel.setAction(self.playCard)
        self.interface.discardLabel.setAction(self.discardCard)
        self.interface.newGame.triggered.connect(self.startGame)

        if DEBUG_MODE:
            self.interface.newSituation.triggered.connect(self.showDebugMenu)
        
        self.pointsInMiddle = 0
        self.pointsRemaining = 0
        self.ai = AI(self.dealer, self.hand)

    def showDebugMenu(self):
        if not DEBUG_MODE:
            return
        self.interface.situationWidget = QSituationWidget(self.interface)
        self.interface.situationWidget.goButton.setAction(self.goToSituationHelper)
        self.interface.situationWidget.show()

    def discardCard(self):  # only for human
        if gv.phase is not Phase.SELECT_PHASE:  # should not happen
            return
        player = self.dealer.getPlayer(0)
        selectedCards = player.getSelectedCards()
        if len(selectedCards) != 6:
            self.interface.showWarning("You must select 6 cards to discard")
        else:
            self.pointsInMiddle = 0
            for card in selectedCards:
                self.pointsInMiddle += card.points
                player.cardArray.remove(card)
            self.interface.drawCards(player.cardArray, 0)
            self.pointsRemaining -= self.pointsInMiddle
            self.interface.showPointsRemaining(self.pointsRemaining)
            gv.phase = Phase.PLAY_PHASE
            self.interface.showPhase(gv.phase)
            self.interface.discardLabel.hide()
            self.interface.playLabel.show()

    def playCardPlayPhase(self):
        playerNo = self.dealer.getCurrentPlayerNumber()
        player = self.dealer.getPlayer(playerNo)

        if self.dealer.isComputerTurn():
            action = self.ai.getAction(playerNo)
            if action.action is not ActionType.NONE:
                selectedCards = action.cards
                self.hand.update(selectedCards, playerNo)
                cards = player.getCardArray()
                for card in selectedCards:
                    cards.remove(card)
                self.interface.drawCards(cards, playerNo)
                self.interface.drawCards(self.hand.getCenterCards(), 4)
                self.dealer.incrementPlayer()
        else:  # human turn
            selectedCards = player.getSelectedCards()
            cards = player.getCardArray()
            if self.hand.isPlayable(selectedCards, cards):
                self.hand.update(selectedCards, 0)
                for card in selectedCards:
                    cards.remove(card)
                self.interface.drawCards(cards, 0)
                self.interface.drawCards(self.hand.getCenterCards(), 4)
                self.dealer.incrementPlayer()
            else:
                self.interface.showWarning("These cards aren't playable")

        if self.hand.getNumPlayers() == 4:
            winningPlayerNo = self.hand.winningPlayerNo
            winningCards = self.hand.cards[winningPlayerNo]
            self.pointsRemaining -= self.hand.points
            time.sleep(1)  # sleep before msg (give time to see last card)
            msg = "Player " + str(winningPlayerNo) + " won hand with the " + \
                getCardName(winningCards[0])
            self.interface.showWarning(msg)
            self.hand.clear()
            self.interface.hideClickableCardsThisDirection(
                ScreenDirection.CENTER_SELECT_PHASE)

    def finishDealPhase(self, trumpCard):  # called after trump has been determined
        gv.trump = trumpCard.color
        self.dealer.specialPlayer = 0
        self.interface.showTrump(gv.trump)
        while self.dealer.cardDeck.getSize() > 6:
            self.dealCard()
        gv.phase = Phase.SELECT_PHASE
        centerCards = copy.deepcopy(self.dealer.cardDeck.cardArray)
        # only draw if human player didn't win bid
        # self.interface.drawCards(centerCards, 4)
        while self.dealer.cardDeck.getSize() > 0:
            self.dealCard()

        # select center cards which are now in player 1 hand
        clickableCards = self.interface.clickableCards1
        for clickableCard in clickableCards:
            for card in centerCards:
                if clickableCard.card is not None:
                    if clickableCard.card == card:
                        clickableCard.selectCard()

        self.interface.dealLabel.hide()
        self.interface.playLabel.hide()
        self.interface.discardLabel.show()
        self.interface.showPhase(gv.phase)
        self.dealer.currentPlayer = 0

    # only for human (computer action controlled by deal button)
    def playCardDealPhase(self):
        player = self.dealer.getPlayer(0)
        selectedCards = player.getSelectedCards()

        if len(selectedCards) != 1:
            self.interface.showWarning("You must select 1 card")
        else:
            selectedCard = selectedCards[0]
            if selectedCard.number == gv.specialNumber:
                self.dealer.specialPlayer = 0
                self.interface.showWarning(
                    "Player 1 played the " + getCardName(selectedCard))
                self.finishDealPhase(selectedCard)
            else:
                self.interface.showWarning(
                    "This card is not the special number")

    def playCard(self):
        if gv.phase is Phase.NO_PHASE:  # should not happen
            return

        if gv.phase is Phase.DEAL_PHASE:
            self.playCardDealPhase()
        else:  # gv.phase is Phase.PLAY_PHASE
            self.playCardPlayPhase()

    def dealCard(self):
        if gv.phase is Phase.NO_PHASE:  # should not happen
            return

        computerTurn = self.dealer.isComputerTurn()
        if gv.phase is Phase.DEAL_PHASE:
            playerNo = self.dealer.getCurrentPlayerNumber()
        else:  # gv.phase is Phase.SELECT_PHASE:
            playerNo = self.dealer.specialPlayer
        player = self.dealer.getPlayer(playerNo)
        self.dealer.deal()
        self.interface.drawCards(player.getCardArray(), playerNo)

        if self.dealer.specialPlayer is not None:
            return

        if computerTurn:
            action = self.ai.getAction(playerNo)
            if action.action == ActionType.PLAY:
                self.dealer.specialPlayer = playerNo
                selectedCard = action.cards[0]
                msg = "Computer played the " + getCardName(selectedCard)
                self.interface.showWarning(msg, 2)
                self.finishDealPhase(action.cards[0])

    def startGame(self):
        self.dealer.initializeDeck()  # initialize deck for current round
        gv.phase = Phase.DEAL_PHASE
        self.dealer.specialPlayer = None
        self.dealer.currentPlayer = 0
        self.pointsRemaining = 100
        self.pointsInMiddle = 0
        self.interface.dealLabel.show()
        self.interface.playLabel.show()
        self.interface.discardLabel.hide()
        self.interface.hideClickableCards()
        self.interface.showTrump(None)
        self.interface.showPhase(Phase.DEAL_PHASE)
        self.interface.showScores(0, 0)
        self.interface.showSpecialNumber(gv.specialNumber)

    @staticmethod
    def setupGame(seed, trump, specialNumber, dealer):  # for testing only
        gv.trump = trump
        gv.specialNumber = specialNumber
        gv.phase = Phase.DEAL_PHASE
        dealer.initializeDeck(True, seed)
        while dealer.cardDeck.getSize() > 6:
            dealer.deal()
        gv.phase = Phase.PLAY_PHASE

    
    def goToSituationHelper(self):
        if not DEBUG_MODE:
            return
        self.interface.situationWidget.hide()
        self.goToSituation(1000, Suit.SPADES, Value.TWO, 7)


    def goToSituation(self, seed, trump, specialNumber, turn):
        self.startGame()
        GameController.setupGame(
            seed, trump, specialNumber, self.dealer)  # update backend
        numTurns = 0
        while numTurns < turn:
            self.hand.clear()
            actions = []
            for playerNo in range(4):
                actions.append(self.ai.getActionPlayPhase(playerNo))
                self.hand.update(actions[playerNo].cards, playerNo)
            numTurns += 1
        self.interface.drawCards(self.dealer.getPlayer(0).getCardArray(), 0)
        self.interface.drawCards(self.dealer.getPlayer(1).getCardArray(), 1)
        self.interface.drawCards(self.dealer.getPlayer(2).getCardArray(), 2)
        self.interface.drawCards(self.dealer.getPlayer(3).getCardArray(), 3)
