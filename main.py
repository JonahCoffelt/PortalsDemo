import basilisk as bsk
from level import load_level
from player import Player
from portal_handler import PortalHandler

class Demo:
    def __init__(self):
        """
        Creates the basilisk context used by the demo
        """
        # Create Basilisk objects
        self.engine = bsk.Engine(title=None)
        self.scene = bsk.Scene(self.engine)
        self.player = Player(self.scene.camera)

        # Load a sample level
        self.load_assets()
        load_level(self.scene)

        # Handler for portals
        self.portal_handler = PortalHandler(self)

        self.portal_handler.add(self.scene, open_position=(-15, 2, 10), end_position=(15, 2, 10), scale=(2, 4, .1))

    def load_assets(self):
        self.invisible_shader = bsk.Shader(self.engine, 'shaders/invisible.vert', 'shaders/invisible.frag')

    def update(self):
        self.scene.update(render=False)
        self.portal_handler.update(self.scene.camera)

    def start(self):
        """
        Starts the demo
        """
        
        while self.engine.running:
            self.update()
            print(self.player.radius)
            self.scene.render()
            self.portal_handler.render()

            self.engine.update()


demo = Demo()
demo.start()