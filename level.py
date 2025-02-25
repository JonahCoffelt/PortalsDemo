import basilisk as bsk

def load_level(scene: bsk.Scene):

    brown = bsk.Material(color=(140, 108, 66))
    red = bsk.Material(color=(255, 75, 75))

    floor = bsk.Node(position=(0, -1, 0), scale=(15, 2, 15), material=brown)
    cube = bsk.Node(position=(2, 1, 5), scale=(1.5, 2, 1), material=red)

    scene.add(floor, cube)