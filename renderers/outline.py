import basilisk as bsk
import moderngl as mgl
from renderers.renderer import Renderer


class OutlineRenderer(Renderer):
    def __init__(self, scene):
        super().__init__(scene)

        self.main_shader = bsk.Shader(self.engine, frag='shaders/blank.frag')
        self.other_shader = bsk.Shader(self.engine, frag='shaders/blankOther.frag')
        self.outline_shader = bsk.Shader(self.engine, 'shaders/frame.vert', 'shaders/outline.frag')
        self.combine_shader = bsk.Shader(self.engine, 'shaders/frame.vert', 'shaders/combineOutline.frag')

        # self.temp_fbo = bsk.Framebuffer(self.engine)
        self.edge_detect_fbo = bsk.Framebuffer(self.engine, self.outline_shader)
        self.outline_fbo     = bsk.Framebuffer(self.engine)
        self.blank_fbo       = bsk.Framebuffer(self.engine)
        self.combine_fbo     = bsk.Framebuffer(self.engine, self.combine_shader)



    def render(self) -> None:
        """
        Renders the scene onto the fbo. Can access with Renderer.texture
        """
        
        self.scene.render(self.blank_fbo)


        self.edge_detect_fbo.bind(self.scene.frame.input_buffer.depth, 'depthTexture', 0)
        self.edge_detect_fbo.bind(self.scene.frame.input_buffer.color_attachments[2], 'normalTexture', 1)
        self.edge_detect_fbo.render(self.outline_fbo, auto_bind=False)

        self.combine_fbo.bind(self.blank_fbo.texture, 'mainTexture', 2)
        self.combine_fbo.bind(self.outline_fbo.texture, 'outlineTexture', 3)
        self.combine_fbo.render(self.fbo, auto_bind=False)
