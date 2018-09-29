"""
BROKEN
I HATE THIS
"""
from pyglet.image import SolidColorImagePattern
from pyglet.sprite import Sprite
from pyglet.window import FPSDisplay

from battle_city.basic import Direction
from battle_city.monsters.wall import Wall
from battle_city.drawer import Drawer as OldDrawer

from os import path

import pyglet


DIR = path.abspath(path.dirname(__file__))
IMAGES_DIR = path.join(DIR, '..', 'images')


class Drawer(OldDrawer):
    window = None

    def __init__(self, game):
        self.window = pyglet.window.Window(
            width=self.SCREEN_WIDTH,
            height=self.SCREEN_HEIGHT,
            caption='BATTLE CITY AI',
        )
        # I dunno what this is doing
        # BUT i need this to run pyglet without event loop
        pyglet.app.event_loop._legacy_setup()

        self.fps = FPSDisplay(self.window)
        self.background = pyglet.image.create(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.time = 0
        self.game = game

    @staticmethod
    def _load_pack(name):
        pathfile = path.join(IMAGES_DIR, '%s.png' % name)
        image = pyglet.image.load(pathfile).get_texture()

        return {
            Direction.UP: image.get_image_data(),
            Direction.LEFT: image.get_transform(rotate=90).get_image_data(),
            Direction.DOWN: image.get_transform(rotate=180).get_image_data(),
            Direction.RIGHT: image.get_transform(rotate=270).get_image_data(),
        }

    @staticmethod
    def _load_simple(name):
        pathfile = path.join(IMAGES_DIR, '%s.png' % name)
        return pyglet.image.load(pathfile)

    def render(self):
        self.window.clear()
        super().render()

    def _post_render(self):
        self._render_players()
        self.fps.draw()
        self.window.flip()

    def _support_events(self):
        return
        self.window.dispatch_event()

    def _render_background(self):
        self.background.blit(0, 0)

    def bake_static_background(self):
        surface = pyglet.image.create(
            width=self.SCREEN_WIDTH,
            height=self.SCREEN_HEIGHT,
            pattern=SolidColorImagePattern(color=(0x5f, 0x57, 0x4f, 0xff))
        )

        self._render_solid_colors(surface)
        self._render_walls(surface)
        self._render_coins(surface)
        self.background = surface

    def _render_solid_colors(self, surface):
        black = pyglet.image.create(
            width=self.game.WIDTH,
            height=self.game.HEIGHT,
            pattern=SolidColorImagePattern(color=(0, 0, 0, 0xff))
        )
        offset = self.OFFSET
        black.blit_to_texture(surface.get_texture().target, 0, offset, offset, 0)

    def _render_walls(self, surface):
        target = surface.get_texture().target
        for wall in self.game.walls: 
            position = wall.position
            xx = position.x % Wall.SIZE
            yy = position.y % Wall.SIZE
            image = self.WALLS[type(wall)]
            region = image.get_region(xx, yy, position.width, position.height)
            region = region.get_image_data()
            region.blit_to_texture(target, 0, self.OFFSET + position.x, self.OFFSET + position.y, 0)

    def _render_coins(self, surface):
        image = self.IMAGES['COIN']
        target = surface.get_texture().target
        for coin in self.game.coins:
            position = coin.position
            image.blit_to_texture(target, 0, position.x, position.y, 0)

    def _render_label(self, label: str, cords, color=(0xff, 0xf1, 0xe8)):
        label = pyglet.text.Label(
            label,
          font_name='Monospace',
          font_size=10,
          x=self.OFFSET_LABELS_X + cords[0],
          y=self.OFFSET_LABELS_Y + cords[1],
        )
        label.draw()

    def _blit(self, image_name, monster):
        image_pack = self.IMAGES[image_name]

        if isinstance(image_pack, dict):
            image = image_pack[monster.direction]
        else:
            image = image_pack

        position = monster.position
        image.blit(self.OFFSET + position.x, self.OFFSET + position.y)
