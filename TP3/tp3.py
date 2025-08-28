import pyglet
import moderngl
import numpy as np
from pathlib import Path

class window(pyglet.window.Window):
    def __init__(self):
        super().__init__(640, 400, caption="TP3 - Mateos")
        self.ctx = moderngl.create_context()

        shader_dir = Path(__file__).parent/"shader"
        with open(shader_dir/"vertex.glsl") as f:
            vertex_shader = f.read()
        with open(shader_dir/"fragment.glsl") as f:   
            fragment_shader = f.read()  

        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        quad_points = [(0.5, 0.5), (-0.5, 0.5), (-0.5, -0.5), (0.5, -0.5)]
        vertices = []

        r,g,b = (1.0, 1.0, 1.0)

        for (px,py) in quad_points:
            vertices.extend([px, py, r, g, b])

        vertices_array = np.array(vertices, dtype='f4')
        vbo = self.ctx.buffer(vertices_array.tobytes())

        self.vao = self.ctx.vertex_array(self.prog,[(vbo,"2f 3f", "in_pos", "in_color")])
    
    def on_draw(self):
        self.clear()
        self.ctx.clear(0.0,0.0,0.0)
        self.vao.render(mode = moderngl.TRIANGLE_FAN)


window()
pyglet.app.run()
