from direct.gui.DirectButton import DirectButton
from direct.gui.DirectScrolledList import DirectScrolledList
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.controls.GravityWalker import GravityWalker
from panda3d.core import *
import ActorDict
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
import random
import sys
import os
import math
from direct.controls import ControlManager
import LightMgr

class Landwalker(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.OSD = True

        #self.controlManager = ControlManager.ControlManager(True, False)

        #Store which keys are currently pressed
        self.keyMap = {
            "escape": 0,
            "left": 0,
            "right": 0,
            "forward": 0,
            "backward": 0,
            "cam-left": 0,
            "cam-right": 0,
        }

        self.loadWorld()
        localAvatar = self.getActor()
        base.localAvatar = localAvatar

        self.LoadButtons()
        self.objectList = list()

        # Floater Object
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(self.actorBody)
        self.floater.setY(-10)
        self.floater.setZ(8.5)
        self.floater.setHpr(0, -10, 0)

        # Set Camera
        self.camera.reparentTo(self.floater)

        # Accept the control keys for movement and rotation
        self.accept("escape", self.toggle_osd)
        self.accept("arrow_left", self.setKey, ["left", True])
        self.accept("arrow_right", self.setKey, ["right", True])
        self.accept("arrow_up", self.setKey, ["forward", True])
        self.accept("arrow_down", self.setKey, ["backward", True])
        self.accept("arrow_left-up", self.setKey, ["left", False])
        self.accept("arrow_right-up", self.setKey, ["right", False])
        self.accept("arrow_up-up", self.setKey, ["forward", False])
        self.accept("arrow_down-up", self.setKey, ["backward", False])

        self.taskMgr.add(self.move, "moveTask")


        # Create an instance of fog called 'distanceFog'.
        #'distanceFog' is just a name for our fog, not a specific type of fog.
        self.fog = Fog('distanceFog')
        # Set the initial color of our fog to black.
        self.fog.setColor(0, 0, 0)
        # Set the density/falloff of the fog.  The range is 0-1.
        # The higher the numer, the "bigger" the fog effect.
        self.fog.setExpDensity(.01)
        # We will set fog on render which means that everything in our scene will
        # be affected by fog. Alternatively, you could only set fog on a specific
        # object/node and only it and the nodes below it would be affected by
        # the fog.
        self.render.setFog(self.fog)

        self.offset = 3.2375

        wallBitmask = BitMask32(1)
        floorBitmask = BitMask32(2)
        base.cTrav = CollisionTraverser()

        walkControls = GravityWalker(legacyLifter=True)
        walkControls.setWallBitMask(wallBitmask)
        walkControls.setFloorBitMask(floorBitmask)
        walkControls.setWalkSpeed(16.0, 24.0, 8.0, 80.0)
        walkControls.initializeCollisions(base.cTrav, self.actorBody, floorOffset=0.025, reach=4.0)
        walkControls.setAirborneHeightFunc(self.getAirborneHeight())
        walkControls.enableAvatarControls()
        # self.controlManager.add(walkControls, 'walk')
        self.actorBody.physControls = walkControls

        localAvatar.physControls.placeOnFloor()
        # problem: onScreenDebug.enabled = self.toggle

        # print(updateOnScreenDebug.enabled)

        onScreenDebug.enabled = True

        base.taskMgr.add(self.updateOnScreenDebug, 'UpdateOSD')

    def loadWorld(self):
        #Loading our Scene
        self.scene = loader.loadModel("models/world.egg.pz")
        self.scene.reparentTo(self.render)

        self.setBackgroundColor(0.53, 0.80, 0.92, 1)

    def removeWorld(self):
        self.scene.removeNode()

    def getActor(self):
        # Loading our Actor
        actorStartPos = self.scene.find("**/start_point").getPos()
        self.actorBody = ActorDict.playerBody
        self.actorBody.reparentTo(self.render)
        self.actorBody.loop('neutral')
        self.actorBody.setPos(actorStartPos + (0, 0, 1.5))
        self.actorBody.setScale(0.3)
        self.actorBody.setH(-180)

        def ActorHead():
            actorHead = loader.loadModel("custom/def_m.bam")
            actorHead.reparentTo(self.actorBody.find('**/to_head'))
            actorHead.setScale(0.20)
            actorHead.setZ(0)
            actorHead.setH(-180)

        ActorHead()
        return self.actorBody

    def LoadButtons(self):
        Button_Up = loader.loadModel('phase_3/models/gui/quit_button.bam').find('**/QuitBtn_UP')
        Button_Down = loader.loadModel('phase_3/models/gui/quit_button.bam').find('**/QuitBtn_DN')
        Button_Rlvr = loader.loadModel('phase_3/models/gui/quit_button.bam').find('**/QuitBtn_RLVR')
        # https://pastebin.com/agdb8260

        Arrow_Up = loader.loadModel('phase_3/models/gui/nameshop_gui.bam').find('**/triangleButtonUp')
        Arrow_Down = loader.loadModel('phase_3/models/gui/nameshop_gui.bam').find('**/triangleButtonDwn')
        Arrow_Rlvr = loader.loadModel('phase_3/models/gui/nameshop_gui.bam').find('**/triangleButtonRllvr')
        Buttons = [Button_Up, Button_Down, Button_Rlvr]

        numItemsVisible = 4
        itemHeight = 0.11

        myScrolledList = DirectScrolledList(
            decButton_pos=(0.35, 0, 0.54),
            decButton_text_scale=0.04,
            decButton_relief=None,
            decButton_image=(Arrow_Up, Arrow_Down, Arrow_Rlvr),

            incButton_pos=(0.35, 0, -0.01),
            incButton_hpr=(0, 0, 180),
            incButton_text_scale=0.04,
            incButton_relief=None,
            incButton_image=(Arrow_Up, Arrow_Down, Arrow_Rlvr),

            pos=(0.74, 0, 0.4),
            numItemsVisible=numItemsVisible,
            forceHeight=itemHeight,
            itemFrame_pos=(0.35, 0, 0.43))

        modelArray = ['phase_4/models/neighborhoods/toontown_central.bam',
                      'phase_13/models/parties/partyGrounds.bam']
        nameArray = ['Toontown Central', 'Party Grounds']

        for index, name in enumerate(nameArray):
            l = DirectButton(text=name, image=(Buttons), extraArgs=[modelArray[index]], command=self.spawnObject,
                             text_scale=0.045, text_pos=(0, -0.007, 0), relief=None)
            myScrolledList.addItem(l)

    #will be used to spawn objects
    def spawnObject(self, modelName):
        #if spawned object already exists, we're gonna need to remove it
        spawnedObject = loader.loadModel(modelName)
        spawnedObject.reparentTo(render)
        spawnedObject.setPos(base.localAvatar.getPos())
        #self.removeWorld(self.objectList.find(spawnedObject))
        self.objectList.append(spawnedObject)
        print("Model Name: " + repr(modelName))
        print("Spawned Object: " + repr(spawnedObject))
        testobjectindex = len(self.objectList)
        self.removeWorld()

    def getAirborneHeight(self):
        return self.offset + 0.025000000000000001

    def toggle_osd(self):
        self.OSD = not self.OSD
        if self.OSD:
            self.onScreenDebug.enabled = True
        else:
            self.onScreenDebug.enabled = False

    def updateOnScreenDebug(self, task):
        if(onScreenDebug.enabled):
            onScreenDebug.add('Avatar Position', base.localAvatar.getPos())
            onScreenDebug.add('Avatar Angle', base.localAvatar.getHpr())
            onScreenDebug.add('Camera Position', base.camera.getPos())
            onScreenDebug.add('Camera Angle', base.camera.getHpr())

        return Task.cont




    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value



    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):
        dt = globalClock.getDt()
        if self.keyMap["forward"]:
                self.localAvatar.setY(self.localAvatar, 20 * dt)
        elif self.keyMap["backward"]:
                self.localAvatar.setY(self.localAvatar, -20 * dt)
        if self.keyMap["left"]:
                self.localAvatar.setHpr(self.localAvatar.getH() + 1.5, self.localAvatar.getP(), self.localAvatar.getR())
        elif self.keyMap["right"]:
                self.localAvatar.setHpr(self.localAvatar.getH() - 1.5, self.localAvatar.getP(), self.localAvatar.getR())

        currentAnim = self.actorBody.getCurrentAnim()

        if self.keyMap["forward"]:
            if currentAnim != "walk":
                self.localAvatar.loop("walk")
        elif self.keyMap["backward"]:
            # Play the walk animation backwards.
            if currentAnim != "walk":
                self.localAvatar.loop("walk")
            self.localAvatar.setPlayRate(-1.0, "walk")
        elif self.keyMap["left"] or self.keyMap["right"]:
            if currentAnim != "walk":
                self.localAvatar.loop("walk")
            self.localAvatar.setPlayRate(1.0, "walk")
        else:
            if currentAnim is not None:
                self.localAvatar.stop()
                self.localAvatar.loop("neutral")
                self.isMoving = False

        return task.cont



demo = Landwalker()
demo.run()
