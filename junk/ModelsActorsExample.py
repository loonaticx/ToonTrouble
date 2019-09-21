from direct.showbase.ShowBase import ShowBase
from panda3d.direct import *
from panda3d.core import *

class ModelsActorsExample(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.model = self.loader.loadModel('phase_8/models/props/snowman.bam') # <-- File path of model
        self.model.reparentTo(self.render)
        self.model.place()

        self.camera.hide()
        self.oobe()


app = ModelsActorsExample()
app.run()