from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenImage import OnscreenImage, TransparencyAttrib
from direct.showbase.ShowBase import ShowBase

from src import Customize, Landwalker

class MainMenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.introButtons()


    def introButtons(self):

    def loadGame(self):
        print("Loading game...")
        Button1.removeNode()
        Button2.removeNode()
        imageObject.destroy()
        landFile = Landwalker
        landFile.loadGame()

    def loadCustomize(self):
        print("Loading customize screen...")
        Button1.removeNode()
        Button2.removeNode()
        imageObject.destroy()
        customFile = Customize
        customFile.loadScene()

    def introButtons(self):
        self.imageObject = OnscreenImage(image='stat_board.png', pos=(0, 0, 0))
        self.imageObject.setTransparency(TransparencyAttrib.MAlpha)

        buttonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
        self.loadButton = DirectButton(frameSize=None, text="Load Game", image=(self.ButtonImage.find('**/QuitBtn_UP'),
                                                                 self.ButtonImage.find('**/QuitBtn_DN'),
                                                                 self.ButtonImage.find('**/QuitBtn_RLVR')),
                               relief=None, command=loadGame, text_pos=(0, -0.015),
                               geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(0.00, 0.00, 0.30),
                               text_scale=0.059999999999999998, borderWidth=(0.015, 0.01), scale=2.53)
        self.customizeButton = DirectButton(frameSize=None, text="Customize", image=(self.ButtonImage.find('**/QuitBtn_UP'),
                                                                 self.ButtonImage.find('**/QuitBtn_DN'),
                                                                 self.ButtonImage.find('**/QuitBtn_RLVR')),
                               relief=None, command=loadCustomize, text_pos=(0, -0.015),
                               geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(0.00, 0.00, -0.30),
                               text_scale=0.059999999999999998, borderWidth=(0.015, 0.01), scale=2.53)
        buttonImage.removeNode()


program = MainMenu()
program.run()