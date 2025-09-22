from graphics import Graphics
import glm
import moderngl
import numpy as np


class Scene:
    def __init__(self, ctx, camera):
        self.ctx = ctx
        self.objects = []
        self.graphics = {}
        self.camera = camera
        self.model = glm.mat4(1)
        self.view = camera.get_view_matrix()
        self.projection = camera.get_perspective_matrix()

    def add_object(self, obj, shader_program=None):
        self.objects.append(obj)
        self.graphics[obj.name] = Graphics(self.ctx, shader_program, obj.vertices, obj.indices)

    def render(self):
        self.ctx.enable(moderngl.DEPTH_TEST)

        view = self.camera.get_view_matrix()
        projection = self.camera.get_perspective_matrix()

        for obj in self.objects:
            model = obj.get_model_matrix()
            mvp = projection * view * model

            self.graphics[obj.name].program["Mvp"].write(np.array(mvp.to_list(), dtype='f4').tobytes())

            self.graphics[obj.name].vao.render()

    def on_resize(self, width, height):
        self.ctx.viewport = (0, 0, width, height)
        self.camera.projection = glm.perspective(glm.radians(45), width / height, 0.1, 100.0)
