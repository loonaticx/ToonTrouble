from panda3d.core import *

def makeLightOne(render):
    directionalLight = DirectionalLight('directionalLight')
    directionalLight.setColor((0.8, 0.2, 0.2, 1))
    return render.attachNewNode(directionalLight);

def setLight(render):
    # This light is facing backwards, towards the camera.
    directionalLightNP.setHpr(180, -20, 0)
    render.setLight(directionalLightNP)

    directionalLight = DirectionalLight('directionalLight')
    directionalLight.setColor((0.2, 0.2, 0.8, 1))
    directionalLightNP = render.attachNewNode(directionalLight)
    # This light is facing forwards, away from the camera.
    directionalLightNP.setHpr(0, -20, 0)
    render.setLight(directionalLightNP)