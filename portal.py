import basilisk as bsk
import numpy as np
import glm

class Portal:
    def __init__(self, portal_handler: ..., scene: bsk.Scene, shader: bsk.Shader, position: tuple[int], scale: tuple[int]) -> None:
        """
        
        """
        
        self.portal_handler = portal_handler
        self.scene = scene
        self.engine = scene.engine

        self.link: Portal = None

        self.fbo = bsk.Framebuffer(self.engine)
        self.black = bsk.Material(color=0)
        self.mesh = bsk.Mesh('assets/cube.obj', custom_format=True)
        self.mesh.data[:,3] = 0
        self.mesh.data = self.mesh.data[:,:4]

        self.node = bsk.Node(mesh=self.mesh, position=position, scale=(scale[0], scale[1], scale[2]), shader=shader)
        self.outline = bsk.Node(position=position, scale=(scale[0] + .1, scale[1] + .1, scale[2] - .01,), material=self.black)
        self.scene.add(self.node, self.outline)

    def render_view(self, camera: bsk.FreeCamera, texture_index: int):
        """
        Renders the view of the portal for the link
        """

        # Cannot render the view if there is no link
        if not self.link: return
        self.link.mesh.data[:,3] = texture_index

        # Get the position of the camera relative to the link
        relative_position = camera.position - (self.link.node.position.x, self.link.node.position.y, self.link.node.position.z)

        # Save the camera
        temp = self.scene.camera
        # Make a new camera 
        view_cam = bsk.FixedCamera(position=((self.node.position.x, self.node.position.y, self.node.position.z) + relative_position), rotation=camera.rotation)
        self.scene.camera = view_cam

        # Render the scene from the correct view
        self.node.y -= 1000
        self.outline.y -= 1000
        self.scene.render(self.fbo)
        self.node.y += 1000
        self.outline.y += 1000

        # Reset the camera
        self.scene.camera = temp
        
    @property
    def view_data(self): return self.fbo.texture.read()
