import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListView, \
    QVBoxLayout, QGridLayout, QPushButton, QHBoxLayout, QMessageBox, \
    QMainWindow, QMenuBar, QMenu, QAction, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap, QIcon, QTransform, QPalette, \
    QColor, QFont, QIntValidator
from PyQt5.QtCore import Qt, QObject

from constants import *
from globalVariables import *
# front end does not include backend (gameLogic)


class QSituationWidget(QWidget):
    def __init__(self, args):
        super().__init__(args)
        self.mainList = QListView()
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.mainList)
        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.setLayout(self.mainLayout)
        self.trumpLabel = QLabel(self.mainList)
        self.trumpLabel.setText("Trump: ")
        self.trumpLabel.move(10, 25)
        self.trumpComboBox = QComboBox(self.mainList)
        self.trumpComboBox.addItems(["Hearts", "Spades", "Clubs", "Diamonds"])
        self.trumpComboBox.move(80, 25)
        self.trumpComboBox.resize(75, 20)
        self.trumpComboBox.setStyleSheet(
            "background-color: rgb(135, 206, 250)")
        self.turnLabel = QLabel(self.mainList)
        self.turnLabel.setText("Turn: ")
        self.turnLabel.move(10, 75)
        self.turnComboBox = QComboBox(self.mainList)
        self.turnComboBox.addItems(
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
        self.turnComboBox.move(80, 75)
        self.turnComboBox.setStyleSheet("background-color: rgb(135, 206, 250)")
        self.turnComboBox.resize(75, 20)
        self.specialNumberLabel = QLabel(self.mainList)
        self.specialNumberLabel.setText("Special: ")
        self.specialNumberLabel.move(10, 125)
        self.specialNumberComboBox = QComboBox(self.mainList)
        self.specialNumberComboBox.addItems(["2", "3", "4", "5", "6", "7", "8",
                                             "9", "10", "J", "Q", "K", "A"])
        self.specialNumberComboBox.setStyleSheet(
            "background-color: rgb(135, 206, 250)")
        self.specialNumberComboBox.move(80, 125)
        self.specialNumberComboBox.resize(75, 20)
        self.seedLabel = QLabel(self.mainList)
        self.seedLabel.move(10, 175)
        self.seedLabel.setText("Seed: ")
        self.seedInput = QLineEdit(self.mainList)
        self.seedInput.move(80, 175)
        self.seedInput.setValidator(QIntValidator(0, 10000, self))
        self.seedInput.resize(75, 20)
        self.seedInput.setText("1000")
        self.seedInput.setStyleSheet("background-color: rgb(135, 206, 250)")
        self.goButton = QClickableButton(self.mainList)
        self.goButton.setText("Go!")
        self.goButton.move(80, 230)
        self.goButton.setStyleSheet("background-color: rgb(135, 206, 250)")
        self.move(75, 50)
        self.setStyleSheet("background-color: white")
        self.setWindowTitle("Debug window")
        self.resize(200, 300)


class QClickableCard(QLabel):
    def __init__(self, args):
        super().__init__(args)
        self.card = None
        self.hidden = False

    def selectCard(self):
        if self.card is None:  # should not happen
            return
        if not self.hidden:  # card is only selectable when visible
            if not self.card.selected:
                self.card.selected = True
                self.setStyleSheet(
                    "background-color: rgb(135, 206, 250); border:2px solid")
            else:
                self.card.selected = False
                self.setStyleSheet("background-color: white; border:2px solid")

    def hideCard(self):
        # self.clear()
        # self.setStyleSheet("QLabel{background:transparent}")
        self.hide()
        self.hidden = True
        if self.card is not None:
            self.card.selected = False

    def showCard(self, pixMap, pixMapPos):
        self.setPixmap(pixMap.scaled(Interface.CARDWIDTH, Interface.CARDHEIGHT,
                                     Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.setStyleSheet("background-color: white; border: 2px solid")
        self.move(pixMapPos[0], pixMapPos[1])
        self.showNormal()
        self.hidden = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("card clicked!")
            self.selectCard()  # highlight card


class QClickableButton(QLabel):  # similar to QPushButton
    def __init__(self, args):
        super(QClickableButton, self).__init__(args)
        self.clickAction = None

    def setAction(self, clickAction):
        self.clickAction = clickAction

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("button clicked!")
            self.clickAction()


# a message box that automatically closes after a timeout
class QAutoMessageBox(QMessageBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.timeout = 0
        self.autoClose = False
        self.currentTime = 0

    # pylint: disable=W0613
    def showEvent(self, event):
        self.currentTime = 0
        if self.autoClose:
            self.startTimer(1000)  # check every 1s

    def timerEvent(self, event):
        self.currentTime += 1
        if self.currentTime >= self.timeout:
            self.done(0)

    # pylint: disable=too-many-arguments
    @staticmethod
    def showMsg(parent, msg, timeout, title="", icon=QMessageBox.Information,
                buttons=QMessageBox.Ok):
        w = QAutoMessageBox(parent)
        w.setStyleSheet("background-color: white")
        w.autoClose = True
        w.timeout = timeout
        w.setText(msg)
        w.setWindowTitle(title)
        w.setIcon(icon)
        w.setStandardButtons(buttons)
        w.exec_()

# pylint: disable=R0902,R0904


class Interface(QMainWindow):
    CARDWIDTH = CARDWIDTH_DEFAULT
    CARDHEIGHT = CARDHEIGHT_DEFAULT
    GAMEWIDTH = GAMEWIDTH_DEFAULT
    GAMEHEIGHT = GAMEHEIGHT_DEFAULT
    TOP_BORDER_GAP = TOP_BORDER_GAP_DEFAULT
    BOTTOM_BORDER_GAP = BOTTOM_BORDER_GAP_DEFAULT
    LEFT_BORDER_GAP = LEFT_BORDER_GAP_DEFAULT
    RIGHT_BORDER_GAP = RIGHT_BORDER_GAP_DEFAULT
    HEIGHT_OFFSET = HEIGHT_OFFSET_DEFAULT
    LABEL_FONT_SIZE = LABEL_FONT_SIZE_DEFAULT
    DEAL_LABEL_POS = [DEAL_LABEL_POS_DEFAULT[0], DEAL_LABEL_POS_DEFAULT[1]]
    PLAY_LABEL_POS = [PLAY_LABEL_POS_DEFAULT[0], PLAY_LABEL_POS_DEFAULT[1]]
    DISCARD_LABEL_POS = [DISCARD_LABEL_POS_DEFAULT[0],
                         DISCARD_LABEL_POS_DEFAULT[1]]
    CARDGAP = CARDGAP_DEFAULT

    def initMenus(self):
        self.newGame = QAction("&New Game", self)
        self.newGame.setShortcut("Ctrl+N")
        self.newGame.setStatusTip("Start a new game")
        self.mainMenu = self.menuBar()
        self.mainMenu.setStyleSheet("background-color: white")
        self.fileMenu = self.mainMenu.addMenu("&File")
        self.fileMenu.addAction(self.newGame)
        self.fileMenu.setStyleSheet("QMenu::item:selected"
                                    "{ background-color: rgb(135, 206, 250);"
                                    "color: rgb(0, 0, 0);}"
                                    "QMenu::item { background-color: white; }")
        self.bottomMenu = self.statusBar()
        self.bottomMenu.setStyleSheet("background-color: white")
        self.bottomMenu.setWindowTitle("hello")

        if DEBUG_MODE:
            self.newSituation = QAction("&Go To Situation", self)
            self.newSituation.setShortcut("Ctrl+D")
            self.newSituation.setStatusTip("Debug a game situation")
            self.debugMenu = self.mainMenu.addMenu("&Debug")
            self.debugMenu.addAction(self.newSituation)
            self.debugMenu.setStyleSheet("QMenu::item:selected"
                                         "{ background-color: rgb(135, 206, 250);"
                                         "color: rgb(0, 0, 0);}"
                                         "QMenu::item { background-color: white; }")

        self.bottomMenuMessageC1 = QLabel()
        self.bottomMenuMessageC2 = QLabel()
        self.bottomMenuMessageC3 = QLabel()
        self.bottomMenuMessageC4 = QLabel()
        self.bottomMenuMessageC5 = QLabel()
        self.bottomMenu.addPermanentWidget(self.bottomMenuMessageC1, 0)
        self.bottomMenu.addPermanentWidget(self.bottomMenuMessageC2, 1)
        self.bottomMenu.addPermanentWidget(self.bottomMenuMessageC3, 2)
        self.bottomMenu.addPermanentWidget(self.bottomMenuMessageC4, 3)
        self.bottomMenu.addPermanentWidget(self.bottomMenuMessageC5, 4)

    def initLabels(self):
        self.dealLabel = QClickableButton(self.mainList)
        self.dealLabel.setText("Deal")
        self.dealLabel.setFont(QFont("Arial", Interface.LABEL_FONT_SIZE))
        self.dealLabel.setStyleSheet("background-color: white; border:0px")
        self.dealLabel.move(
            Interface.DEAL_LABEL_POS[0], Interface.DEAL_LABEL_POS[1])
        self.dealLabel.hide()

        self.playLabel = QClickableButton(self.mainList)
        self.playLabel.setText("Play")
        self.playLabel.setFont(QFont("Arial", Interface.LABEL_FONT_SIZE))
        self.playLabel.setStyleSheet("background-color: white; border:0px")
        self.playLabel.move(
            Interface.PLAY_LABEL_POS[0], Interface.PLAY_LABEL_POS[1])
        self.playLabel.hide()

        self.discardLabel = QClickableButton(self.mainList)
        self.discardLabel.setText("Discard")
        self.discardLabel.setFont(QFont("Arial", Interface.LABEL_FONT_SIZE))
        self.discardLabel.setStyleSheet("background-color: white; border:0px")
        self.discardLabel.move(
            Interface.DISCARD_LABEL_POS[0], Interface.DISCARD_LABEL_POS[1])
        self.discardLabel.hide()

    def __init__(self):
        super().__init__()
        #self.rescale(800, 800)
        self.rescale(400, 400)
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.initMenus()

        self.resize(Interface.GAMEWIDTH, self.GAMEHEIGHT)
        self.move(WINDOWXPOS, WINDOWYPOS)
        self.setWindowTitle(GAMENAME)
        wIcon = QIcon(gv.WINDOW_ICON_URL)
        self.setWindowIcon(wIcon)
        self.repaint()
        self.setStyleSheet("background-color: rgb(0, 90, 0); border:0px")

        self.mainList = QListView()

        self.clickableCards1 = [QClickableCard(
            self.mainList) for i in range(SIZEHAND + 6)]
        self.clickableCards2 = [QClickableCard(
            self.mainList) for i in range(SIZEHAND)]
        self.clickableCards3 = [QClickableCard(
            self.mainList) for i in range(SIZEHAND)]
        self.clickableCards4 = [QClickableCard(
            self.mainList) for i in range(SIZEHAND)]
        self.clickableCards5 = [QClickableCard(
            self.mainList) for i in range(6)]

        self.initLabels()

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addWidget(self.mainList)

        self.mainLayout = QGridLayout()
        self.mainLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.mainWidget.setLayout(self.mainLayout)

        self.show()

    # pylint: disable=W0201
    def rescale(self, gameWidth, gameHeight):
        if self.width() != Interface.GAMEWIDTH or self.height() != self.GAMEHEIGHT:
            WIDTH_FACTOR = gameWidth / GAMEWIDTH_DEFAULT
            HEIGHT_FACTOR = gameHeight / GAMEHEIGHT_DEFAULT
            AVG_FACTOR = (WIDTH_FACTOR + HEIGHT_FACTOR) / 2

            Interface.CARDWIDTH = CARDWIDTH_DEFAULT * WIDTH_FACTOR
            Interface.CARDHEIGHT = CARDHEIGHT_DEFAULT * HEIGHT_FACTOR
            Interface.GAMEWIDTH = GAMEWIDTH_DEFAULT * WIDTH_FACTOR
            Interface.GAMEHEIGHT = GAMEHEIGHT_DEFAULT * HEIGHT_FACTOR
            Interface.BOTTOM_BORDER_GAP = BOTTOM_BORDER_GAP_DEFAULT * HEIGHT_FACTOR
            Interface.TOP_BORDER_GAP = TOP_BORDER_GAP_DEFAULT * HEIGHT_FACTOR
            Interface.LEFT_BORDER_GAP = LEFT_BORDER_GAP_DEFAULT * WIDTH_FACTOR
            Interface.RIGHT_BORDER_GAP = RIGHT_BORDER_GAP_DEFAULT * WIDTH_FACTOR
            Interface.HEIGHT_OFFSET = HEIGHT_OFFSET_DEFAULT * HEIGHT_FACTOR
            Interface.LABEL_FONT_SIZE = LABEL_FONT_SIZE_DEFAULT * AVG_FACTOR
            Interface.DEAL_LABEL_POS = [DEAL_LABEL_POS_DEFAULT[0] * WIDTH_FACTOR,
                                        DEAL_LABEL_POS_DEFAULT[1] * HEIGHT_FACTOR]
            Interface.PLAY_LABEL_POS = [PLAY_LABEL_POS_DEFAULT[0] * WIDTH_FACTOR,
                                        PLAY_LABEL_POS_DEFAULT[1] * HEIGHT_FACTOR]
            Interface.DISCARD_LABEL_POS = [DISCARD_LABEL_POS_DEFAULT[0] * WIDTH_FACTOR,
                                           DISCARD_LABEL_POS_DEFAULT[1] * HEIGHT_FACTOR]
            Interface.CARDGAP = CARDGAP_DEFAULT * WIDTH_FACTOR

            # perform shift for elements which are too low
            if Interface.BOTTOM_BORDER_GAP < 70:
                shiftAmount = 70 - Interface.BOTTOM_BORDER_GAP
                Interface.BOTTOM_BORDER_GAP += shiftAmount
                Interface.PLAY_LABEL_POS[1] -= shiftAmount
                Interface.DEAL_LABEL_POS[1] -= shiftAmount
                Interface.DISCARD_LABEL_POS[1] -= shiftAmount
                # Interface.HEIGHT_OFFSET -= shiftAmount

    def resizeEvent(self, event):
        super(Interface, self).resizeEvent(event)
        self.rescale(self.width(), self.height())
        self.redrawAll()

    def redrawAll(self):
        self.hideClickableCards()
        self.playLabel.hide()
        self.playLabel.setFont(QFont("Arial", Interface.LABEL_FONT_SIZE))
        self.playLabel.move(
            Interface.PLAY_LABEL_POS[0], Interface.PLAY_LABEL_POS[1])
        if gv.phase is Phase.DEAL_PHASE:
            self.playLabel.showNormal()
        self.dealLabel.hide()
        self.dealLabel.setFont(QFont("Arial", Interface.LABEL_FONT_SIZE))
        self.dealLabel.move(
            Interface.DEAL_LABEL_POS[0], Interface.DEAL_LABEL_POS[1])
        if gv.phase is Phase.DEAL_PHASE:
            self.dealLabel.showNormal()
        self.discardLabel.setFont(QFont("Arial", Interface.LABEL_FONT_SIZE))
        self.discardLabel.move(
            Interface.DISCARD_LABEL_POS[0], Interface.DISCARD_LABEL_POS[1])
        if gv.phase is Phase.SELECT_PHASE:
            self.discardLabel.show()
        Interface.redrawCards(self.clickableCards1, 0)
        Interface.redrawCards(self.clickableCards2, 1)
        Interface.redrawCards(self.clickableCards3, 2)
        Interface.redrawCards(self.clickableCards4, 3)
        Interface.redrawCards(self.clickableCards5, 4)

    def showWarning(self, msg, timeout=1):
        QAutoMessageBox.showMsg(self, msg, timeout)

    def showPointsRemaining(self, pointsRemaining):
        self.showBottomMessage("Points remaining: " + str(pointsRemaining) + "\t\t",
                               StatusBarSlot.COL5)

    def showTrump(self, trump):
        if trump is None:
            self.showBottomMessage("Trump: TBD\t\t", StatusBarSlot.COL1)
        else:
            self.showBottomMessage("Trump: " + str(trump)[5:].title() +
                                   "\t\t", StatusBarSlot.COL1)

    def showPhase(self, phase):
        if phase is Phase.DEAL_PHASE:
            self.showBottomMessage("Deal phase\t", StatusBarSlot.COL2)
        elif phase is Phase.PLAY_PHASE:
            self.showBottomMessage("Play phase\t", StatusBarSlot.COL2)
        elif phase is Phase.SELECT_PHASE:
            self.showBottomMessage("Select phase\t", StatusBarSlot.COL2)
        else:
            self.showBottomMessage("Phase: TBD\t\t", StatusBarSlot.COL2)

    def showSpecialNumber(self, specialNumber):
        self.showBottomMessage("Special number: " +
                               str(specialNumber)[6:].title() + "\t", StatusBarSlot.COL3)

    def showScores(self, score1, score2):
        self.showBottomMessage("Team 1: " + str(score1) + "\t Team2: " + str(score2) + "\t",
                               StatusBarSlot.COL4)

    def showBottomMessage(self, msg, slot):
        if slot == StatusBarSlot.COL1:
            self.bottomMenuMessageC1.setText(msg)
        elif slot == StatusBarSlot.COL2:
            self.bottomMenuMessageC2.setText(msg)
        elif slot == StatusBarSlot.COL3:
            self.bottomMenuMessageC3.setText(msg)
        elif slot == StatusBarSlot.COL4:
            self.bottomMenuMessageC4.setText(msg)
        else:  # slot == StatusBarSlot.COL5
            self.bottomMenuMessageC5.setText(msg)

    @staticmethod
    # pylint: disable=too-many-branches
    def getFilename(card):
        fileName = ""

        if card.number == Value.ACE:
            fileName += "1"
        elif card.number == Value.TWO:
            fileName += "2"
        elif card.number == Value.THREE:
            fileName += "3"
        elif card.number == Value.FOUR:
            fileName += "4"
        elif card.number == Value.FIVE:
            fileName += "5"
        elif card.number == Value.SIX:
            fileName += "6"
        elif card.number == Value.SEVEN:
            fileName += "7"
        elif card.number == Value.EIGHT:
            fileName += "8"
        elif card.number == Value.NINE:
            fileName += "9"
        elif card.number == Value.TEN:
            fileName += "10"
        elif card.number == Value.JACK:
            fileName += "11"
        elif card.number == Value.QUEEN:
            fileName += "12"
        elif card.number == Value.KING:
            fileName += "13"
        elif card.number == Value.REDJOKER:
            fileName += "redjoker"
        elif card.number == Value.BLACKJOKER:
            fileName += "blackjoker"

        if card.color == Suit.HEARTS:
            fileName += "hearts"
        elif card.color == Suit.SPADES:
            fileName += "spades"
        elif card.color == Suit.DIAMONDS:
            fileName += "diamonds"
        elif card.color == Suit.CLUBS:
            fileName += "clubs"

        fileName += ".png"

        return fileName

    @staticmethod
    def getDirection(playerNo):
        if playerNo == 0:
            return ScreenDirection.SOUTH
        if playerNo == 1:
            return ScreenDirection.WEST
        if playerNo == 2:
            return ScreenDirection.NORTH
        if playerNo == 3:
            return ScreenDirection.EAST
        if playerNo == 4:
            return ScreenDirection.CENTER_SELECT_PHASE
        return None  # should not happen

    # [x,y] position to draw a card
    @staticmethod
    def getCardPosition(direction, numCards, cardNo):
        # distance spanned by all cards
        totalWidth = Interface.CARDHEIGHT * 1 + \
            (numCards - 1) * Interface.CARDGAP

        pos = [0, 0]
        if direction == ScreenDirection.SOUTH:
            pos[1] = Interface.GAMEHEIGHT - Interface.CARDHEIGHT - \
                Interface.BOTTOM_BORDER_GAP
            pos[0] = (Interface.GAMEWIDTH - totalWidth) / 2
            pos[0] += (cardNo - 1) * Interface.CARDGAP
        elif direction == ScreenDirection.WEST:
            pos[0] = Interface.LEFT_BORDER_GAP
            pos[1] = (Interface.GAMEHEIGHT - totalWidth) / \
                2 - Interface.HEIGHT_OFFSET
            pos[1] += (cardNo - 1) * Interface.CARDGAP
        elif direction == ScreenDirection.NORTH:
            pos[1] = Interface.TOP_BORDER_GAP
            pos[0] = (Interface.GAMEWIDTH - totalWidth) / 2
            pos[0] += (cardNo - 1) * Interface.CARDGAP
        elif direction == ScreenDirection.EAST:
            pos[0] = Interface.GAMEWIDTH - \
                (Interface.RIGHT_BORDER_GAP + Interface.CARDHEIGHT)
            pos[1] = (Interface.GAMEHEIGHT - totalWidth) / \
                2 - Interface.HEIGHT_OFFSET
            pos[1] += (cardNo - 1) * Interface.CARDGAP
        else:  # direction == ScreenDirection.CENTER_SELECT_PHASE
            pos[1] = Interface.GAMEHEIGHT/2 - Interface.CARDHEIGHT
            pos[0] = (Interface.GAMEWIDTH - totalWidth) / 2
            pos[0] += (cardNo - 1) * Interface.CARDGAP

        return pos

    def hideClickableCards(self):
        self.hideClickableCardsThisDirection(ScreenDirection.SOUTH)
        self.hideClickableCardsThisDirection(ScreenDirection.WEST)
        self.hideClickableCardsThisDirection(ScreenDirection.NORTH)
        self.hideClickableCardsThisDirection(ScreenDirection.EAST)
        self.hideClickableCardsThisDirection(
            ScreenDirection.CENTER_SELECT_PHASE)

    def hideClickableCardsThisDirection(self, direction):
        if direction == ScreenDirection.SOUTH:
            clickableCards = self.clickableCards1
        elif direction == ScreenDirection.WEST:
            clickableCards = self.clickableCards2
        elif direction == ScreenDirection.NORTH:
            clickableCards = self.clickableCards3
        elif direction == ScreenDirection.EAST:
            clickableCards = self.clickableCards4
        else:  # direction == ScreenDirection.CENTER_SELECT_PHASE
            clickableCards = self.clickableCards5

        for item in clickableCards:
            if item is not None:
                item.hideCard()

    @staticmethod
    # draws a pixel map to the screen
    def drawCard(card, clickableCard, blank, position, direction):
        if card is None:
            return
        if not blank:
            imageFile = Interface.getFilename(card)
        else:
            imageFile = "back.png"

        pixMap = QPixmap(gv.CARD_IMAGE_FOLDER_URL + imageFile)
        rotation = Interface.getRotation(direction)

        if rotation != 0:
            transform = QTransform()
            transform = transform.rotate(rotation)
            pixMap = pixMap.transformed(transform)

        clickableCard.card = card
        clickableCard.showCard(pixMap, position)

    @staticmethod
    def showBlank(direction):
        if direction == ScreenDirection.SOUTH:
            return False
        if direction == ScreenDirection.WEST:
            return True if not DEBUG_MODE else False
        if direction == ScreenDirection.NORTH:
            return True if not DEBUG_MODE else False
        if direction == ScreenDirection.EAST:
            return True if not DEBUG_MODE else False
        if direction == ScreenDirection.CENTER_SELECT_PHASE:
            return False
        return None  # should not happen

    @staticmethod
    def getRotation(direction):
        if direction == ScreenDirection.SOUTH:
            return 0
        if direction == ScreenDirection.WEST:
            return 90
        if direction == ScreenDirection.NORTH:
            return 180
        if direction == ScreenDirection.EAST:
            return 270
        if direction == ScreenDirection.CENTER_SELECT_PHASE:
            return 0
        return None  # should not happen

    def getClickableCard(self, direction, cardNo):
        if direction == ScreenDirection.SOUTH:
            return self.clickableCards1[cardNo - 1]
        if direction == ScreenDirection.WEST:
            return self.clickableCards2[cardNo - 1]
        if direction == ScreenDirection.NORTH:
            return self.clickableCards3[cardNo - 1]
        if direction == ScreenDirection.EAST:
            return self.clickableCards4[cardNo - 1]
        if direction == ScreenDirection.CENTER_SELECT_PHASE:
            return self.clickableCards5[cardNo - 1]
        return None

    @staticmethod
    def redrawCards(clickableCardArray, playerNo):
        direction = Interface.getDirection(playerNo)
        # no clear card list
        blank = Interface.showBlank(direction)

        numCards = 0
        for clickableCard in clickableCardArray:
            if clickableCard.card is not None:
                numCards += 1
        cardNo = 1

        for clickableCard in clickableCardArray:
            card = clickableCard.card  # grab card from clickableCard
            position = Interface.getCardPosition(direction, numCards, cardNo)
            clickableCard.hide()
            Interface.drawCard(card, clickableCard, blank, position, direction)
            cardNo += 1

    def drawCards(self, cardArray, playerNo):  # displays all cards in cardArray
        direction = Interface.getDirection(playerNo)
        self.hideClickableCardsThisDirection(direction)
        blank = Interface.showBlank(direction)

        numCards = len(cardArray)
        cardNo = 1

        for card in cardArray:
            position = Interface.getCardPosition(direction, numCards, cardNo)
            clickableCard = self.getClickableCard(direction, cardNo)
            Interface.drawCard(card, clickableCard, blank, position, direction)
            cardNo += 1
