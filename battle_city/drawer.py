from battle_city.basic import Direction
from battle_city.monsters.wall import Wall, Metal, Water, TinyWall

from pygame.image import load as img_load
from pygame.transform import rotate

from os import path

import pygame
import pygame.display
import pygame.draw


DIR = path.abspath(path.dirname(__file__))
IMAGES_DIR = path.join(DIR, '..', 'images')


def _load_pack(name):
    pathfile = path.join(IMAGES_DIR, '%s.png' % name)
    image = img_load(pathfile)

    return {
        Direction.UP: image,
        Direction.LEFT: rotate(image, 90),
        Direction.DOWN: rotate(image, 180),
        Direction.RIGHT: rotate(image, 270),
    }


def _load_simple(name):
    pathfile = path.join(IMAGES_DIR, '%s.png' % name)
    return img_load(pathfile)


class Drawer(object):
    game = None  # type: game.Game
    time = 0 # type: int

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

    IMAGES = dict(
        IMG_PLAYER_1_1=_load_pack('player_11'),
        IMG_PLAYER_2_1=_load_pack('player_21'),
        IMG_NPC_1=_load_pack('npc_1'),
        IMG_NPC_2=_load_pack('npc_2'),
        IMG_PLAYER_1_2=_load_pack('player_12'),
        IMG_PLAYER_2_2=_load_pack('player_22'),
        BULLET=_load_pack('bullet'),
        FREEZE=_load_simple('freeze'),
    )

    WALLS = {
        TinyWall: _load_simple('wall'),
        Metal: _load_simple('metal'),
        Water: _load_simple('water'),
    }

    def __init__(self, game):
        pygame.init()
        pygame.display.set_caption('BATTLE CITY AI')
        self.time = 0
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), 0, 32)
        self.font = pygame.font.SysFont('monospace', self.FONT_SIZE, bold=True)
        self.game = game

    def render(self):
        self._support_pygame_events()

        self.time = self.time + 1
        if self.time >= 100:
            self.time = 0
    
        self._render_background()
        self._render_players()
        self._render_bullets()
        self._render_npcs()
        self._render_walls()
        self._render_text()
        pygame.display.flip()

    def _support_pygame_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit(0)

    def _render_background(self):
        self.screen.fill((0x5f, 0x57, 0x4f))
        offset = self.OFFSET
        rect_size = (offset, offset, self.game.WIDTH, self.game.HEIGHT)
        pygame.draw.rect(self.screen, (0, 0, 0), rect_size)

    def _render_players(self):
        players = self.game.alive_players
        for player in players:
            if player.player_id == 0:
                image_pack = self._get_frame(player, 'IMG_PLAYER_1')
            else:
                image_pack = self._get_frame(player, 'IMG_PLAYER_2')

            self._blit(image_pack, player)
            if player.is_freeze and self.time % 30 < 15:
                self._blit('FREEZE', player)

    def _render_npcs(self):
        npcs = self.game.npcs
        for npc in npcs:
            image = self._get_frame(npc, 'IMG_NPC')
            self._blit(image, npc)

    def _get_frame(self, obj, img: str):
        prediction = self.time * obj.speed * 0.8 % 2 < 1
        image_pack = '{}_{}'.format(img, 1 if prediction else 2)
        return image_pack

    def _render_bullets(self):
        for bullet in self.game.bullets:
            self._blit('BULLET', bullet)

    def _render_walls(self):
        for wall in self.game.walls: 
            position = wall.position
            cords = (self.OFFSET + position.x, self.OFFSET + position.y)
            xx = position.x % Wall.SIZE
            yy = position.y % Wall.SIZE
            area = (xx, yy, position.width, position.height)
            image = self.WALLS[type(wall)]
            self.screen.blit(image, cords, area)

    def _render_text(self):
        npcs_left = self.game.npcs_left
        npcs_in_area = len(self.game.npcs)
        time_left = self.game.time_left
        self._render_label('BATTLE CITY AI', (0, 0))
        self._render_label('NPCs left:    {:03d}'.format(npcs_left), (0, 40))
        self._render_label('NPCs in area: {:03d}'.format(npcs_in_area), (0, 80))
        self._render_label('Time left:    {:03d}'.format(time_left), (0, 120))

        if not self.game.is_ready():
            self._render_label('NOT READY', (0, 180))
        elif self.game.is_over():
            self._render_label('GAME OVER', (0, 180), color=(255, 0, 0))

        for num, player in enumerate(self.game.players, start=1):
            name_label = player.nick or 'P%s' % player.player_id
            info_label = self._get_info_label(player)
            label = '{:10} {:06d}'.format(name_label, player.score)
            color = self.PLAYER_COLORS[player.player_id]
            self._render_label(label, (0, 200 + 40 * num), color)
            self._render_label(info_label, (0, 220 + 40 * num), color)

    def _get_info_label(self, player):
        if player.is_game_over and self.time < 50:
            return 'KILLED'
        elif not player.connection:
            return 'WAIT'
        elif player.is_freeze:
            return 'FREEZE'
        else:
            return ''

    def _render_label(self, label: str, cords, color=(0xff, 0xf1, 0xe8)):
        image = self.font.render(label, 1, color)
        new_cords = (self.OFFSET_LABELS_X + cords[0], self.OFFSET_LABELS_Y + cords[1])
        self.screen.blit(image, new_cords)

    def _blit(self, image_name, monster):
        image_pack = self.IMAGES[image_name]

        if isinstance(image_pack, dict):
            image = image_pack[monster.direction]
        else:
            image = image_pack

        position = monster.position
        cords = (self.OFFSET + position.x, self.OFFSET + position.y)
        self.screen.blit(image, cords)

