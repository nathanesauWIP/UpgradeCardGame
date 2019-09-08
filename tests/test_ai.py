# pylint: disable-all
# determine how AI responds to certain scenarios

import unittest
import sys
import os
import copy
import pickle

#PROJECT_PATH = os.path.abspath(os.path.split(sys.argv[0])[0])

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from PyQt5.Qt import QApplication
from gameController import *  # frontend and backend

# current AI logic: always play card zero
saveActions = False  # only do this when replacing AI algorithm
seedArray = [1000, 2000, 3000]
trumpArray = [Suit.CLUBS, Suit.CLUBS, Suit.CLUBS]
specialNumberArray = [Value.TWO, Value.TWO, Value.TWO]

dealer = Dealer()
hand = Hand()
ai = AI(dealer, hand)


def getFilename(seed):  # pickle output file
    return "tests/output/ai_actions_" + str(seed)


def createOutput():  # write ai actions to file
    if not saveActions:
        return
    for i in range(len(seedArray)):
        seed = seedArray[i]
        trump = trumpArray[i]
        specialNumber = specialNumberArray[i]
        setupGame(seed, trump, specialNumber, dealer)
        fileObject = open(getFilename(seed), 'wb')
        numTurns = 0
        while numTurns < 12:  # four computers against each other
            hand.clear()
            actions = []
            for playerNo in range(4):
                actions.append(ai.getActionPlayPhase(playerNo))
                hand.update(actions[playerNo].cards, playerNo)
            pickle.dump(actions, fileObject)
            numTurns += 1
        fileObject.close()


class TestAI(unittest.TestCase):
    def testGetActionPlayPhase(self):
        for i in range(len(seedArray)):
            seed = seedArray[i]
            trump = trumpArray[i]
            specialNumber = specialNumberArray[i]
            fileObject = open(getFilename(seed), 'rb')
            setupGame(seed, trump, specialNumber, dealer)
            numTurns = 0
            while numTurns < 12:
                expectedActions = pickle.load(fileObject)
                hand.clear()
                actions = []
                for playerNo in range(4):
                    actions.append(ai.getActionPlayPhase(playerNo))
                    hand.update(actions[playerNo].cards, playerNo)
                for i in range(4):
                    msg = "invalid action: turn #" + str(numTurns) + ", " + \
                        "player #" + str(i) + ", " + "seed #" + str(seed)
                    self.assertEquals(actions[i], expectedActions[i], msg)
                numTurns += 1


createOutput()

if __name__ == '__main__':
    unittest.main()
