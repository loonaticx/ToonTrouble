from direct.gui.DirectButton import DirectButton
from direct.gui.DirectScrolledList import DirectScrolledList
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *

import Buttons

from direct.gui.DirectGui import DirectButton

class GUIMenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")

        self.loadButtons()

    def loadButtons(self):
        Buttons.buttons(self, 'hi')



app = GUIMenu()
app.run()