import basilisk as bsk

def load_level(scene: bsk.Scene):

    brown = bsk.Material(color=(140, 108, 66))
    red = bsk.Material(color=(255, 75, 75))
    green = bsk.Material(color=(75, 255, 75))

    floor1 = bsk.Node(position=(-20, -1, 0), scale=(15, 2, 15), material=brown)
    floor2 = bsk.Node(position=(20, -1, 0), scale=(15, 2, 15), material=green)

    cube1 = bsk.Node(position=(2, 1, 5), scale=(1.5, 2, 1), material=red)
    cube2 = bsk.Node(position=(-15, 2, 5), scale=(1.5, 2, 1), material=red)

    scene.add(floor1, floor2, cube1, cube2)