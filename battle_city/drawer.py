from pygame.font import SysFont

from battle_city.basic import Direction
from battle_city.monsters.wall import Wall, Metal, Water

from pygame.image import load as img_load
from pygame.display import set_mode, flip
from pygame.transform import rotate
from pygame.draw import rect as draw_rect
from pygame import init as pygame_init


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


def _load_simple(name):
    pathfile = path.join(IMAGES_DIR, f'{name}.png')
    return img_load(pathfile)


IMG_PLAYER_1 = _load_pack('player_1')
IMG_PLAYER_2 = _load_pack('player_2')
IMG_NPC = _load_pack('npc')
BULLET = _load_pack('bullet')
FREEZE = _load_simple('freeze')

WALLS = {
    Wall: _load_simple('wall'),
    Metal: _load_simple('metal'),
    Water: _load_simple('water'),
}


class Drawer(object):
    game = None  # type: game.Game
    time: int = 0

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    OFFSET = 32

    OFFSET_LABELS_X = 550
    OFFSET_LABELS_Y = 32
    FONT_SIZE = 24

    PLAYER_COLORS = [
        (255, 255, 0),
        (0, 255, 0),
    ]


    def __init__(self, game):
        pygame_init()
        self.time = 0
        self.screen = set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)
        self.font = SysFont('monospace', self.FONT_SIZE, bold=True)
        self.game = game

    def render(self):
        self.time = self.time + 1
        if self.time >= 100:
            self.time = 0
    
        self._render_background()
        self._render_players()
        self._render_bullets()
        self._render_npcs()
        self._render_walls()
        self._render_text()
        flip()

    def _render_background(self):
        self.screen.fill((64, 64, 64))
        offset = self.OFFSET
        rect_size = (offset, offset, self.game.WIDTH, self.game.HEIGHT)
        draw_rect(self.screen, (0, 0, 0), rect_size)

    def _render_players(self):
        players = self.game.players
        for player in players:
            if player.player_id == 0:
                image = IMG_PLAYER_1
            elif player.player_id == 1:
                image = IMG_PLAYER_2

            self._blit(image, player)
            if player.is_freeze and self.time % 30 > 15:
                self._blit_simple(FREEZE, player)

    def _render_npcs(self):
        npcs = self.game.npcs
        for npc in npcs:
            self._blit(IMG_NPC, npc)

    def _render_bullets(self):
        for bullet in self.game.bullets:
            self._blit(BULLET, bullet)

    def _render_walls(self):
        for wall in self.game.walls: 
            position = wall.position
            cords = (self.OFFSET + position.x, self.OFFSET + position.y)
            area = (0, 0, position.width, position.height)
            image = WALLS[type(wall)]
            self.screen.blit(image, cords, area)

    def _render_text(self):
        self._render_label('BATTLE CITY AI', (0, 0))
        self._render_label(f'NPCs left: {self.game.npcs_left}', (0, 40))
        self._render_label(f'NPCs in area: {len(self.game.npcs)}', (0, 80))
        self._render_label(f'Time: {self.time}', (0, 120))

        if not self.game.is_ready():
            self._render_label(f'NOT READY', (0, 180))

        for num, player in enumerate(self.game.players, start=1):
            connected_label = '' if player.connection else ' WAIT'
            label = f'P{player.player_id}{connected_label}: {player.score:06d}'
            color = self.PLAYER_COLORS[player.player_id]
            self._render_label(label, (0, 200 + 40 * num), color)

    def _render_label(self, label: str, cords, color=(255, 255, 255)):
        image = self.font.render(label, 1, color)
        new_cords = (self.OFFSET_LABELS_X + cords[0], self.OFFSET_LABELS_Y + cords[1])
        self.screen.blit(image, new_cords)

    def _blit_simple(self, image, monster):
        position = monster.position
        cords = (self.OFFSET + position.x, self.OFFSET + position.y)
        self.screen.blit(image, cords)

    def _blit(self, image_pack, monster):
        image = image_pack[monster.direction]
        self._blit_simple(image, monster)

