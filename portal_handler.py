import basilisk as bsk
import glm
import moderngl as mgl
from renderers.renderer import Renderer


class PortalHandler:
    scene_main: bsk.Scene
    """The current primary scene. The scene the player/camera is in"""
    scene_other: bsk.Scene
    """The scene that is rendered in portals"""

    def __init__(self, game, main_renderer: Renderer, other_renderer: Renderer):
        """
        
        """
        
        # Back references
        self.game   = game
        self.engine = game.engine
        self.ctx    = main_renderer.scene.ctx

        # Load shaders
        self.portal_shader  = bsk.Shader(self.engine, 'shaders/portal.vert', 'shaders/portal.frag' )
        self.combine_shader = bsk.Shader(self.engine, 'shaders/frame.vert' , 'shaders/combine.frag')

        # Scene FBOs. Stores images and depths until needed
        self.portal_fbo  = bsk.Framebuffer(self.engine)
        self.combine_fbo = bsk.Framebuffer(self.engine, self.combine_shader)
      
        # Create a scene for the portals
        self.portal_scene = bsk.Scene(self.engine, shader=self.portal_shader)
        # Add a portal node
        self.portal = bsk.Node(position=(0, 0, 10), scale=(5, 5, 1))
        self.portal_scene.add(self.portal)
        self.portal_scene.camera = bsk.StaticCamera()
        self.portal_scene.sky = None

        self.set_levels(main_renderer, other_renderer)
        self.set_positions(glm.vec3(0, 0, 10), glm.vec3(5, 0, 5))
        self.set_rotations(glm.quat(0, 0, 0, 0), glm.quat(0, 0, 0, 0))

    def update(self):
        """
        Updates the portal scene
        """

        self.main_renderer.update()
        self.other_renderer.update()
        
        main_scene = self.main_renderer.scene
        other_scene = self.other_renderer.scene

        position_difference = main_scene.camera.position - self.portal.position

        other_scene.camera.position = self.other_position + position_difference
        
        self.portal_scene.camera.position = main_scene.camera.position
        self.portal_scene.camera.rotation = main_scene.camera.rotation
        self.portal_scene.update(render=False)


    def render(self):
        """
        Renders both of the active scenes and renders the portals
        """

        # Render the base scenes
        self.ctx.disable(mgl.CULL_FACE)
        self.portal_scene.render(self.portal_fbo)
        self.other_renderer.other_shader.bind(self.portal_scene.frame.input_buffer.depth, 'depthTexture', 1)
        self.ctx.enable(mgl.CULL_FACE)

        self.other_renderer.render()
        self.main_renderer.render()

        self.bind_all()

        # Render the portals, using the other fbo texture
        self.ctx.disable(mgl.CULL_FACE)
        self.portal_fbo.clear()
        self.portal_scene.render(self.portal_fbo)
        self.ctx.enable(mgl.CULL_FACE)

        # Render the combined scene
        self.combine_fbo.render(self.ctx.screen, auto_bind=False)


    def set_levels(self, main_renderer: Renderer, other_renderer: Renderer):
        """
        Sets the main and other scene. 
        Main scene is where the player is, other scene is what is shown in the portal. 
        """

        self.main_renderer  = main_renderer
        self.other_renderer = other_renderer

        self.main_renderer.set_main()
        self.other_renderer.set_other()

        self.bind_all()

    def bind_all(self):
        """
        Binds all the textures for the portal pipeline
        """
        
        # Fixes a Basilisk bug :P
        if self.other_renderer.scene.sky and 'skyboxTexture' in self.other_renderer.other_shader.uniforms:
            self.other_renderer.other_shader.bind(self.other_renderer.scene.sky.texture_cube, 'skyboxTexture', 8)
        
        # Bind all stages
        self.other_renderer.other_shader.bind(self.portal_scene.frame.input_buffer.depth, 'depthTexture', 1)
        self.portal_shader.bind(self.other_renderer.texture, 'otherTexture', 2)
        self.combine_shader.bind(self.main_renderer.texture, 'mainTexture', 3)
        self.combine_shader.bind(self.other_renderer.texture, 'portalTexture', 4)
        self.combine_shader.bind(self.main_renderer.scene.frame.input_buffer.depth,  'mainDepthTexture', 5)
        self.combine_shader.bind(self.portal_scene.frame.input_buffer.depth, 'portalDepthTexture', 6)

    def set_positions(self, main_position: glm.vec3, other_position: glm.vec3):
        """
        
        """
        
        self.portal.position = main_position
        self.other_position = other_position

    def set_rotations(self, main_rotation: glm.quat, other_position: glm.quat):
        """
        
        """

        self.portal.rotation = main_rotation
        self.other_rotation = other_position

    def swap(self):
        """
        
        """

        main_scene = self.main_renderer.scene

        main_scene.camera.position = self.other_position + main_scene.camera.position - self.portal.position
        self.portal.rotation, self.other_rotation = self.other_rotation, self.portal.rotation
        self.portal.position, self.other_position = glm.vec3(self.other_position), glm.vec3(self.portal.position.data)

        self.main_renderer, self.other_renderer = self.other_renderer, self.main_renderer

        self.main_renderer.set_main()
        self.other_renderer.set_other()

        self.update()
        self.bind_all()