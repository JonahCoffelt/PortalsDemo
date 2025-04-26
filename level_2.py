import basilisk as bsk


def load(app, scene):
    shader = bsk.Shader(app.engine)
    cube1 = bsk.Node(scale=(1, 2, 2))
    cube2 = bsk.Node(position=(4, 2, 2), material=app.mtl)

    scene.add(cube1, cube2)