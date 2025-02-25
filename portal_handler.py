import basilisk as bsk
from portal import Portal
import numpy as np
import moderngl as mgl


class PortalHandler:
    portals: list[list[Portal]]
    texture_array: mgl.TextureArray=None
    """"""
    def __init__(self, game: ...) -> None:
        """
        Handles all the rendering and interactions of portals
        """
        
        # Parent Basilisk references
        self.game = game
        self.engine = game.engine

        # Shader for the portal nodes
        self.portal_shader = bsk.Shader(self.engine, "shaders/portal.vert", "shaders/portal.frag")

        # List containing all portals in the game
        self.portals = []

    def add(self, scene: bsk.Scene, open_position: tuple[int], end_position: tuple[int], scale: tuple[int]=(1, 1, 1)):
        """
        Add a new portal to the given scene
        """

        # Create the two portal ends
        open_portal = Portal(self, scene, self.portal_shader, open_position, scale)
        end_portal  = Portal(self, scene, self.portal_shader, end_position, scale)

        # Link each end of the portal to the other
        open_portal.link = end_portal
        end_portal.link = open_portal

        # Save the portal ends as a pair
        self.portals.append([open_portal, end_portal])

    def update(self, camera: bsk.FreeCamera) -> None:
        """
        Updates all portals accordiing to the given primary camera
        """

        # Do not attempt to get portal views if there are no portals
        if not self.portals: return

        # Empty array for all portal view data
        array_data_texture = []
        array_data_depth   = []

        # Loop through portals and render the view according to the given camera
        for i, (portal_1, portal_2) in enumerate(self.portals):
            portal_1.render_view(camera, i * 2)
            portal_2.render_view(camera, i * 2 + 1)

            array_data_texture.append(portal_1.fbo.texture.read())
            array_data_texture.append(portal_2.fbo.texture.read())

            array_data_depth.append(portal_1.fbo.depth.read())
            array_data_depth.append(portal_2.fbo.depth.read())

        # Condense array data
        dim = (*self.engine.win_size, len(array_data_texture))
        array_data_texture = np.array(array_data_texture)
        array_data_depth = np.array(array_data_depth)

        # Build new array
        if not self.texture_array:
            # Color attachment array
            self.texture_array = self.engine.ctx.texture_array(size=dim, components=4, data=array_data_texture)
            self.texture_array.build_mipmaps()
            self.texture_array.anisotropy = 32.0
            # Depth attachment array
            self.depth_array = self.engine.ctx.texture_array(size=dim, components=4, data=array_data_depth)

            # Bind to Shader
            self.portal_shader.program['portalTextures'] = 0
            self.texture_array.use(location=0)
            # self.portal_shader.program['portalDepths'] = 1
            # self.depth_array.use(location=1)

        # Write to existing array
        else:
            self.texture_array.write(array_data_texture)
            self.depth_array.write(array_data_depth)
