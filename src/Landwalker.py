import os

from panda3d.core import *
from panda3d.core import CollisionTraverser
from panda3d.core import PandaNode, NodePath, TextNode

import ActorManager
from direct.controls.GravityWalker import GravityWalker
from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectScrolledList import DirectScrolledList
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from src import Customize, ActorDict


#import ConfigMgr


#borrowed the xray mod from /samples/culling/portal_culling.py
# https://www.panda3d.org/manual/?title=Common_Image_Filters
#possibly make a slider for bloom
#YO WHAT IF I MAKE A BENCHMARK PROGRAM

offset = 3.2375

actor = ActorManager

# Store which keys are currently pressed
keyMap = {
    "1": 0,
    "escape": 0,
    "left": 0,
    "right": 0,
    "forward": 0,
    "backward": 0,
    "cam-left": 0,
    "cam-right": 0,
}


def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1),
                        parent=base.a2dTopLeft, align=TextNode.ALeft,
                        pos=(0.08, -pos - 0.04), scale=.05)

class Landwalker(ShowBase):
    def __init__():
        loadPrcFile('../config/Config.prc')
        #loadPrcFile("Config.prc")
        ShowBase.__init__()
        #config = ConfigMgr.loadSettings()

        #Config stuff here
        filters = CommonFilters(base.win, base.cam)
        AOEnabled = False
        bloomEnabled = False
        invertEnabled = False
        OSD = True
        shadersLoaded = False
        xray_mode = False
        show_model_bounds = False
        fogEnabled = True
        mouseEnabled = False



def loadGame():
    # Adding onscreen text here
    inst1 = addInstructions(0.06, "Press F to toggle wireframe")
    inst2 = addInstructions(0.12, "Press X to toggle xray")
    inst3 = addInstructions(0.18, "Press 1 to activate cartoon shading")
    inst4 = addInstructions(0.24, "Press 2 to deactivate cartoon shading")
    inst4 = addInstructions(0.30, "Press 3 to toggle fog")
    inst4 = addInstructions(0.36, "Press 4 to toggle free camera")
    inst4 = addInstructions(0.42, "Press 5 to toggle bloom")
    inst4 = addInstructions(0.48, "Press 6 to toggle Ambient Occlusion")
    inst4 = addInstructions(0.54, "Press Escape to toggle the onscreen debug")

    #Loading required modules...
    scene = loadWorld()
    localAvatar = actor.makeActor(scene, False)
    #localAvatar.reparentTo(render)
    #localAvatar.reparentTo(scene.find('**/ground'))

    base.localAvatar = localAvatar
    LoadButtons()
    #loadShaders()
    FogDensity = loadFog()

    objectList = list()
    objectList.append(scene)


    # Floater Object (For camera)
    floater = NodePath(PandaNode("floater"))
    floater.reparentTo(localAvatar)
    floater.setY(-10)
    floater.setZ(8.5)
    floater.setHpr(0, -10, 0)

    # Set Camera
    camera.reparentTo(floater)

    # Accept the control keys for movement and rotation
    #ShowBase.accept('f', toggleWireframe)
    #ShowBase.accept('x', toggle_xray_mode)
    #ShowBase.accept('b', toggle_model_bounds)
    #ShowBase.accept("escape", toggle_osd)
    #ShowBase.accept("1", loadCartoonShaders)
    #ShowBase.accept("2", unloadShaders)
    #ShowBase.accept("3", toggleFog)
    #ShowBase.accept("4", toggleCamera)
    #ShowBase.accept("5", toggleBloom)
    #ShowBase.accept("6", toggleAmbientOcclusion)

    #warning: bright! accept("6", toggleInvert)


    #accept("arrow_left", setKey, ["left", True])
    #accept("arrow_right", setKey, ["right", True])
    #accept("arrow_up", setKey, ["forward", True])
    #accept("arrow_down", setKey, ["backward", True])
    #accept("arrow_left-up", setKey, ["left", False])
    #accept("arrow_right-up", setKey, ["right", False])
    #accept("arrow_up-up", setKey, ["forward", False])
    #accept("arrow_down-up", setKey, ["backward", False])

    taskMgr.add(move, "moveTask")




    offset = 3.2375

    wallBitmask = BitMask32(1)
    floorBitmask = BitMask32(2)
    base.cTrav = CollisionTraverser()

    walkControls = GravityWalker(legacyLifter=True)
    walkControls.setWallBitMask(wallBitmask)
    walkControls.setFloorBitMask(floorBitmask)
    walkControls.setWalkSpeed(16.0, 24.0, 8.0, 80.0)
    walkControls.initializeCollisions(base.cTrav, localAvatar, floorOffset=0.025, reach=4.0)
    walkControls.setAirborneHeightFunc(getAirborneHeight())
    walkControls.enableAvatarControls()
    # controlManager.add(walkControls, 'walk')
    localAvatar.physControls = walkControls

    localAvatar.physControls.placeOnFloor()
    # problem: onScreenDebug.enabled = toggle

    # print(updateOnScreenDebug.enabled)

    onScreenDebug.enabled = True
    base.setFrameRateMeter(True)
    PStatClient.connect()

    base.taskMgr.add(updateOnScreenDebug, 'UpdateOSD')

