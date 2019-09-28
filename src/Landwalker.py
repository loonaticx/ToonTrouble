import os
import sys

from panda3d.core import *
from panda3d.core import CollisionTraverser
from panda3d.core import PandaNode, NodePath

from direct.controls.GravityWalker import GravityWalker
from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectScrolledList import DirectScrolledList
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from src.actor import ActorDict, ActorManager
from src import AvatarControls, GameGlobals
from src.scenefx import EffectsManager

#borrowed the xray mod from /samples/culling/portal_culling.py
# https://www.panda3d.org/manual/?title=Common_Image_Filters
#possibly make a slider for bloom
#YO WHAT IF I MAKE A BENCHMARK PROGRAM

objectList = list()

actor = ActorManager

#filters = CommonFilters(base.win, base.cam)
graphicShaders = EffectsManager

def loadGame():
    # Setting up key maps and the instruction set into the scene...
    GameGlobals.setKeys()
    GameGlobals.setInstructions()

    # Loads our world.
    scene = loadWorld()

    # Makes our local avatar.
    localAvatar = actor.makeActor()
    base.localAvatar = localAvatar
    base.localAvatar.reparentTo(render)

    # Load our buttons.
    LoadButtons()

    # Load our shaders.
    #fog = loadFog()
    #print(fogStats(fog))
    EffectsManager.loadShaders()
    #FogDensity = EffectsManager.loadFog(1)

    # Floater Object (For camera)
    floater = NodePath(PandaNode("floater"))
    floater.reparentTo(localAvatar)
    floater.setY(-10)
    floater.setZ(8.5)
    floater.setHpr(0, -10, 0)

    # Set Camera
    camera.reparentTo(floater)

    wallBitmask = BitMask32(1)
    floorBitmask = BitMask32(2)
    base.cTrav = CollisionTraverser()

    # Walk controls
    walkControls = GravityWalker(legacyLifter=True)
    walkControls.setWallBitMask(wallBitmask)
    walkControls.setFloorBitMask(floorBitmask)
    walkControls.setWalkSpeed(16.0, 24.0, 8.0, 80.0)
    walkControls.initializeCollisions(base.cTrav, localAvatar, floorOffset=0.025, reach=4.0)
    walkControls.setAirborneHeightFunc(AvatarControls.getAirborneHeight())
    walkControls.enableAvatarControls()
    # controlManager.add(walkControls, 'walk')
    localAvatar.physControls = walkControls
    localAvatar.physControls.placeOnFloor()

    # Some debug stuff, should be moved later once I can toggle stuff from different files./
    onScreenDebug.enabled = True
    base.setFrameRateMeter(True)
    base.taskMgr.add(AvatarControls.move, "moveTask")
    base.taskMgr.add(updateOnScreenDebug, 'UpdateOSD')

# Loading our world.
def loadWorld():
    # Loading our Scene
    background = loader.loadModel('phase_4/models/neighborhoods/toontown_central.bam')
    background.reparentTo(render)
    background.show()
    objectList.append(background)
    print("Loading world")
    return background

def removeWorld(scene):
    scene.removeNode()

# This shouldn't exist in the future for this class.
def loadFog():
    fog = Fog('distanceFog')
    fog.setColor(0, 0, 0)
    fog.setExpDensity(.07)
    render.setFog(fog)
    fog.setOverallHidden(False)
    return fog

def fogStats(fog):
    return [fog, fog.getExpDensity(), GameGlobals.fogEnabled]

# Loading our actor.
def getActor():
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

# Loading onscreen buttons.
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

# Used to spawn objects within the scene.
def spawnObject(modelName):
    # If spawned object already exists, we're gonna need to remove it
    while len(objectList) >= 1:
        for world in objectList:
            world.removeNode()
        objectList.pop(0)

    spawnedObject = loader.loadModel(modelName)
    spawnedObject.reparentTo(render)
    spawnedObject.setPos(base.localAvatar.getPos())
    objectList.append(spawnedObject)

    print("Model Name: " + repr(modelName))
    print("Spawned Object: " + repr(spawnedObject))

def toggle_osd():
    OSD = not OSD
    if OSD:
        onScreenDebug.enabled = True
    else:
        onScreenDebug.enabled = False

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

