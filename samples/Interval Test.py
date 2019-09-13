
from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import *
from panda3d.core import *
import random, sys, os, math

class IntervalTest(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        base.disableMouse()

        # Generate our interval
        self.generateInterval()

        # Set up an accept function that will run our interval when the "p" button is pressed
        self.accept('p', self.runTest)

        # Set up an accept function that will stop our interval when the "p" button is released
        self.accept('p-up', self.stopTest)

    def generateInterval(self):
        apple = loader.loadModel('../phase_4/models/minigames/apple.bam')
        apple.setPos(-10, 50, 0)
        apple.setScale(0.01)
        apple.reparentTo(render)

        # The structure of our interval
        self.interval = Sequence(
            # An interval that scales our apple up to 1.0 after 1 second
            LerpScaleInterval(apple, 1.0, (1.0, 1.0, 1.0)),
            # A parallel, which allows us to run multiple sub-intervals at once
            Parallel(
                # An interval that moves our apple 20.0 unites to the right after 1 second
                LerpPosInterval(apple, 10.0, (10, 50, 0)),
                # A sub-interval structure
                Sequence(
                    # An interval that scales our apple up to 1.5 after 1 second
                    LerpScaleInterval(apple, 1.0, (1.5, 1.5, 1.5)),
                    # A pause in our interval that lasts for 1.5 seconds
                    Wait(1.5),
                    LerpScaleInterval(apple, 1.0, (1.0, 1.0, 1.0)),
                    Wait(1.5),
                    LerpScaleInterval(apple, 1.0, (1.5, 1.5, 1.5)),
                    Wait(1.5),
                    LerpScaleInterval(apple, 1.0, (1.0, 1.0, 1.0)),
                    Wait(1.5)
                )
            ),
            # An interval that scales our apple down to 0.01 after 1 second
            LerpScaleInterval(apple, 1.0, (0.01, 0.01, 0.01))
        )

    def runTest(self):
        self.interval.resume()

    def stopTest(self):
        self.interval.pause()


intervalTest = IntervalTest()
intervalTest.run()
