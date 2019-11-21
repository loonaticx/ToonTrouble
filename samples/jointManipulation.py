from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode, NodePath, LightAttrib
from panda3d.core import LVector3
from direct.actor.Actor import Actor
from direct.task.Task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
import sys


class JointDemo(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.loadModel()
        #base.oobe()

    def loadModel(self):
        self.character = Actor("../phase_3/models/char/tt_a_chr_dgl_shorts_torso_1000.bam", {
            'neutral' : "../phase_3/models/char/tt_a_chr_dgl_shorts_torso_neutral.bam"
        })
        self.character.reparentTo(self.render)
        self.character.loop('neutral')
        #character.list_joints()
        #self.character.place()

        def loadProp():
            sword = loader.loadModel("../custom/chr_w_swo01a.egg")
            sword.reparentTo(self.character.find('**/neck'))
            sword.setScale(0.03)
            #sword.place()

        loadProp()
        return self.character


demo = JointDemo()
demo.run()