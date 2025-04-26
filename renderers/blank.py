import basilisk as bsk
import moderngl as mgl
from renderers.renderer import Renderer


class BlankRenderer(Renderer):
    def __init__(self, scene):
        super().__init__(scene)

        self.main_shader = bsk.Shader(self.engine, frag='shaders/blank.frag')
        self.other_shader = bsk.Shader(self.engine, frag='shaders/blankOther.frag')
