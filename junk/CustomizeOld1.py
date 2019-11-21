from panda3d.core import Fog

from direct.gui.DirectScrolledList import DirectScrolledList, DirectButton
from direct.interval.FunctionInterval import Func
from direct.interval.MetaInterval import Sequence
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import Point3
from src.actor import ActorDict


#ideas for changing torso:
#for *each* file(texture) in directory(shirts), add each element into shirtList arr. do the same with pants, sleeve, etc
#and then do a texture flip 180 degrees, attach texture to corresponding nodes, maybe a directScrollList might work..
#i think we should revert this back into a class but instead of Showbase do DirectObject


class Customize(DirectObject):

    def __init__(self):
        #ShowBase.__init__(self)
        #self.testModel = loader.loadModel('phase_4/models/props/snowball.bam')
        self.loadScene()
        #base.disableMouse()
        #base.oobe()
        #print(self.camera.getPos())
        #self.testModel.reparentTo(render)
        #self.camera.setPos(0,0,0)
        #self.testModel.setPos(self.camera.getPos())
        #self.testModel.hide()
        #self.camera.reparentTo(self.testModel)


        #self.camInterval(self.camera)
        #self.camInterval(self.testModel)

        #self.testTwo = loader.loadModel('phase_4/models/char/suitA-heads.bam')
        #self.testTwo.reparentTo(render)
        #self.testCogHeadsHere()

    def testCogHeadsHere(self):
        modelArrTwo = ['phase_4/models/char/suitA-heads.bam']
        for modelName in modelArrTwo:
            tempLoader = loader.loadModel(modelName)
            for node in tempLoader.nodes:
                print(node)
        print(self.testTwo.nodes)
        print(self.testTwo.ancestors)
        print(self.testTwo.children)
        print(self.testTwo.findAllMaterials())
        print(self.testTwo.getNodes())

    def annoyingTempHeadList(self):
        self.backstabber = loader.loadModel('phase_4/models/char/suitA-heads.bam').find('**/backstabber')
        self.bigcheese = loader.loadModel('phase_4/models/char/suitA-heads.bam').find('**/bigcheese')
        self.bigwig = loader.loadModel('phase_4/models/char/suitA-heads.bam').find('**/bigwig')
        return [self.backstabber, self.bigcheese, self.bigwig]




    def loadScene(self):
        self.loadBackground()
        self.getActor()
        self.loadFog()
        self.objectList = list()
        self.objectList.append(self.actorHead)

    def loadFog(self):
        self.fog = Fog('distanceFog')
        self.fog.setColor(0, 0, 0)
        self.fog.setExpDensity(.07)
        self.render.setFog(self.fog)
        self.fog.setOverallHidden(False)
        return self.fog.getExpDensity()


    def loadBackground(self):
        self.background = loader.loadModel('phase_4/models/minigames/treehouse_2players.bam')
        self.background.reparentTo(render)
        self.background.place()
        self.background.setPosHprScale(0.00, 15.00, -3.00, 0.00, 270.00, 180.00, 1.00, 1.00, 1.00)


    def getActor(self):
        # Loading our Actor
        self.actorBody = ActorDict.playerBody
        self.actorBody.reparentTo(self.background.find('**/ground'))
        self.actorBody.loop('neutral')
        #self.actorBody.setPos(0, -2, 0)
        self.actorBody.setScale(0.5)
        self.actorBody.setP(90)
        #self.actorBody.place()

        def ActorHead():
            actorHead = loader.loadModel("custom/def_m.bam")
            actorHead.reparentTo(self.actorBody.find('**/to_head'))
            actorHead.setScale(0.20)
            actorHead.setZ(0)
            actorHead.setH(-180)
            return actorHead

        self.actorHead = ActorHead()
        return self.actorBody

    def camInterval(self, cam):
        inc = cam.getX(), cam.getY() + 10, cam.getZ()
        #print(inc)
        #maybe a list of numbers-- an array for x, y, z, a method (manX, manY, manZ) man = manipulate by +- int, ret that array which will be used
        #as the Point3 args. if args are NaN/0/null, just ret the xyz arr. will be used to get the last position args for after the sequence finalizes.
        # just realized, look at line 53 instead of array
        intervalOne = cam.posInterval(4.0, Point3(inc))
        #print('pos during interval: ', str(cam.getPos()))
        camSequence = Sequence(intervalOne)
        camSequence.append(Func(self.loadButtons))

        #print(camSequence.__len__())

        camSequence.start()
        #cam.setPos(inc)
        #print ('Pos after interval: ' + str(cam.getPos()))

        #return cam.setPos(cam.getPos())

        #so apparently with the test model it doesn't revert back to 0,0,0
        #just for now, should change later.
        #cam.setPos(cam.getX(), cam.getY() + 10, cam.getZ())

        #if i wanted to make the model change for example during the interval, i could do an event https://www.panda3d.org/manual/?title=Event_Handlers

    def loadButtons(self):
        #arrowUp = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui.bam').find('**/nextUp')
        #arrowDown = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui.bam').find('**/nextDown')
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
                      'models/world.egg.pz']
        nameArray = ['Head 1', 'Head 2', 'Head 3']

        thisIsTemp = self.annoyingTempHeadList()

        #for each model in modelArray --> for each node in nodePath, append to array

        for index, name in enumerate(nameArray):
            l = DirectButton(text=name, image=(Buttons), extraArgs=[thisIsTemp[index]], command=self.changeHead,
                             text_scale=0.045, text_pos=(0, -0.007, 0), relief=None)
            myScrolledList.addItem(l)

    def changeHead(self, modelName):
        #if spawned object already exists, we're gonna need to remove it
        while len(self.objectList) >= 1:
            for head in self.objectList:
                head.detachNode()
            self.objectList.pop(0)

        spawnedObject = modelName
        #spawnedObject = loader.loadModel(modelName)
        spawnedObject.reparentTo(self.actorBody.find('**/to_head'))
        spawnedObject.setZ(0.05)
        #eventually havea task to be able to rotate the head around

        #spawnedObject = self.scene
        #self.removeWorld(self.objectList.find(spawnedObject))
        self.objectList.append(spawnedObject)
        #print("Model Name: " + repr(modelName))
        #print("Spawned Object: " + repr(spawnedObject))
        testobjectindex = len(self.objectList)
        #print(testobjectindex)
        #print(self.objectList)



game = Customize()
game.run()