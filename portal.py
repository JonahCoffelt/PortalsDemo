import basilisk as bsk
import glm

class Portal:
    def __init__(self, portal_handler: ..., scene: bsk.Scene, position: tuple[int], scale: tuple[int]) -> None:
        """
        
        """
        
        self.portal_handler = portal_handler
        self.engine = scene.engine

        # Get the scenes
        self.game_scene = scene
        self.portal_scene = self.portal_handler.portal_scene
        
        # Get the shaders
        self.game_shader   = self.game_scene.shader
        self.color_shader  = self.portal_handler.color_shader
        self.portal_shader = self.portal_handler.portal_shader
        self.depth_shader  = self.portal_handler.depth_shader

        # Other portal that this portal is linked to
        self.link: Portal = None

        # FBOs for the pre and post pass
        self.depth_fbo = bsk.Framebuffer(self.engine)
        self.color_fbo = bsk.Framebuffer(self.engine)

        # Load the mesh for the portal (cube with custom data)
        self.mesh = bsk.Mesh('assets/vertical_plane.obj', custom_format=True)
        self.mesh.data[:,3] = 0
        self.mesh.data = self.mesh.data[:,:4]

        # Create the portal node and add it to the portal scene
        self.black = bsk.Material(color=0)
        self.node = bsk.Node(mesh=self.mesh, position=position, scale=scale, shader=self.portal_shader)
        # self.outline = bsk.Node(position=position, scale=(scale[0] + .1, scale[1] + .1, scale[2] - .01,), material=self.black, shader=self.game_shader)
        self.portal_scene.add(self.node)


    def render_pass(self, camera: bsk.FreeCamera, render_target: bsk.Framebuffer, scene: bsk.Scene, shader: bsk.Shader):
        # Cannot render the view if there is no link
        if not self.link: return

        # Get the position of the camera relative to the link
        relative_position = camera.position - (self.link.node.position.x, self.link.node.position.y, self.link.node.position.z)

        # Save the camera and make view camera
        game_camera = scene.camera
        view_camera = bsk.FixedCamera(position=((self.node.position.x, self.node.position.y, self.node.position.z) + relative_position), rotation=camera.rotation)
        scene.camera = view_camera

        # Render depth
        scene.shader = shader
        scene.render(render_target)

        # Reset the camera and shader
        scene.shader = self.game_shader
        scene.camera = game_camera

    def depth_prepass(self, camera: bsk.FreeCamera):
        """
        
        """
        
        self.render_pass(camera, self.depth_fbo, self.portal_scene, self.depth_shader)

    def color_prepass(self, camera: bsk.FreeCamera):
        """
        
        """

        self.color_shader.write('portalID', glm.int32(self.index))
        self.render_pass(camera, self.color_fbo, self.game_scene, self.color_shader)

    def set_index(self, index: int) -> None:
        self.index = index
        self.mesh.data[:,3] = index
        self.node.chunk.node_update_callback(self.node)