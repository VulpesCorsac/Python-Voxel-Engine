import pygame as pg

from player import Player
from voxel_render import VoxelRender


class App:
    def __init__(self):
        self._res = self.width, self.height = (800, 450)
        self.screen = pg.display.set_mode(self._res, pg.HWSURFACE | pg.SCALED)
        self._clock = pg.time.Clock()
        self.player = Player()
        self._voxel_render = VoxelRender(self)

    def update(self):
        self.player.update()
        self._voxel_render.update()

    def draw(self):
        self._voxel_render.draw()
        pg.display.flip()

    def run(self):
        while True:
            self.update()
            self.draw()
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
            self._clock.tick(200)
            pg.display.set_caption(f'FPS: {round(self._clock.get_fps(), 1)}')


if __name__ == '__main__':
    app = App()
    app.run()
