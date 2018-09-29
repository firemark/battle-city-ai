from pyglet.image import SolidColorImagePattern
from pyglet.window import FPSDisplay
from pyglet.gl import glBlendFunc, glEnable, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA

from battle_city.basic import Direction
from battle_city.monsters.wall import Wall
from battle_city.drawer import Drawer as OldDrawer

from os import path

import pyglet


DIR = path.abspath(path.dirname(__file__))
IMAGES_DIR = path.join(DIR, '..', 'images')


class Drawer(OldDrawer):
    window = None
    _labels_cache = None
    FONT_SIZE = 16

    def __init__(self, game):
        self.window = pyglet.window.Window(
            width=self.SCREEN_WIDTH,
            height=self.SCREEN_HEIGHT,
            caption='BATTLE CITY AI',
        )
        glEnable(GL_BLEND)
        self._labels_cache = {}
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
        image = pyglet.image.load(pathfile)
        texture = image.get_texture()
        texture.anchor_x = 16
        texture.anchor_y = 16

        def rotate(x):
            new_text = texture.get_transform(rotate=x)
            new_text.anchor_x = 0
            new_text.anchor_y = 0
            return new_text

        return {
            Direction.UP: rotate(0),
            Direction.DOWN: rotate(180),
            Direction.RIGHT: rotate(90),
            Direction.LEFT: rotate(270),
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
        black.blit_to_texture(
            surface.get_texture().target, 0,
            offset, self.SCREEN_HEIGHT - self.game.HEIGHT - offset, 0)

    def _render_walls(self, surface):
        target = surface.get_texture().target
        for wall in self.game.walls: 
            position = wall.position
            xx = position.x % Wall.SIZE
            yy = position.y % Wall.SIZE
            image = self.WALLS[type(wall)]
            region = image.get_region(xx, yy, position.width, position.height)
            region = region.get_image_data()
            region.blit_to_texture(
                target, 0,
                self.OFFSET + position.x,
                self.SCREEN_HEIGHT - self.OFFSET - position.y - position.height,
                0)

    def _render_coins(self, surface):
        image = self.IMAGES['COIN']
        target = surface.get_texture().target
        for coin in self.game.coins:
            position = coin.position
            image.blit_to_texture(
                target, 0,
                self.OFFSET + position.x,
                self.SCREEN_HEIGHT - self.OFFSET - position.y - position.height,
                0)

    def _render_label(self, id: str, label: str, cords, color=(0xff, 0xf1, 0xe8)):
        label_obj = self._labels_cache.get(id)
        text = label_obj and label_obj.text

        if text != label:
            label_obj = pyglet.text.Label(
                label,
                font_name='monospace',
                font_size=self.FONT_SIZE,
                color=color + (0xFF,),
                x=self.OFFSET_LABELS_X + cords[0],
                y=self.SCREEN_HEIGHT - self.OFFSET_LABELS_Y - cords[1],
            )
            self._labels_cache[id] = label_obj
        label_obj.draw()

    def _blit(self, image_name, monster):
        image_pack = self.IMAGES[image_name]

        if isinstance(image_pack, dict):
            image = image_pack[monster.direction]
        else:
            image = image_pack

        position = monster.position
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        image.blit(
            self.OFFSET + position.x,
            self.SCREEN_HEIGHT - self.OFFSET - position.y - position.height,
        )
