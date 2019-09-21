import sys

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectScrolledList import DirectScrolledList
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *


def buttons(self, text):
    def toggleSomething():
        print("test")
        Button1.removeNode()
        sys.exit()


    Button1 = DirectButton(frameSize=None, text=text, image=(self.ButtonImage.find('**/QuitBtn_UP'),
                                                          self.ButtonImage.find('**/QuitBtn_DN'),
                                                          self.ButtonImage.find('**/QuitBtn_RLVR')),
                        relief=None, command=toggleSomething, text_pos=(0, -0.015),
                        geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(-.85, -0, -.93),
                        text_scale=0.059999999999999998, borderWidth=(0.015, 0.01), scale=.7)

    Button1.setPosHprScale(0.00, 0.00, 0.30, 0.00, 0.00, 0.00, 2.53, 2.53, 2.53)
    Button1.place()

    # ImgBtn1.reparentTo(self.render2d)


class Buttons():
    def __init__(self):
        self.buttons = buttons



app = Buttons()