def loadWorld():
    #Loading our Scene
    background = loader.loadModel("models/world.egg.pz")
    background.reparentTo(render)
    return background

    #scene.setBackgroundColor(0.53, 0.80, 0.92, 1)

def removeWorld(scene):
    scene.removeNode()

def getActor():
    # Loading our Actor
    actorStartPos = scene.find("**/start_point").getPos()
    actorBody = ActorDict.playerBody
    actorBody.reparentTo(render)
    actorBody.loop('neutral')
    actorBody.setPos(actorStartPos + (0, 0, 1.5))
    actorBody.setScale(0.3)
    actorBody.setH(-180)

    def ActorHead():
        actorHead = loader.loadModel("custom/def_m.bam")
        actorHead.reparentTo(actorBody.find('**/to_head'))
        actorHead.setScale(0.20)
        actorHead.setZ(0)
        actorHead.setH(-180)

    ActorHead()
    return actorBody

def LoadButtons():
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
        l = DirectButton(text=name, image=(Buttons), extraArgs=[modelArray[index]], command=spawnObject,
                         text_scale=0.045, text_pos=(0, -0.007, 0), relief=None)
        myScrolledList.addItem(l)

#will be used to spawn objects
def spawnObject(modelName):
    #if spawned object already exists, we're gonna need to remove it
    while len(objectList) >= 1:
        for world in objectList:
            world.removeNode()
        objectList.pop(0)

    spawnedObject = loader.loadModel(modelName)
    spawnedObject.reparentTo(render)
    spawnedObject.setPos(base.localAvatar.getPos())
    #spawnedObject = scene
    #removeWorld(objectList.find(spawnedObject))
    objectList.append(spawnedObject)
    print("Model Name: " + repr(modelName))
    print("Spawned Object: " + repr(spawnedObject))
    testobjectindex = len(objectList)
    print(testobjectindex)
    print(objectList)
    #removeWorld()


def loadPStats():
    os.system("pstats.exe")


def loadFog():
    fog = Fog('distanceFog')
    fog.setColor(0, 0, 0)
    fog.setExpDensity(.01)
    render.setFog(fog)
    fog.setOverallHidden(False)
    return fog.getExpDensity()

def loadShaders():
    normalsBuffer = win.makeTextureBuffer("normalsBuffer", 0, 0)
    normalsBuffer.setClearColor(LVecBase4(0.5, 0.5, 0.5, 1))
    normalsBuffer = normalsBuffer
    normalsCamera = makeCamera(
        normalsBuffer, lens=cam.node().getLens())
    normalsCamera.node().setScene(render)

    drawnScene = normalsBuffer.getTextureCard()
    drawnScene.setTransparency(1)
    drawnScene.setColor(1, 1, 1, 0)
    drawnScene.reparentTo(render2d)
    drawnScene = drawnScene

def toggleAmbientOcclusion():
    if not AOEnabled:
        filters.setAmbientOcclusion()
        AOEnabled = True
    else:
        filters.delAmbientOcclusion()
        AOEnabled = False

