import basilisk as bsk
from level import load_level
from portal_handler import PortalHandler
class Demo:
    def __init__(self):
        """
        Creates the basilisk context used by the demo
        """
        
        # Create Basilisk objects
        self.engine = bsk.Engine(title=None)
        self.scene = bsk.Scene(self.engine)

        # Load a sample level
        self.load_assets()
        load_level(self.scene)

        # Handler for portals
        self.portal_handler = PortalHandler(self)
        # Add a portal
        self.portal_handler.add(self.scene, open_position=(-15, 2, 10), end_position=(15, 2, 10), scale=(2, 4, .1))

        self.portal_handler.add(self.scene, open_position=(-15, 2, -10), end_position=(15, 2, -10), scale=(2, 4, .1))
    

    def load_assets(self):
        self.invisible_shader = bsk.Shader(self.engine, 'shaders/invisible.vert', 'shaders/invisible.frag')

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