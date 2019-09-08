from constants import *

# pylint: disable=too-few-public-methods
class GlobalVariables:
    def __init__(self):
        self.phase = Phase.NO_PHASE
        self.trump = None
        self.specialNumber = None
        
        # paths are shared by test and src scripts and must be globals
        self.PROJECT_PATH = os.path.abspath(os.path.split(sys.argv[0])[0])
        self.WINDOW_ICON_URL = self.PROJECT_PATH + "/images/vanilla/windowicon.jpg"
        self.CARD_IMAGE_FOLDER_URL = self.PROJECT_PATH + "/images/translucent/"

gv = GlobalVariables()
