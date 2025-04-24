import basilisk as bsk


def load(app, scene):
    mtl = bsk.Material(emissive_color=(500, 500, 100))
    cube = bsk.Node(scale=(2, .5, 2), material=mtl)

    scene.add(cube)