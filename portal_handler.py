import basilisk as bsk


class PortalHandler:
    scene_main: bsk.Scene
    """The current primary scene. The scene the player/camera is in"""
    scene_other: bsk.Scene
    """The scene that is rendered in portals"""

    def __init__(self, game, main_scene: bsk.Scene, other_scene: bsk.Scene):
        """
        
        """
        
        # Back references
        self.game   = game
        self.engine = game.engine
        self.ctx    = main_scene.ctx

        # Load shaders
        self.blank_shader   = bsk.Shader(self.engine, 'shaders/blank.vert' , 'shaders/blank.frag'  )
        self.other_shader   = bsk.Shader(self.engine, 'shaders/other.vert' , 'shaders/other.frag'  )
        self.portal_shader  = bsk.Shader(self.engine, 'shaders/portal.vert', 'shaders/portal.frag' )
        self.combine_shader = bsk.Shader(self.engine, 'shaders/frame.vert' , 'shaders/combine.frag')

        # Scene FBOs. Stores images and depths until needed
        self.main_fbo    = bsk.Framebuffer(self.engine)
        self.other_fbo   = bsk.Framebuffer(self.engine)
        self.portal_fbo  = bsk.Framebuffer(self.engine)
        self.combine_fbo = bsk.Framebuffer(self.engine, self.combine_shader)
      
        # Create a scene for the portals
        self.portal_scene = bsk.Scene(self.engine, shader=self.portal_shader)
        # Add a portal node
        self.portal = bsk.Node(position=(0, 0, 10), scale=(5, 5, .1))
        self.portal_scene.add(self.portal)

        self.set_scenes(main_scene, other_scene)

    def update(self):
        """
        Updates the portal scene
        """
        
        self.portal_scene.update(render=False)

    def render(self):
        """
        Renders both of the active scenes and renders the portals
        """

        # Render the base scenes
        self.portal_scene.render(self.portal_fbo)
        self.other_shader.bind(self.portal_scene.frame.input_buffer.depth, 'testTexture', 1)
        self.other_scene.render(self.other_fbo)
        self.main_scene.render(self.main_fbo)

        # Render the portals, using the other fbo texture
        self.portal_fbo.clear()
        self.portal_scene.render(self.portal_fbo)

        # Render the combined scene
        self.combine_fbo.render(auto_bind=False)

    def set_scenes(self, main_scene: bsk.Scene, other_scene: bsk.Scene):
        """
        Sets the main and other scene. 
        Main scene is where the player is, other scene is what is shown in the portal. 
        """

        self.main_scene   = main_scene
        self.other_scene  = other_scene
        self.other_scene.shader = self.other_shader

        self.bind_all()

    def bind_all(self):
        """
        Binds all the textures for the portal pipeline
        """
        
        # Fixes a Basilisk bug :P
        self.other_shader.bind(self.other_scene.sky.texture_cube, 'skyboxTexture', 8)
        
        # Bind all stages
        self.other_shader.bind  (self.portal_scene.frame.input_buffer.depth, 'testTexture', 1)
        self.portal_shader.bind (self.other_fbo.texture, 'otherTexture', 2)
        self.combine_shader.bind(self.main_fbo.texture, 'mainTexture', 3)
        self.combine_shader.bind(self.portal_fbo.texture, 'portalTexture', 4)
        self.combine_shader.bind(self.main_scene.frame.input_buffer.depth,  'mainDepthTexture', 5)
        self.combine_shader.bind(self.portal_scene.frame.input_buffer.depth, 'portalDepthTexture', 6)