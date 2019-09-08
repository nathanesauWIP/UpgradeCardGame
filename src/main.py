import sys
import copy
from PyQt5.Qt import QApplication

from gameController import GameController

app = QApplication(sys.argv)
gameControl = GameController()

sys.exit(app.exec_())

