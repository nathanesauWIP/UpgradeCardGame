# AI Logic

This document describes the AI Logic used in the Upgrade game.

## Deal phase

Simple algorithm (*current*):
* If the computer has the special number, it will play it right away.

Sophisticated algorithm:
* If the computer has the special number in the first round, it will play it right away.
* In all other rounds, the computer will only play the special number if that would put the trump is in their favor.
    * In their favor means the trump matches the suit which they have the most of.

# Play phase

Simple algorithm (*current*):
* The computer will always play one card when leading a hand