import basilisk as bsk


def load(app, scene):
    cube = bsk.Node(scale=(2, .5, 2))

    scene.add(cube)