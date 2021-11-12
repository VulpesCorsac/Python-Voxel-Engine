import math

import numpy as np
import pygame as pg
from numba import njit


height_map_img = pg.image.load('img/height_map_2.jpg')
height_map = pg.surfarray.array3d(height_map_img)

color_map_img = pg.image.load('img/color_map_2.jpg')
color_map = pg.surfarray.array3d(color_map_img)

map_height = len(height_map[0])
map_width = len(height_map)


@njit(fastmath=True)
def ray_casting(screen_array,
                player_position, player_angle, player_height, player_pitch,
                screen_width, screen_height,
                delta_angle, ray_distance, horizontal_field_of_view, scale_height):

    screen_array[:] = np.array([0, 0, 0])
    y_buffer = np.full(screen_width, screen_height)

    ray_angle = player_angle - horizontal_field_of_view
    for num_ray in range(screen_width):
        first_contact = False
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        for depth in range(1, ray_distance):
            x = int(player_position[0] + depth * cos_a)
            if 0 < x < map_width:
                y = int(player_position[1] + depth * sin_a)
                if 0 < y < map_height:

                    # remove fish eye and get height on screen
                    depth *= math.cos(player_angle - ray_angle)
                    height_on_screen = int((player_height - height_map[x, y][0]) / depth * scale_height + player_pitch)

                    # remove unnecessary drawing
                    if not first_contact:
                        y_buffer[num_ray] = min(height_on_screen, screen_height)
                        first_contact = True

                    # remove mirror bug
                    if height_on_screen < 0:
                        height_on_screen = 0

                    # draw vert line
                    if height_on_screen < y_buffer[num_ray]:
                        for screen_y in range(height_on_screen, y_buffer[num_ray]):
                            screen_array[num_ray, screen_y] = color_map[x, y]
                        y_buffer[num_ray] = height_on_screen

        ray_angle += delta_angle
    return screen_array


class VoxelRender:
    def __init__(self, app):
        self._app = app
        self._player = app.player
        self._vertical_field_of_view = math.pi / 6
        self._horizontal_field_of_view = self._vertical_field_of_view / 2
        self._num_rays = app.width
        self._delta_angle = self._vertical_field_of_view / self._num_rays
        self._ray_distance = 5000
        self._scale_height = 920
        self._screen_array = np.full((app.width, app.height, 3), (0, 0, 0))

    def update(self):
        self._screen_array = ray_casting(self._screen_array,
                                         self._player.position, self._player.angle,
                                         self._player.height, self._player.pitch,
                                         self._app.width, self._app.height,
                                         self._delta_angle, self._ray_distance,
                                         self._horizontal_field_of_view, self._scale_height)

    def draw(self):
        pg.surfarray.blit_array(self._app.screen, self._screen_array)
