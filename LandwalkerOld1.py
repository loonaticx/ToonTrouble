import os

from panda3d.core import *
from panda3d.core import CollisionTraverser
from panda3d.core import PandaNode, NodePath, TextNode

from direct.controls.GravityWalker import GravityWalker
from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectScrolledList import DirectScrolledList
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from src import ConfigManager, ActorDict


#borrowed the xray mod from /samples/culling/portal_culling.py
# https://www.panda3d.org/manual/?title=Common_Image_Filters
#possibly make a slider for bloom
#YO WHAT IF I MAKE A BENCHMARK PROGRAM

def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1),
                        parent=base.a2dTopLeft, align=TextNode.ALeft,
                        pos=(0.08, -pos - 0.04), scale=.05)

class Landwalker(ShowBase):
    def __init__(self):
        #loadPrcFile("Config.prc")
        ShowBase.__init__(self)
        self.config = ConfigManager.loadSettings()


        #Config stuff here
        self.filters = CommonFilters(base.win, base.cam)
        self.AOEnabled = False
        self.bloomEnabled = False
        self.invertEnabled = False
        self.OSD = True
        self.shadersLoaded = False
        self.xray_mode = False
        self.show_model_bounds = False
        self.fogEnabled = True
        self.mouseEnabled = False

        #Store which keys are currently pressed
        self.keyMap = {
            "1": 0,
            "escape": 0,
            "left": 0,
            "right": 0,
            "forward": 0,
            "backward": 0,
            "cam-left": 0,
            "cam-right": 0,
        }

        self.ButtonImage = loader.loadModel("phase_3/models/gui/quit_button.bam")
        self.introButtons()


    def introButtons(self):
        def loadGame():
            print("Loading game...")
            Button1.removeNode()
            Button2.removeNode()
            imageObject.destroy()
            self.loadGame()

        imageObject = OnscreenImage(image='stat_board.png', pos=(0, 0, 0))
        imageObject.setTransparency(TransparencyAttrib.MAlpha)

        Button1 = DirectButton(frameSize=None, text="Load Game", image=(self.ButtonImage.find('**/QuitBtn_UP'),
                                                                 self.ButtonImage.find('**/QuitBtn_DN'),
                                                                 self.ButtonImage.find('**/QuitBtn_RLVR')),
                               relief=None, command=loadGame, text_pos=(0, -0.015),
                               geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(-.85, -0, -.93),
                               text_scale=0.059999999999999998, borderWidth=(0.015, 0.01), scale=.7)

        Button1.setPosHprScale(0.00, 0.00, 0.30, 0.00, 0.00, 0.00, 2.53, 2.53, 2.53)

        Button2 = DirectButton(frameSize=None, text="Customize", image=(self.ButtonImage.find('**/QuitBtn_UP'),
                                                                 self.ButtonImage.find('**/QuitBtn_DN'),
                                                                 self.ButtonImage.find('**/QuitBtn_RLVR')),
                               relief=None, command=loadGame, text_pos=(0, -0.015),
                               geom=None, pad=(0.01, 0.01), suppressKeys=0, pos=(-.85, -0, -.93),
                               text_scale=0.059999999999999998, borderWidth=(0.015, 0.01), scale=.7)

        Button2.setPosHprScale(0.00, 0.00, -0.30, 0.00, 0.00, 0.00, 2.53, 2.53, 2.53)


    def loadGame(self):
        # Adding onscreen text here
        self.inst1 = addInstructions(0.06, "Press F to toggle wireframe")
        self.inst2 = addInstructions(0.12, "Press X to toggle xray")
        self.inst3 = addInstructions(0.18, "Press 1 to activate cartoon shading")
        self.inst4 = addInstructions(0.24, "Press 2 to deactivate cartoon shading")
        self.inst4 = addInstructions(0.30, "Press 3 to toggle fog")
        self.inst4 = addInstructions(0.36, "Press 4 to toggle free camera")
        self.inst4 = addInstructions(0.42, "Press 5 to toggle bloom")
        self.inst4 = addInstructions(0.48, "Press 6 to toggle Ambient Occlusion")
        self.inst4 = addInstructions(0.54, "Press Escape to toggle the onscreen debug")

        #Loading required modules...
        self.loadWorld()
        localAvatar = self.getActor()
        base.localAvatar = localAvatar
        self.LoadButtons()
        self.loadShaders()
        self.FogDensity = self.loadFog()

        self.objectList = list()
        self.objectList.append(self.scene)


        # Floater Object (For camera)
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(self.actorBody)
        self.floater.setY(-10)
        self.floater.setZ(8.5)
        self.floater.setHpr(0, -10, 0)

        # Set Camera
        self.camera.reparentTo(self.floater)

        # Accept the control keys for movement and rotation
        self.accept('f', self.toggleWireframe)
        self.accept('x', self.toggle_xray_mode)
        self.accept('b', self.toggle_model_bounds)
        self.accept("escape", self.toggle_osd)
        self.accept("1", self.loadCartoonShaders)
        self.accept("2", self.unloadShaders)
        self.accept("3", self.toggleFog)
        self.accept("4", self.toggleCamera)
        self.accept("5", self.toggleBloom)
        self.accept("6", self.toggleAmbientOcclusion)

        #warning: bright! self.accept("6", self.toggleInvert)


        self.accept("arrow_left", self.setKey, ["left", True])
        self.accept("arrow_right", self.setKey, ["right", True])
        self.accept("arrow_up", self.setKey, ["forward", True])
        self.accept("arrow_down", self.setKey, ["backward", True])
        self.accept("arrow_left-up", self.setKey, ["left", False])
        self.accept("arrow_right-up", self.setKey, ["right", False])
        self.accept("arrow_up-up", self.setKey, ["forward", False])
        self.accept("arrow_down-up", self.setKey, ["backward", False])

        self.taskMgr.add(self.move, "moveTask")




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
        base.setFrameRateMeter(True)
        PStatClient.connect()

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
                      'phase_13/models/parties/partyGrounds.bam',
                      'models/world.egg.pz',
                      'custom/ship/ship.egg']
        nameArray = ['Toontown Central', 'Party Grounds', 'Default World', 'Ship Test']

        for index, name in enumerate(nameArray):
            l = DirectButton(text=name, image=(Buttons), extraArgs=[modelArray[index]], command=self.spawnObject,
                             text_scale=0.045, text_pos=(0, -0.007, 0), relief=None)
            myScrolledList.addItem(l)

    #will be used to spawn objects
    def spawnObject(self, modelName):
        #if spawned object already exists, we're gonna need to remove it
        while len(self.objectList) >= 1:
            for world in self.objectList:
                world.removeNode()
            self.objectList.pop(0)

        spawnedObject = loader.loadModel(modelName)
        spawnedObject.reparentTo(render)
        spawnedObject.setPos(base.localAvatar.getPos())
        #spawnedObject = self.scene
        #self.removeWorld(self.objectList.find(spawnedObject))
        self.objectList.append(spawnedObject)
        print("Model Name: " + repr(modelName))
        print("Spawned Object: " + repr(spawnedObject))
        testobjectindex = len(self.objectList)
        print(testobjectindex)
        print(self.objectList)
        #self.removeWorld()


    def loadPStats(self):
        os.system("pstats.exe")


    def loadFog(self):
        self.fog = Fog('distanceFog')
        self.fog.setColor(0, 0, 0)
        self.fog.setExpDensity(.01)
        self.render.setFog(self.fog)
        self.fog.setOverallHidden(False)
        return self.fog.getExpDensity()

    def loadShaders(self):
        normalsBuffer = self.win.makeTextureBuffer("normalsBuffer", 0, 0)
        normalsBuffer.setClearColor(LVecBase4(0.5, 0.5, 0.5, 1))
        self.normalsBuffer = normalsBuffer
        normalsCamera = self.makeCamera(
            normalsBuffer, lens=self.cam.node().getLens())
        normalsCamera.node().setScene(self.render)

        drawnScene = self.normalsBuffer.getTextureCard()
        drawnScene.setTransparency(1)
        drawnScene.setColor(1, 1, 1, 0)
        drawnScene.reparentTo(self.render2d)
        self.drawnScene = drawnScene

    def toggleAmbientOcclusion(self):
        if not self.AOEnabled:
            self.filters.setAmbientOcclusion()
            self.AOEnabled = True
        else:
            self.filters.delAmbientOcclusion()
            self.AOEnabled = False

    def toggleInvert(self):
        if not self.invertEnabled:
            self.filters.setInverted()
            self.invertEnabled = True
        else:
            self.filters.delInverted()
            self.invertEnabled = False

    def toggleBloom(self):
        if not self.bloomEnabled:
            self.filters.setBloom()
            self.bloomEnabled = True
        else:
            self.filters.delBloom()
            self.bloomEnabled = False

    def toggleCamera(self):
        if not self.mouseEnabled:
            base.enableMouse()
            self.mouseEnabled = True
        else:
            base.disableMouse()
            self.camera.setPosHpr(0, 0, 0, 0, 0, 0)
            self.mouseEnabled = False

    def toggleFog(self):
        if not self.fogEnabled:
            self.fog.setExpDensity(self.FogDensity)
            self.fogEnabled = True
        else:
            self.fog.setExpDensity(0)
            self.fogEnabled = False

    def toggle_xray_mode(self):
        """Toggle X-ray mode on and off. This is useful for seeing the
        effectiveness of the portal culling."""
        self.xray_mode = not self.xray_mode
        if self.xray_mode:
            self.scene.setColorScale((1, 1, 1, 0.5))
            self.scene.setTransparency(TransparencyAttrib.MDual)
        else:
            self.scene.setColorScaleOff()
            self.scene.setTransparency(TransparencyAttrib.MNone)

    def toggle_model_bounds(self):
        """Toggle bounding volumes on and off on the models."""
        self.show_model_bounds = not self.show_model_bounds
        if self.show_model_bounds:
            for model in self.objectList:
                model.showBounds()
        else:
            for model in self.objectList:
                model.hideBounds()

    def toggle_osd(self):
        self.OSD = not self.OSD
        if self.OSD:
            self.onScreenDebug.enabled = True
        else:
            self.onScreenDebug.enabled = False

    def getAirborneHeight(self):
        return self.offset + 0.025000000000000001

    def updateOnScreenDebug(self, task):
        if(onScreenDebug.enabled):
            onScreenDebug.add('Avatar Position', base.localAvatar.getPos())
            onScreenDebug.add('Avatar Angle', base.localAvatar.getHpr())
            onScreenDebug.add('Camera Position', base.camera.getPos())
            onScreenDebug.add('Camera Angle', base.camera.getHpr())

        return Task.cont

    def unloadShaders(self):
        if self.shadersLoaded:
            self.drawnScene.hide()
            self.shadersLoaded = False

    def loadCartoonShaders(self):
        if not self.shadersLoaded:
            self.separation = 0.0015
            self.cutoff = 0.35
            inkGen = loader.loadShader("shaders/inkGen.sha")
            self.drawnScene.setShader(inkGen)
            self.drawnScene.setShaderInput("separation", LVecBase4(self.separation, 0, self.separation, 0))
            self.drawnScene.setShaderInput("cutoff", LVecBase4(self.cutoff))
            self.drawnScene.show()
            self.shadersLoaded = True


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
