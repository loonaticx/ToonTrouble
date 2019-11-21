from src.actor import ActorDict
def makeActor(environ, debugTemp):
    def makeActor():
        # Loading our Actor
        actorBody = ActorDict.playerBody
        actorBody.loop('neutral')
        #actorBody.setPos(0, -2, 0)
        actorBody.setScale(0.5)
        actorBody.setP(90)
        #actorBody.place()

        def ActorHead():
            actorHead = loader.loadModel("custom/def_m.bam")
            actorHead.reparentTo(actorBody.find('**/to_head'))
            actorHead.setScale(0.20)
            actorHead.setZ(0)
            actorHead.setH(-180)
            return actorHead

        actorHead = ActorHead()
        #objectList.append(actorHead)
        return actorBody

    actorBody = makeActor()
    if debugTemp:
        actorBody.reparentTo(environ.find('**/ground'))
    else:
        actorBody.reparentTo(environ.find("**/start_point"))


    return actorBody