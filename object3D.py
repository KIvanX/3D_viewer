
from math import sin, cos, radians
import pygame


class Object3D:
    def __init__(self, obj_type, window, w, h):
        self.obj_type = obj_type
        self.window = window
        self.w, self.h = w, h
        self.vert, self.edj, self.faces = [], [], []
        if obj_type == 'Cube':
            self.vert += [(-2, -2, -2), (2, -2, -2), (2, 2, -2), (-2, 2, -2), (-2, -2, 2), (2, -2, 2), (2, 2, 2),
                          (-2, 2, 2)]
            self.edj += [(1, 2), (1, 4), (1, 5), (2, 3), (2, 6), (3, 4), (3, 7), (4, 8), (5, 6), (5, 8), (6, 7), (7, 8)]
            self.faces += [(1, 5, 6, 2, (200, 150, 150)), (4, 8, 7, 3, (150, 200, 150)), (1, 4, 3, 2, (150, 150, 200)),
                           (5, 8, 7, 6, (200, 200, 150)), (1, 5, 8, 4, (150, 200, 200)), (6, 7, 3, 2, (150, 150, 150))]
        elif obj_type == 'Cylinder':
            for i in range(0, 360, 15):
                x, y = cos(radians(i)) * 3, sin(radians(i)) * 3
                self.vert += [(x, y, -2), (x, y, 2)]
            self.edj += [(i, i + 1) for i in range(1, len(self.vert), 2)]
            self.edj += [(i, i + 2) for i in range(1, len(self.vert)-1)]
            self.edj += [(len(self.vert)-1, 1), (len(self.vert), 2)]
        elif obj_type == 'World_lines':
            for i in range(-9, 10):
                self.vert += [(i, -10, 0), (i, 10, 0), (-10, i, 0), (10, i, 0)]
                self.edj += [((i + 9)*4 + 1, (i + 9)*4 + 2), ((i + 9)*4 + 3, (i + 9)*4 + 4)]
        else:
            self.import_obj(f'models/{obj_type}.obj')

        self.offset = [0, 0, 0]
        self.ang = [0, 0, 0]
        self.pilot = [0, 0, 0]

    def import_obj(self, path):
        with open(path, 'r') as f:
            for line in f:
                line = line.replace('  ', ' ').strip()
                if line.startswith('v '):
                    x, y, z = line[2:].split()
                    self.vert.append((float(x), float(z), float(y)))
                if line.startswith('f '):
                    points = list(map(lambda e: int(e.split('/')[0]), line[2:].split(' ')))
                    for i in range(len(points)):
                        self.edj.append((points[i], points[(i+1) % len(points)]))
                    self.faces.append((*points, (150, 150, 150)))

    def show(self, angle, offset):
        proj = self.get_projection(angle, offset)

        # for e in self.edj:
        #     if proj[e[0] - 1] and proj[e[1] - 1]:
        #         pygame.draw.line(self.window, (0, 0, 0), proj[e[0] - 1][:2], proj[e[1] - 1][:2], 1)

        self.faces.sort(key=lambda face: sum([proj[p - 1][2] for p in face[:-1] if proj[p - 1]]) / len(face[:-1]))
        for f in self.faces:
            coord = [proj[ind - 1][:2] for ind in f[:-1] if proj[ind - 1]]
            if len(coord) > 2:
                pygame.draw.polygon(self.window, f[-1], coord)
                pygame.draw.polygon(self.window, (0, 0, 0), coord, 1)

        # if self.obj_type != 'World_lines':
        #     [self.window.set_at(p[:2], (0, 0, 0)) for p in proj if p]

    def get_projection(self, angle, offset):
        proj = []
        for x, y, z in self.vert:
            x1, y1, z1 = x - self.pilot[0], y - self.pilot[1], z - self.pilot[2]
            y = y1 * cos(radians(angle[0])) + z1 * sin(radians(angle[0]))
            z = z1 * cos(radians(angle[0])) - y1 * sin(radians(angle[0]))
            x = x1 * cos(radians(angle[1])) + z * sin(radians(angle[1]))
            z = z * cos(radians(angle[1])) - x1 * sin(radians(angle[1]))
            x_ = x * cos(radians(angle[2])) + y * sin(radians(angle[2]))
            y = y * cos(radians(angle[2])) - x * sin(radians(angle[2]))
            x, y, z = x_ + offset[0] + self.pilot[0], y + offset[1] + self.pilot[1], z + offset[2] + self.pilot[2]

            leng = 5 / x if x != 0 else 1000
            x_proj = int(self.w // 2 + y * leng * 100)
            y_proj = int(self.h // 2 - z * leng * 100)
            if -self.w <= x_proj <= self.w * 2 and -self.h <= y_proj <= self.h * 2 and leng > 0:
                proj.append((x_proj, y_proj, leng))
            else:
                proj.append(False)
        return proj

    def duplicate(self, n):
        for i in range(1, n):
            self.vert += [(v[0], v[1], v[2] + i * 6) for v in self.vert]

        for i in range(1, n):
            self.vert += [(v[0], v[1] + 6 * i, v[2]) for v in self.vert]

        for i in range(1, n):
            self.vert += [(v[0] + 6 * i, v[1], v[2]) for v in self.vert]

        new_edj = []
        for i in range(1, len(self.vert) // 8):
            new_edj += [(e[0] + 8 * i, e[1] + 8 * i) for e in self.edj]
        self.edj += new_edj

        new_faces = []
        for i in range(1, len(self.vert) // 8):
            new_faces += [(f[0] + 8 * i, f[1] + 8 * i, f[2] + 8 * i, f[3] + 8 * i, f[4]) for f in self.faces]
        self.faces += new_faces
