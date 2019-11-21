from direct.showbase.ShowBase import ShowBase


class PlacerPanel(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.loadModels()
        #self.oobe()
        self.camera.hide()

    def loadModels(self):
        model = loader.loadModel('../phase_4/models/props/coffin.bam')
        model.reparentTo(self.render)
        model.place()

demo = PlacerPanel()
demo.run()