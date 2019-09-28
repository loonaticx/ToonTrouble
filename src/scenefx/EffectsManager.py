import math
from panda3d.core import Fog, LVecBase4

# EffectsManager.fog.loadFog(arg)?

def loadShaders():
    normalsBuffer = base.win.makeTextureBuffer("normalsBuffer", 0, 0)
    normalsBuffer.setClearColor(LVecBase4(0.5, 0.5, 0.5, 1))
    normalsBuffer = normalsBuffer
    normalsCamera = base.makeCamera(
        normalsBuffer, lens=base.cam.node().getLens())
    normalsCamera.node().setScene(render)

    drawnScene = normalsBuffer.getTextureCard()
    drawnScene.setTransparency(1)
    drawnScene.setColor(1, 1, 1, 0)
    drawnScene.reparentTo(render2d)
    print("loading shaders...")
    return drawnScene

def toggleAmbientOcclusion(AOEnabled):
    if not AOEnabled:
        filters.setAmbientOcclusion()
        return True
    else:
        filters.delAmbientOcclusion()
        return False

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

def toggleFog(fog, fogEnabled, FogDensity):
    if not fogEnabled:
        return fog.setExpDensity(FogDensity)
        #return True
    else:
        return fog.setExpDensity(0)
        #return False

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
