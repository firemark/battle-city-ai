from battle_city.basic import Direction

from pygame.image import load as img_load
from pygame.display import set_mode, flip
from pygame.transform import rotate

from os import path

DIR = path.abspath(path.dirname(__file__))
IMAGES_DIR = path.join(DIR, '..', 'images')


def _load_pack(name):
    pathfile = path.join(IMAGES_DIR, f'{name}.png')
    image = img_load(pathfile)

    return {
        Direction.UP: image,
        Direction.LEFT: rotate(image, 90),
        Direction.DOWN: rotate(image, 180),
        Direction.RIGHT: rotate(image, 270),
    }


IMG_PLAYER_1 = _load_pack('player_1')
IMG_PLAYER_2 = _load_pack('player_2')
BULLET = _load_pack('bullet')


class Drawer(object):
    game = None  # type: game.Game

    def __init__(self, game):
        self.screen = set_mode((800, 600), 0, 32)
        self.game = game

    def render(self):
        self.screen.fill((0, 0, 0))
        self._render_players()
        self._render_bullets()
        self._render_text()
        flip()

    def _render_players(self):
        players = self.game.players
        for player in players:
            if player.player_id == 0:
                image = IMG_PLAYER_1
            if player.player_id == 1:
                image = IMG_PLAYER_2

            self._blit(image, player)

    def _render_bullets(self):
        bullets = self.game.bullets
        for bullet in bullets:
            self._blit(BULLET, bullet)

    def _render_text(self):
        pass

    def _blit(self, image_pack, monster):
        image = image_pack[monster.direction]
        self.screen.blit(image, monster.position)

