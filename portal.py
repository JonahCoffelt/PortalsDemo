import basilisk as bsk
import glm


class Portal:
    def __init__(self, scene: bsk.Scene, shader: bsk.Shader, position: tuple[int]) -> None:
        """
        
        """
        
        self.scene = scene
        self.engine = scene.engine

        self.link: Portal = None

        self.fbo = bsk.Framebuffer(self.engine)

        self.node = bsk.Node(position=position, scale=(1, 2, .001), shader=shader)
        self.scene.add(self.node)

    def render_view(self, camera: bsk.FreeCamera, texture_index: int):
        """
        Renders the view of the portal for the link
        """

        # Cannot render the view if there is no link
        if not self.link: return

        # Get the position of the camera relative to the link
        relative_position = camera.position - (self.link.node.position.x, self.link.node.position.y, self.link.node.position.z)

        # Save the camera
        temp = self.scene.camera
        # Make a new camera
        view_cam = bsk.FixedCamera(position=((self.node.position.x, self.node.position.y, self.node.position.z) + relative_position), rotation=camera.rotation)
        self.scene.camera = view_cam
        
        # Render the scene from the correct view
        self.node.y -= 1000
        self.scene.render(self.fbo)
        self.node.y += 1000

        # Reset the camera
        self.scene.camera = temp
        
    @property
    def view_data(self): return self.fbo.texture.read()
