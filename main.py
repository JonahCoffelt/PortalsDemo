import basilisk as bsk
import level_1, level_2
from portal_handler import PortalHandler

class App:
    def __init__(self):
        self.engine  = bsk.Engine(title=None)
        self.scene_1 = bsk.Scene(self.engine)
        self.scene_2 = bsk.Scene(self.engine)

        self.portal_handler = PortalHandler(self, self.scene_1, self.scene_2)

    def load_meshes(self):
        ...

    def load_textures(self):
        ...

    def load_levels(self):
        level_1.load(self, self.scene_1)
        level_2.load(self, self.scene_2)

    def render(self):
        self.portal_handler.render()

    def update(self):
        self.scene_1.update(render=False)
        self.scene_2.update(render=False)
        self.portal_handler.update()

        self.render()

        self.engine.update(render=False)

    def start(self):

        self.load_meshes()
        self.load_textures()
        self.load_levels()

        while self.engine.running:

            if self.engine.keys[bsk.pg.K_1] and not self.engine.previous_keys[bsk.pg.K_1]:
                self.portal_handler.swap()

            self.update()


app = App()
app.start()