import pygame as pg
import numpy as np
import math


class Player:
    def __init__(self):
        self.position = np.array([0, 0], dtype=float)
        self.angle = math.pi / 4
        self.height = 270
        self.pitch = 40
        self.angle_velocity = 0.01
        self.velocity = 3

    def update(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_UP]:
            self.pitch += self.velocity
        if pressed_key[pg.K_DOWN]:
            self.pitch -= self.velocity

        if pressed_key[pg.K_LEFT]:
            self.angle -= self.angle_velocity
        if pressed_key[pg.K_RIGHT]:
            self.angle += self.angle_velocity

        if pressed_key[pg.K_q]:
            self.height += self.velocity
        if pressed_key[pg.K_e]:
            self.height -= self.velocity

        if pressed_key[pg.K_w]:
            self.position[0] += self.velocity * cos_a
            self.position[1] += self.velocity * sin_a
        if pressed_key[pg.K_s]:
            self.position[0] -= self.velocity * cos_a
            self.position[1] -= self.velocity * sin_a
        if pressed_key[pg.K_a]:
            self.position[0] += self.velocity * sin_a
            self.position[1] -= self.velocity * cos_a
        if pressed_key[pg.K_d]:
            self.position[0] -= self.velocity * sin_a
            self.position[1] += self.velocity * cos_a
