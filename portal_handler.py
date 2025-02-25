import basilisk as bsk
from portal import Portal
import numpy as np
import moderngl as mgl


class PortalHandler:
    texture_array: mgl.TextureArray=None
    def __init__(self, engine: bsk.Engine) -> None:
        """
        Handles all the rendering and interactions of portals
        """
        
        # Parent Basilisk references
        self.engine = engine

        # Shader for the portal nodes
        self.portal_shader = bsk.Shader(engine, "shaders/portal.vert", "shaders/portal.frag")

        # List containing all portals in the game
        self.portals = []

    def add(self, scene: bsk.Scene, open_position: tuple[int], end_position: tuple[int]):
        """
        Add a new portal to the given scene
        """

        # Create the two portal ends
        open_portal = Portal(scene, self.portal_shader, open_position)
        end_portal  = Portal(scene, self.portal_shader, end_position)

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
        array_data = []
        # Loop through portals and render the view according to the given camera
        # Get the data of the view to write to the GPU
        for i, pair in enumerate(self.portals):
            pair[0].render_view(camera, i * 2)
            pair[1].render_view(camera, i * 2 + 1)

            array_data.append(pair[0].view_data)
            array_data.append(pair[1].view_data)


        # Condense array data
        dim = (*self.engine.win_size, len(array_data))
        array_data = np.array(array_data)

        # Build new array
        if not self.texture_array:
            self.texture_array = self.engine.ctx.texture_array(size=dim, components=4, data=array_data)
            self.texture_array.build_mipmaps()
            self.texture_array.anisotropy = 32.0
        # Write to existing array
        else:
            self.texture_array.write(array_data)
