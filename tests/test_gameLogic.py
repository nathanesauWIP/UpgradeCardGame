# pylint: disable-all
# see https://docs.python.org/3/library/unittest.html

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from gameLogic import *

card1 = Card(Suit.HEARTS, Value.TWO)
card2 = Card(Suit.HEARTS, Value.TWO)
card3 = Card(Suit.CLUBS, Value.THREE)
card4 = Card(Suit.NONE, Value.REDJOKER)

cardArray1 = [Card(Suit.HEARTS, Value.TWO), Card(Suit.SPADES, Value.THREE),
              Card(Suit.NONE, Value.BLACKJOKER)]

gv.trump = Suit.CLUBS
gv.specialNumber = Value.TWO

class TestCard(unittest.TestCase):
    def test_eq__(self):
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)
    
    def testIsJoker(self):
        self.assertTrue(card4.isJoker())
        self.assertFalse(card3.isJoker())

    def testIsSpecialNumber(self):
        self.assertTrue(card1.isSpecialNumber())
        self.assertFalse(card4.isSpecialNumber())

class TestHand(unittest.TestCase):
    def testHasSuit(self):
        self.assertTrue(Hand.hasSuit(Suit.SPADES, cardArray1))
        # this should be true since the black joker is trump
        self.assertTrue(Hand.hasSuit(Suit.CLUBS, cardArray1))


if __name__ == '__main__':
    unittest.main()
