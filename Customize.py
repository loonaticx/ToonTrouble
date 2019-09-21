from direct.showbase.ShowBase import ShowBase


class Customize(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.loadBackground()

    def loadBackground(self):
        background = loader.loadModel('phase_4/models/minigames/treehouse_2players.bam')
        background.reparentTo(render)
        background.setPosHprScale(0.00, 15.00, -3.00, 0.00, 270.00, 180.00, 1.00, 1.00, 1.00)

game = Customize()
game.run()