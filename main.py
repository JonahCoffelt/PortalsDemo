import basilisk as bsk
import level_1, level_2
from portal_handler import PortalHandler
from renderers.renderer import Renderer
from renderers.kuwahara import KuwaharaRenderer
from renderers.pixel import PixelRenderer, PixelQuantizedRenderer
from renderers.outline import OutlineRenderer
from renderers.gooch import GoochRenderer, GoochInvertedRenderer
from renderers.blank import BlankRenderer
from renderers.quantize import QuantizeRenderer

class App:
    def __init__(self):
        self.engine  = bsk.Engine(title=None)
        self.scene_1 = bsk.Scene(self.engine)
        self.scene_2 = bsk.Scene(self.engine)

    def load_meshes(self):
        ...

    def load_textures(self):
        self.img = bsk.Image('main_fbo.png')
        self.mtl = bsk.Material(texture=self.img)


    def load_levels(self):
        level_1.load(self, self.scene_1)
        level_2.load(self, self.scene_2)

    def render(self):
        self.portal_handler.render()

    def update(self):
        self.portal_handler.update()

        self.render()

        self.engine.update()

    def start(self):

        self.load_meshes()
        self.load_textures()
        self.load_levels()

        self.renderer_1 = Renderer(self.scene_1)
        self.renderer_2 = GoochInvertedRenderer(self.scene_2)

        self.portal_handler = PortalHandler(self, self.renderer_1, self.renderer_2)

        while self.engine.running:

            if self.engine.keys[bsk.pg.K_1] and not self.engine.previous_keys[bsk.pg.K_1]:
                self.portal_handler.swap()

            self.update()


app = App()
app.start()