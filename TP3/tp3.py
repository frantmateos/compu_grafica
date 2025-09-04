import time
import pyglet
import moderngl
import numpy as np
from pathlib import Path
import time

class window(pyglet.window.Window):
    def __init__(self):
        self.mouse_pos = (0.0, 0.0)
        self.mode = 0
        super().__init__(1289, 720, caption="TP3 - Mateos")
        self.ctx = moderngl.create_context()

        shader_dir = Path(__file__).parent/"shader"
        with open(shader_dir/"vertex.glsl") as f:
            vertex_shader = f.read()
        with open(shader_dir/"fragment.glsl") as f:   
            fragment_shader = f.read()  

        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        quad_points = [(1.0, 1.0), (-1.0, 1.0), (-1.0, -1.0), (1.0, -1.0)]
        vertices = []
        for (px,py) in quad_points:
            vertices.extend([px, py, 1.0, 1.0, 1.0])

        vertices_array = np.array(vertices, dtype='f4')
        vbo = self.ctx.buffer(vertices_array.tobytes())
        self.vao = self.ctx.vertex_array(self.prog, [(vbo,"2f 3f", "in_pos", "in_color")])
        self.start = time.time()

    def on_draw(self):
        self.clear()
        self.ctx.clear(0.0, 0.0, 0.0)

        self.prog["u_time"].value = time.time() - self.start
        self.prog["u_resolution"].value = (self.width, self.height)

        self.prog["u_mouse"].value = self.mouse_pos
        self.prog["u_mode"].value = self.mode

        self.vao.render(mode=moderngl.TRIANGLE_FAN)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = (x / self.width, y / self.height)

    def on_key_press(self, symbol, modifiers):
        # cambiar modo con teclas 1,2,3
        if symbol == pyglet.window.key._1:
            self.mode = 0
        elif symbol == pyglet.window.key._2:
            self.mode = 1
        elif symbol == pyglet.window.key._3:
            self.mode = 2


if __name__ == "__main__":
    window()
    pyglet.app.run()
