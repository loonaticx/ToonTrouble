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