def toggleInvert():
    if not invertEnabled:
        filters.setInverted()
        invertEnabled = True
    else:
        filters.delInverted()
        invertEnabled = False

def toggleBloom():
    if not bloomEnabled:
        filters.setBloom()
        bloomEnabled = True
    else:
        filters.delBloom()
        bloomEnabled = False

def toggleCamera():
    if not mouseEnabled:
        base.enableMouse()
        mouseEnabled = True
    else:
        base.disableMouse()
        camera.setPosHpr(0, 0, 0, 0, 0, 0)
        mouseEnabled = False

def toggleFog():
    if not fogEnabled:
        fog.setExpDensity(FogDensity)
        fogEnabled = True
    else:
        fog.setExpDensity(0)
        fogEnabled = False

def toggle_xray_mode():
    """Toggle X-ray mode on and off. This is useful for seeing the
    effectiveness of the portal culling."""
    xray_mode = not xray_mode
    if xray_mode:
        scene.setColorScale((1, 1, 1, 0.5))
        scene.setTransparency(TransparencyAttrib.MDual)
    else:
        scene.setColorScaleOff()
        scene.setTransparency(TransparencyAttrib.MNone)

def toggle_model_bounds():
    """Toggle bounding volumes on and off on the models."""
    show_model_bounds = not show_model_bounds
    if show_model_bounds:
        for model in objectList:
            model.showBounds()
    else:
        for model in objectList:
            model.hideBounds()

def toggle_osd():
    OSD = not OSD
    if OSD:
        onScreenDebug.enabled = True
    else:
        onScreenDebug.enabled = False

def getAirborneHeight():
    return offset + 0.025000000000000001

def updateOnScreenDebug(task):
    if(onScreenDebug.enabled):
        onScreenDebug.add('Avatar Position', base.localAvatar.getPos())
        onScreenDebug.add('Avatar Angle', base.localAvatar.getHpr())
        onScreenDebug.add('Camera Position', base.camera.getPos())
        onScreenDebug.add('Camera Angle', base.camera.getHpr())

    return Task.cont

def unloadShaders():
    if shadersLoaded:
        drawnScene.hide()
        shadersLoaded = False

def loadCartoonShaders():
    if not shadersLoaded:
        separation = 0.0015
        cutoff = 0.35
        inkGen = loader.loadShader("shaders/inkGen.sha")
        drawnScene.setShader(inkGen)
        drawnScene.setShaderInput("separation", LVecBase4(separation, 0, separation, 0))
        drawnScene.setShaderInput("cutoff", LVecBase4(cutoff))
        drawnScene.show()
        shadersLoaded = True


# Records the state of the arrow keys
def setKey(key, value):
    keyMap[key] = value



# Accepts arrow keys to move either the player or the menu cursor,
# Also deals with grid checking and collision detection
def move(task):
    dt = globalClock.getDt()
    if keyMap["forward"]:
            base.localAvatar.setY(base.localAvatar, 20 * dt)
    elif keyMap["backward"]:
            base.localAvatar.setY(base.localAvatar, -20 * dt)
    if keyMap["left"]:
            base.localAvatar.setHpr(base.localAvatar.getH() + 1.5, base.localAvatar.getP(), base.localAvatar.getR())
    elif keyMap["right"]:
            base.localAvatar.setHpr(base.localAvatar.getH() - 1.5, base.localAvatar.getP(), base.localAvatar.getR())

    currentAnim = base.localAvatar.getCurrentAnim()

    if keyMap["forward"]:
        if currentAnim != "walk":
            base.localAvatar.loop("walk")
    elif keyMap["backward"]:
        # Play the walk animation backwards.
        if currentAnim != "walk":
            base.localAvatar.loop("walk")
        base.localAvatar.setPlayRate(-1.0, "walk")
    elif keyMap["left"] or keyMap["right"]:
        if currentAnim != "walk":
            base.localAvatar.loop("walk")
        base.localAvatar.setPlayRate(1.0, "walk")
    else:
        if currentAnim is not None:
            base.localAvatar.stop()
            base.localAvatar.loop("neutral")
            isMoving = False

    return task.cont


