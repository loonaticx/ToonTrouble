import math
from panda3d.core import Fog


def loadFog(fogDensity):
    fog = Fog('distanceFog')
    fog.setColor(0, 0, 0)
    fog.setExpDensity(fogDensity * (math.pow(10, -2)))
    render.setFog(fog)
    fog.setOverallHidden(False)
    #fog.getExpDensity()
    print(fog.getExpDensity())
    print("tried to load fog")
    return fog


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
