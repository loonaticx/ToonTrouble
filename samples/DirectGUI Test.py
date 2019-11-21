
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DirectLabel
from panda3d.core import *
import random, sys, os, math

class Calculator(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        base.disableMouse()

        # What is currently inputted into our calculator
        self.input = ''

        # Generates the calculator GUI
        self.generateGUI()


    def generateGUI(self):
        # This creates a node we can reparent all the children GUI to in order to control them all with ease
        self.calulatorNode = aspect2d.attachNewNode('calculator')

        # This is the label that shows us the current input and result
        self.inputLabel = DirectLabel(parent=self.calulatorNode, scale=0.1, pos=(0, 0, 0.3), text=self.input)

        # The button we press to calculate
        self.calculateButton = DirectButton(parent=self.calulatorNode, scale=0.1, pos=(0, 0, -0.5), text='Calculate!',
                                            command=self.calculate)

        # The button we press to clear
        self.clearButton = DirectButton(parent=self.calulatorNode, scale=0.1, pos=(0.35, 0, -0.5), text='CE',
                                        command=self.clear)

        # The button we press to add
        self.addButton = DirectButton(parent=self.calulatorNode, scale=0.1, pos=(0.35, 0, -0.3), text='+',
                                      command=self.inputFunction, extraArgs=['+'])

        # The button we press to subtract
        self.subtractButton = DirectButton(parent=self.calulatorNode, scale=0.125, pos=(0.35, 0, -0.15), text='-',
                                           command=self.inputFunction, extraArgs=['-'])

        # The button we press to multiply
        self.multiplyButton = DirectButton(parent=self.calulatorNode, scale=0.1, pos=(0.35, 0, 0), text='*',
                                           command=self.inputFunction, extraArgs=['*'])

        # The button we press to divide
        self.divideButton = DirectButton(parent=self.calulatorNode, scale=0.075, pos=(0.35, 0, 0.2), text='/',
                                         command=self.inputFunction, extraArgs=['/'])

        # A for loop that generates the individual number buttons for us
        for x in range(9):
            value = x + 1
            if value >= 7:
                zOffset = 0.1
            elif value >= 4:
                zOffset = -0.1
            else:
                zOffset = -0.3
            if value in (1, 4, 7):
                xOffset = -0.15
            elif value in (3, 6, 9):
                xOffset = 0.15
            else:
                xOffset = 0
            numberInput = DirectButton(parent=self.calulatorNode, scale=0.1, pos=(0 + xOffset, 0, 0 + zOffset),
                                       text=str(x+1), command=self.inputFunction, extraArgs=str(x+1))

        # A separate declaration for the 0 button, due to laziness
        numberInput = DirectButton(parent=self.calulatorNode, scale=0.1, pos=(-0.3, 0, -0.3),
                                   text='0', command=self.inputFunction, extraArgs=str(0))

    def calculate(self):
        # We use the eval function to do the calculation, then update our input and display it on the Input Label
        result = eval(self.input)
        self.input = str(result)
        self.inputLabel['text'] = self.input

    def clear(self):
        # Clear our input and display it on the Input Label
        self.input = ''
        self.inputLabel['text'] = self.input

    def inputFunction(self, value):
        # Make sure that you aren't trying to have multiple functions in the calculation
        for input in ('+', '-', '*', '/'):
            if input in self.input and input == value:
                return

        # Add to the input and display it on the Input Label
        self.input = self.input + value
        self.inputLabel['text'] = self.input


calculator = Calculator()
calculator.run()
