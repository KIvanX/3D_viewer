from math import sin, cos, radians
import pygame
import object3D


def events():
    global show, glob_angle, glob_offset, edit_angle, edit_offset
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            show = False

        if event.type == pygame.MOUSEWHEEL:
            glob_offset[0] -= event.y * max(10, glob_offset[0]) * 0.1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                edit_angle = {'x': x, 'y': y, 'angle': glob_angle}
            elif event.button == 2:
                edit_offset = {'x': x, 'y': y, 'offset': glob_offset}

        if event.type == pygame.MOUSEBUTTONUP:
            edit_angle = False
            edit_offset = False

    if edit_angle:
        glob_angle = [edit_angle['angle'][0] - (y - edit_angle['y']) * sin(radians(glob_angle[2])),
                      edit_angle['angle'][1] - (y - edit_angle['y']) * cos(radians(glob_angle[2])),
                      edit_angle['angle'][2] + (x - edit_angle['x']) ]

    if edit_offset:
        glob_offset = [edit_offset['offset'][0],
                       edit_offset['offset'][1] + (x - edit_offset['x']) * glob_offset[0] / 500,
                       edit_offset['offset'][2] - (y - edit_offset['y']) * glob_offset[0] / 500]


w, h = 1400, 750
window = pygame.display.set_mode((w, h))
pygame.display.set_caption('3D_viewer')
glob_angle, glob_offset = [0, 0, 45], [300, 0, 0]

objects = [object3D.Object3D('tank', window, w, h)]

show, edit_angle, edit_offset = True, False, False
while show:
    window.fill((200, 200, 200))

    for obj in objects:
        obj.show(glob_angle, glob_offset)

    pygame.display.flip()

    events()
