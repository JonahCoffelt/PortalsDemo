import basilisk as bsk
from portal import Portal
import glm

class PortalHandler:
    portals: list[list[Portal]]
    """"""
    def __init__(self, game: ...) -> None:
        """
        Handles all the rendering and interactions of portals
        """
        
        # Parent Basilisk references
        self.game = game
        self.engine = game.engine

        # Shaders for the portal pipeline
        self.depth_shader  = bsk.Shader(self.engine, 'shaders/depth.vert',  'shaders/depth.frag' )
        """Shader used for the depth prepass"""
        self.portal_shader = bsk.Shader(self.engine, 'shaders/portal.vert', 'shaders/portal.frag')
        """Shader used when rendering the portals in the player's view"""
        self.color_shader  = bsk.Shader(self.engine, 'shaders/color.vert', 'shaders/color.frag')
        """Shader used when rendering the portal's view"""

        # Scene fpr all the portals
        self.portal_scene = bsk.Scene(self.engine, shader=self.portal_shader)
        self.portal_scene.camera = self.game.scene.camera

    def add(self, scene: bsk.Scene, open_position: tuple[int], end_position: tuple[int], scale: tuple[int]=(1, 1, 1)):
        """
        
        """
        
        self.portal_1 = Portal(self, scene, open_position, scale)
        self.portal_2 = Portal(self, scene, end_position,  scale)

        self.portal_1.link = self.portal_2
        self.portal_2.link = self.portal_1

        self.portal_1.set_index(1)
        self.portal_2.set_index(0)

        self.portal_shader.bind(self.portal_1.color_fbo.texture, "portalTexture1", 1)
        self.portal_shader.bind(self.portal_2.color_fbo.texture, "portalTexture2", 2)
        self.color_shader.bind(self.portal_1.depth_fbo.depth, "portalDepthTexture1", 3)
        self.color_shader.bind(self.portal_2.depth_fbo.depth, "portalDepthTexture2", 4)

    def render(self) -> None:
        self.portal_scene.render()

    def update(self, camera: bsk.FreeCamera):
        self.portal_scene.update(render=False)

        # Depth prepass for each portal
        self.portal_1.depth_prepass(camera)
        self.portal_2.depth_prepass(camera)

        # View pass
        self.game.scene.light_handler.write(self.color_shader.program)
        self.portal_1.color_prepass(camera)
        self.portal_2.color_prepass(camera)
        
    def __getitem__(self, key: bsk.Node) -> Portal: # TODO this will need to be adapted to handle multiple portal pairs preferably stored as a dict[bsk.Node, Portal]
        if key == self.portal_1.node: return self.portal_1
        if key == self.portal_2.node: return self.portal_2