
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import *
from direct.task import Task
from panda3d.core import *
import random, sys, os, math

class TaskTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        base.disableMouse()

        # Generate our task
        self.generateTask()

    def generateTask(self):
        # Load our apple
        apple = loader.loadModel('../phase_4/models/minigames/apple.bam')
        apple.setPos(0, 50, 0)
        apple.reparentTo(render)

        # Set up a "doMethodLater" task, which runs a function after a specified amount of time. In this case, it's one second.
        taskMgr.doMethodLater(1.0, self.incrementHeight, 'coconutIncrementTask', extraArgs=[apple])

    def incrementHeight(self, apple):

        # Increment our apple's height
        apple.setZ(apple.getZ() + 1.0)

        # Tell the task to run again
        return Task.again


taskTest = TaskTest()
taskTest.run()
