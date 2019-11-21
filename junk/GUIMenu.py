from direct.showbase.ShowBase import ShowBase

from junk import Buttons


class GUIMenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")

        self.loadButtons()

    def loadButtons(self):
        Buttons.buttons(self, 'hi')



app = GUIMenu()
app.run()