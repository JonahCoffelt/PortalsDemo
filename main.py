import basilisk as bsk
from level import load_level
from portal_handler import PortalHandler
class Demo:
    def __init__(self):
        """
        Creates the basilisk context used by the demo
        """
        
        # Create Basilisk objects
        self.engine = bsk.Engine()
        self.scene = bsk.Scene(self.engine)

        # Load a sample level
        load_level(self.scene)

        # Handler for portals
        self.portal_handler = PortalHandler(self.engine)
        # Add a portal
        self.portal_handler.add(self.scene, open_position=(-3, 4, 5), end_position=(5, 6, -3))

        print(self.portal_handler.portals)

    def update(self):
        self.portal_handler.update(self.scene.camera)

    def start(self):
        """
        Starts the demo
        """
        
        while self.engine.running:
            self.scene.update(render=False)
            
            self.update()
            if self.engine.keys[bsk.pg.K_1]:
                self.portal_handler.portals[0][0].fbo.render()
            elif self.engine.keys[bsk.pg.K_2]:
                self.portal_handler.portals[0][1].fbo.render()
            else:
                self.scene.render()

            self.engine.update()


demo = Demo()
demo.start()