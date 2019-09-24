from direct.showbase.ShowBase import ShowBase

from src import Landwalker

land = Landwalker()

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        land()




        #self.camera.reparentTo(self.render)
        #self.camera.show()


app = MyApp()
app.run()