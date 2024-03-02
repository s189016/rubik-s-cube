from vispy import app, gloo
import numpy as np
from vispy.util.transforms import rotate, translate, perspective


class Kostka(app.Canvas):
    def __init__(self):
        super().__init__(title="Kostka Rubika", size=(800, 800))
        gloo.set_state(depth_test=True)

        self.vertex_shader = self.load_shader("vertex_shader.glsl")
        self.fragment_shader = self.load_shader("fragment_shader.glsl")

        self.shapes = []
        self.translations = []
        self.rotations = []
        for i in range(29):
            self.rotations.append(np.eye(4, dtype=np.float32))
        self.history = []
        self.i = 0
        self.cofanie = 0
        self.key_block = False
        self.block = True
        self.obrx = 0
        self.obry = 0
        self.rot = []
        for i in range(26):
            self.rot.append(0)
        self.obrW = np.eye(4, dtype=np.float32)
        self.gen_scene()
        self.time = 0
        self.timer = app.Timer(1 / 60, connect=self.on_timer)
        self.timer.start()
        self.view = translate((0, 0, -8))
        self.projection = perspective(80, 1, 2, 10)
        self.model = np.eye(4, dtype=np.float32)
        self.cube = []
        for i in range(26):
            self.cube.append(i)

        self.rotate_start = False
        self.last_x = 0
        self.last_y = 0
        self.last_z = 0
        self.rotate_z = False
        self.hist_check = False
        self.hist_i = 0
        self.good_time = 0.0

        self.show_axis = True

    def gen_scene(self):
        # model kostki

        # ścianka 0
        self.shapes.append(self.gen_cube(0))
        self.translations.append((0, 0, 1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((0, 1.05, 1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((0, -1.05, 1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((1.05, 0, 1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((1.05, 1.05, 1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((1.05, -1.05, 1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((-1.05, 0, 1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((-1.05, 1.05, 1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((-1.05, -1.05, 1.05))

        # ścianka 1
        self.shapes.append(self.gen_cube(0))
        self.translations.append((0, 0, -1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((0, 1.05, -1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((0, -1.05, -1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((1.05, 0, -1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((1.05, 1.05, -1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((1.05, -1.05, -1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((-1.05, 0, -1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((-1.05, 1.05, -1.05))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((-1.05, -1.05, -1.05))

        # ścianka 2
        self.shapes.append(self.gen_cube(0))
        self.translations.append((0, 1.05, 0))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((0, -1.05, 0))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((1.05, 0, 0))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((1.05, 1.05, 0))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((1.05, -1.05, 0))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((-1.05, 0, 0))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((-1.05, 1.05, 0))
        self.shapes.append(self.gen_cube(0))
        self.translations.append((-1.05, -1.05, 0))
# osie
        self.shapes.append(self.gen_cube(1))
        self.translations.append((3, 0, 0))
        self.shapes.append(self.gen_cube(2))
        self.translations.append((0, 3, 0))
        self.shapes.append(self.gen_cube(3))
        self.translations.append((0, 0, 3))

    def gen_cube(self, axis):
        shape = dict()
        shape['program'] = gloo.Program(self.vertex_shader, self.fragment_shader, 24)

        # Generowanie płaszczyzn
        if axis == 0:
            colors = np.array([
                # Ścianka 1 (przednia)
                [1, 0, 0, 0],  # Czerwony
                [1, 0, 0, 0],  # Czerwony
                [1, 0, 0, 0],  # Czerwony
                [1, 0, 0, 0],  # Czerwony
                # Ścianka 2 (tylna)
                [0, 1, 0, 0],  # Zielony
                [0, 1, 0, 0],  # Zielony
                [0, 1, 0, 0],  # Zielony
                [0, 1, 0, 0],  # Zielony
                # Ścianka 3 (lewa)
                [0, 0, 1, 0],  # Niebieski
                [0, 0, 1, 0],  # Niebieski
                [0, 0, 1, 0],  # Niebieski
                [0, 0, 1, 0],  # Niebieski
                # Ścianka 4 (prawa)
                [1, 1, 0, 0],  # Żółty
                [1, 1, 0, 0],  # Żółty
                [1, 1, 0, 0],  # Żółty
                [1, 1, 0, 0],  # Żółty
                # Ścianka 5 (górna)
                [1, 0, 1, 0],  # Magenta
                [1, 0, 1, 0],  # Magenta
                [1, 0, 1, 0],  # Magenta
                [1, 0, 1, 0],  # Magenta
                # Ścianka 6 (dolna)
                [0, 1, 1, 0],  # Cyjan
                [0, 1, 1, 0],  # Cyjan
                [0, 1, 1, 0],  # Cyjan
                [0, 1, 1, 0]  # Cyjan
            ], dtype=np.float32)

        elif axis == 1:
            colors = np.array([
                # Ścianka 1 (przednia)
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                # Ścianka 2 (tylna)
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                # Ścianka 3 (lewa)
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                # Ścianka 4 (prawa)
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                # Ścianka 5 (górna)
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                # Ścianka 6 (dolna)
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
                [1, 0, 0, 0.9],  # Czerwony
            ], dtype=np.float32)
        if axis == 2:
            colors = np.array([
                # Ścianka 1 (przednia)
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                # Ścianka 2 (tylna)
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                # Ścianka 3 (lewa)
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                # Ścianka 4 (prawa)
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                # Ścianka 5 (górna)
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                # Ścianka 6 (dolna)
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
                [0, 1, 0, 0.5],  # Zielony
            ], dtype=np.float32)
        if axis == 3:
            colors = np.array([
                # Ścianka 1 (przednia)
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                # Ścianka 2 (tylna)
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                # Ścianka 3 (lewa)
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                # Ścianka 4 (prawa)
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                # Ścianka 5 (górna)
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                # Ścianka 6 (dolna)
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
                [0, 0, 1, 0.5],  # Niebieski
            ], dtype=np.float32)

        positions = np.array([
            [-0.5, -0.5, -0.5],  # Wierzchołek 0
            [0.5, -0.5, -0.5],  # Wierzchołek 1
            [0.5, 0.5, -0.5],  # Wierzchołek 2
            [-0.5, 0.5, -0.5],  # Wierzchołek 3

            [-0.5, -0.5, 0.5],  # Wierzchołek 4
            [0.5, -0.5, 0.5],  # Wierzchołek 5
            [0.5, 0.5, 0.5],  # Wierzchołek 6
            [-0.5, 0.5, 0.5],  # Wierzchołek 7

            [-0.5, 0.5, 0.5],  # Wierzchołek 8
            [-0.5, -0.5, 0.5],  # Wierzchołek 9
            [-0.5, -0.5, -0.5],  # Wierzchołek 10
            [-0.5, 0.5, -0.5],  # Wierzchołek 11

            [0.5, 0.5, 0.5],  # Wierzchołek 8
            [0.5, -0.5, 0.5],  # Wierzchołek 9
            [0.5, -0.5, -0.5],  # Wierzchołek 10
            [0.5, 0.5, -0.5],  # Wierzchołek 11

            [0.5, -0.5, 0.5],  # Wierzchołek 16
            [0.5, -0.5, -0.5],  # Wierzchołek 17
            [-0.5, -0.5, -0.5],  # Wierzchołek 18
            [-0.5, -0.5, 0.5],  # Wierzchołek 19

            [0.5, 0.5, 0.5],  # Wierzchołek 16
            [0.5, 0.5, -0.5],  # Wierzchołek 17
            [-0.5, 0.5, -0.5],  # Wierzchołek 18
            [-0.5, 0.5, 0.5],  # Wierzchołek 19
        ], dtype=np.float32)

        if axis != 0:
            positions *= 0.2
        # Macierz przechowująca indeksy wierzchołków, które tworzą ścianki sześcianu
        indices = np.array([
            # Ścianka 1 (przednia)
            [0, 1, 2],
            [2, 3, 0],
            # Ścianka 2 (tylna)
            [4, 5, 6],
            [6, 7, 4],
            # Ścianka 3 (lewa)
            [8, 9, 10],
            [10, 11, 8],
            # Ścianka 4 (prawa)
            [12, 13, 14],
            [14, 15, 12],
            # Ścianka 5 (górna)
            [16, 17, 18],
            [18, 19, 16],
            # Ścianka 6 (dolna)
            [20, 21, 22],
            [22, 23, 20]
        ], dtype=np.uint32)

        shape['program']['pos'] = positions
        shape['program']['color'] = colors
        shape['triangle_indices'] = gloo.IndexBuffer(indices)

        return shape

    @staticmethod
    def load_shader(shader_path):
        with open(shader_path, "r") as file:
            shader = file.read()
        return shader

    def on_draw(self, event):
        gloo.clear()
        self.i = 0
        for shape, trans in zip(self.shapes, self.translations):
            if self.i == self.cube[0]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[0], (0, 0, 1)).dot(rotate(self.rot[6], (1, 0, 0))).dot(rotate(self.rot[7], (0, 1, 0))))
            if self.i == self.cube[1]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[0], (0, 0, 1)).dot(rotate(self.rot[2], (0, 1, 0))).dot(rotate(self.rot[6], (1, 0, 0))))
            if self.i == self.cube[2]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[0], (0, 0, 1)).dot(rotate(self.rot[3], (0, 1, 0))).dot(rotate(self.rot[6], (1, 0, 0))))
            if self.i == self.cube[3]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[0], (0, 0, 1)).dot(rotate(self.rot[4], (1, 0, 0))).dot(rotate(self.rot[7], (0, 1, 0))))
            if self.i == self.cube[4]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[0], (0, 0, 1)).dot(rotate(self.rot[2], (0, 1, 0))).dot(rotate(self.rot[4], (1, 0, 0))))
            if self.i == self.cube[5]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[0], (0, 0, 1)).dot(rotate(self.rot[3], (0, 1, 0))).dot(rotate(self.rot[4], (1, 0, 0))))
            if self.i == self.cube[6]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[0], (0, 0, 1)).dot(rotate(self.rot[5], (1, 0, 0))).dot(rotate(self.rot[7], (0, 1, 0))))
            if self.i == self.cube[7]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[0], (0, 0, 1)).dot(rotate(self.rot[2], (0, 1, 0))).dot(rotate(self.rot[5], (1, 0, 0))))
            if self.i == self.cube[8]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[0], (0, 0, 1)).dot(rotate(self.rot[3], (0, 1, 0))).dot(rotate(self.rot[5], (1, 0, 0))))
            if self.i == self.cube[9]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[1], (0, 0, 1)).dot(rotate(self.rot[6], (1, 0, 0))).dot(rotate(self.rot[7], (0, 1, 0))))
            if self.i == self.cube[10]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[1], (0, 0, 1)).dot(rotate(self.rot[2], (0, 1, 0))).dot(rotate(self.rot[6], (1, 0, 0))))
            if self.i == self.cube[11]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[1], (0, 0, 1)).dot(rotate(self.rot[3], (0, 1, 0))).dot(rotate(self.rot[6], (1, 0, 0))))
            if self.i == self.cube[12]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[1], (0, 0, 1)).dot(rotate(self.rot[4], (1, 0, 0))).dot(rotate(self.rot[7], (0, 1, 0))))
            if self.i == self.cube[13]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[1], (0, 0, 1)).dot(rotate(self.rot[2], (0, 1, 0))).dot(rotate(self.rot[4], (1, 0, 0))))
            if self.i == self.cube[14]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[1], (0, 0, 1)).dot(rotate(self.rot[3], (0, 1, 0))).dot(rotate(self.rot[4], (1, 0, 0))))
            if self.i == self.cube[15]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[1], (0, 0, 1)).dot(rotate(self.rot[5], (1, 0, 0))).dot(rotate(self.rot[7], (0, 1, 0))))
            if self.i == self.cube[16]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[1], (0, 0, 1)).dot(rotate(self.rot[2], (0, 1, 0))).dot(rotate(self.rot[5], (1, 0, 0))))
            if self.i == self.cube[17]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[1], (0, 0, 1)).dot(rotate(self.rot[3], (0, 1, 0))).dot(rotate(self.rot[5], (1, 0, 0))))
            if self.i == self.cube[18]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[8], (0, 0, 1)).dot(rotate(self.rot[2], (0, 1, 0))).dot(rotate(self.rot[6], (1, 0, 0))))
            if self.i == self.cube[19]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[8], (0, 0, 1)).dot(rotate(self.rot[2], (0, 1, 0))).dot(rotate(self.rot[6], (1, 0, 0))))
            if self.i == self.cube[20]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[4], (1, 0, 0)).dot(rotate(self.rot[7], (0, 1, 0))).dot(rotate(self.rot[8], (0, 0, 1))))
            if self.i == self.cube[21]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[4], (1, 0, 0)).dot(rotate(self.rot[2], (0, 1, 0))).dot(rotate(self.rot[8], (0, 0, 1))))
            if self.i == self.cube[22]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[3], (0, 1, 0)).dot(rotate(self.rot[4], (1, 0, 0))).dot(rotate(self.rot[8], (0, 0, 1))))
            if self.i == self.cube[23]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[5], (1, 0, 0)).dot(rotate(self.rot[7], (0, 1, 0))).dot(rotate(self.rot[8], (0, 0, 1))))
            if self.i == self.cube[24]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[5], (1, 0, 0)).dot(rotate(self.rot[8], (0, 0, 1))).dot(rotate(self.rot[2], (0, 1, 0))))
            if self.i == self.cube[25]:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot[5], (1, 0, 0)).dot(rotate(self.rot[8], (0, 0, 1))).dot(rotate(self.rot[3], (0, 1, 0))))
            self.draw_shape(shape, trans)
            self.i += 1
        if self.rot[0] == 90:
            a = self.cube[1]
            self.cube[1] = self.cube[3]
            b = self.cube[2]
            self.cube[2] = self.cube[6]
            self.cube[3] = b
            c = self.cube[4]
            self.cube[4] = self.cube[5]
            self.cube[5] = self.cube[8]
            self.cube[6] = a
            d = self.cube[7]
            self.cube[7] = c
            self.cube[8] = d

        if self.rot[1] == 90:
            a = self.cube[10]
            self.cube[10] = self.cube[12]
            self.cube[12] = self.cube[11]
            b = self.cube[13]
            self.cube[13] = self.cube[14]
            self.cube[14] = self.cube[17]
            c = self.cube[15]
            self.cube[15] = a
            d = self.cube[16]
            self.cube[16] = b
            self.cube[17] = d
            self.cube[11] = c

        if self.rot[2] == 90:
            a = self.cube[7]
            self.cube[7] = self.cube[16]
            b = self.cube[1]
            self.cube[1] = self.cube[24]
            c = self.cube[4]
            self.cube[4] = a
            self.cube[24] = self.cube[10]
            self.cube[10] = self.cube[21]
            self.cube[21] = b
            self.cube[16] = self.cube[13]
            self.cube[13] = c

        if self.rot[3] == 90:
            a = self.cube[8]
            self.cube[8] = self.cube[17]
            b = self.cube[2]
            self.cube[2 ]= self.cube[25]
            d = self.cube[5]
            self.cube[5] = a
            self.cube[25]= self.cube[11]
            c = self.cube[22]
            self.cube[22] = b
            self.cube[17] = self.cube[14]
            self.cube[11] = c
            self.cube[14] = d

        if self.rot[4] == 90:
            a = self.cube[4]
            self.cube[4] = self.cube[13]
            b = self.cube[21]
            self.cube[21 ]= self.cube[12]
            self.cube[13] = self.cube[14]
            c = self.cube[3]
            self.cube[3] = b
            self.cube[12] = self.cube[22]
            d = self.cube[5]
            self.cube[5] = a
            self.cube[22] = c
            self.cube[14] = d

        if self.rot[5] == 90:
            a = self.cube[7]
            self.cube[7] = self.cube[16]
            b = self.cube[24]
            self.cube[24] = self.cube[15]
            self.cube[16 ]= self.cube[17]
            d = self.cube[6]
            self.cube[6] = b
            self.cube[15] = self.cube[25]
            c = self.cube[8]
            self.cube[8] = a
            self.cube[25] = d
            self.cube[17] = c

        if self.rot[6] == 90:
            a = self.cube[1]
            self.cube[1] = self.cube[10]
            b = self.cube[18]
            self.cube[18] = self.cube[9]
            self.cube[10] = self.cube[11]
            c = self.cube[0]
            self.cube[0] = b
            self.cube[9] = self.cube[19]
            b = self.cube[2]
            self.cube[2] = a
            self.cube[19] = c
            self.cube[11] = b

        if self.rot[7] == 90:
            a = self.cube[6]
            self.cube[6] = self.cube[15]
            b = self.cube[00]
            self.cube[00] = self.cube[23]
            d = self.cube[3]
            self.cube[3] = a
            self.cube[23] = self.cube[9]
            e = self.cube[20]
            self.cube[20] = b
            self.cube[15] = self.cube[12]
            self.cube[9] = e
            self.cube[12] = d

        if self.rot[8] == 90:
            a = self.cube[24]
            self.cube[24] = self.cube[21]
            b = self.cube[18]
            self.cube[18] = self.cube[20]
            self.cube[21] = self.cube[22]
            c = self.cube[23]
            self.cube[23] = b
            self.cube[20] = self.cube[19]
            d = self.cube[25]
            self.cube[25] = a
            self.cube[19] = c
            self.cube[22] = d
        if self.cofanie != 0:
            self.cofanie += 1
            if self.cofanie == 3:
                self.cofanie = 0
        else:
            for i in range(len(self.rot)):
                self.rot[i] = 0
            if not self.hist_check:
                self.key_block = False
        if self.hist_check and self.hist_i + 1 < len(self.history) and 1 < self.good_time < 1.015:
            self.hist_i += 1
            self.good_time = 0
            for i in range(len(self.rot)):
                if self.history[self.hist_i] == i:
                    self.rot[i] = 90
        if self.hist_i + 1 == len(self.history):
            self.hist_check = False
            self.hist_i = 0

    def draw_shape(self, shape, translation=(0, 0, 0)):
        shape['program']['view'] = self.view
        shape['program']['projection'] = self.projection
        shape['program']['obr'] = self.obrW
        shape['program']['model'] = self.model.dot(translate(translation).dot(self.rotations[self.i]))
        shape['program'].draw('triangles', shape['triangle_indices'], 36)

    def on_mouse_press(self, event):
        if event.button == 1:  # Lewy przycisk myszy
            self.rotate_start = True
            self.last_x = event.pos[0]
            self.last_y = event.pos[1]
        if event.button == 2 and not self.rotate_start:
            self.rotate_z = True
            self.last_z = event.pos[1]

    def on_mouse_release(self, event):
        if event.button == 1:  # Lewy przycisk myszy
            self.rotate_start = False
        if event.button == 2 and not self.rotate_start:
            self.rotate_z = False

    def on_mouse_move(self, event):
        if self.rotate_start:
            dx = (event.pos[0] - self.last_x) / 6
            dy = (event.pos[1] - self.last_y) / 6
            self.last_x = event.pos[0]
            self.last_y = event.pos[1]
            rotation = rotate(dx, (0, 1, 0)).dot(rotate(dy, (1, 0, 0)))
            self.obrW = rotation.dot(self.obrW)
        if self.rotate_z:
            dz = (event.pos[1] - self.last_z) / 6
            self.last_z = event.pos[1]
            rotation = rotate(-dz, (0, 0, 1))
            self.obrW = rotation.dot(self.obrW)

    def on_key_press(self, event):
        if event.key == "S" and not self.key_block:
            self.key_block = True
            self.obrx -= 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))
        if event.key == "D" and not self.key_block:
            self.key_block = True
            self.obry += 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))
        if event.key == "W" and not self.key_block:
            self.key_block = True
            self.obrx += 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))
        if event.key == "A" and not self.key_block:
            self.key_block = True
            self.obry -= 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))

        if event.key == "Z" and not self.key_block:
            self.key_block = True
            self.history.append(0)
            self.rot[0] += 90
        if event.key == "X" and not self.key_block:
            self.key_block = True
            self.history.append(1)
            self.rot[1] += 90
        if event.key == "C" and not self.key_block:
            self.key_block = True
            self.history.append(2)
            self.rot[2] += 90
        if event.key == "V" and not self.key_block:
            self.key_block = True
            self.history.append(3)
            self.rot[3] += 90
        if event.key == "B" and not self.key_block:
            self.key_block = True
            self.history.append(4)
            self.rot[4] += 90
        if event.key == "N" and not self.key_block:
            self.key_block = True
            self.history.append(5)
            self.rot[5] += 90
        if event.key == "J" and not self.key_block:
            self.key_block = True
            self.history.append(6)
            self.rot[6] += 90
        if event.key == "K" and not self.key_block:
            self.key_block = True
            self.history.append(7)
            self.rot[7] += 90
        if event.key == "L" and not self.key_block:
            self.key_block = True
            self.history.append(8)
            self.rot[8] += 90
        if (event.key == "P" and not self.key_block and len(self.history) != 0) or (
                self.cofanie != 0 and not self.key_block and len(self.history)):
            self.key_block = True
            for i in range(len(self.rot)):
                if self.history[len(self.history) - 1] == i:
                    self.rot[i] = 90
            self.history.pop()
            self.cofanie += 1
        if event.key == "Q":
            if not self.block:
                self.block = True
            else:
                self.block = False
        if event.key == "R" and not self.key_block and self.hist_i < len(self.history):
            self.key_block = True
            self.hist_check = True
            self.good_time = 0
            for i in range(len(self.cube)):
                self.cube[i] = i
            self.rotations = []
            for i in range(26):
                self.rotations.append(np.eye(4, dtype=np.float32))
            for i in range(len(self.rot)):
                if self.history[self.hist_i] == i:
                    self.rot[i] = 90

    def on_timer(self, event):
        self.good_time += (1/60)
        if not self.block:
            self.time += 1 / 60
            self.view = rotate(self.time * 180 / np.pi, (0, 1, 0)).dot(translate((0, 0, -8)))
        self.show()


kostka = Kostka()
app.run()
