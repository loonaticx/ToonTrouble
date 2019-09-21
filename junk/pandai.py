import direct.directbase.DirectStart
from panda3d.core import *
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
# for Pandai
from panda3d.ai import *


class World(DirectObject):
    def __init__(self):
        base.disableMouse()

        self.loadModels()
        self.setAI()
        base.camera.reparentTo(self.seeker)


    def loadModels(self):
        # Seeker
        ralphStartPos = Vec3(-10, 0, 0)
        self.seeker = Actor("models/ralph",
                            {"run": "models/ralph-run"})
        self.seeker.reparentTo(render)
        self.seeker.setScale(0.5)
        self.seeker.setPos(ralphStartPos)
        # Target
        self.target = loader.loadModel("models/arrow.bam")
        self.target.setColor(1, 0, 0)
        self.target.setPos(5, 0, 0)
        self.target.setScale(1)
        self.target.reparentTo(render)


    def setAI(self):
        # Creating AI World
        self.AIworld = AIWorld(render)

        self.AIchar = AICharacter("seeker", self.seeker, 100, 0.05, 5)
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()

        self.AIbehaviors.seek(self.target)
        self.seeker.loop("run")

        # AI World update
        taskMgr.add(self.AIUpdate, "AIUpdate")

    # to update the AIWorld
    def AIUpdate(self, task):
        self.AIworld.update()
        return Task.cont


w = World()
run()