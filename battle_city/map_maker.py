from battle_city.monsters import Wall, Water, Metal, Spawner, Coin
from os import path

from battle_city.monsters.wall import TinyWall

DIR = path.abspath(path.dirname(__file__))
MAPS_DIR = path.join(DIR, '..', 'maps')


class MapCharError(Exception):
    pass


class MapMaker(object):

    CHAR_TO_METHOD = {
        '.': 'empty',
        ' ': 'empty',
        '$': 'coin',
        '\n': 'empty',
        '#': 'brick',
        '@': 'metal',
        '~': 'water',
        '*': 'spawn',
        '1': 'player',
        '2': 'player',
        '3': 'player',
        '4': 'player',
    }

    def __init__(self, game, data):
        self.game = game
        self.data = data

    @staticmethod
    def load_data_from_name(name):
        filepath = path.join(MAPS_DIR, '%s.map' % name)
        with open(filepath) as fp:
            lines = fp.readlines()[:16]
        return [line[:16].ljust(16, '.') for line in lines]

    def make(self):
        methods = {
            char: getattr(self, 'make_%s' % name, self.make_unknown)
            for char, name in self.CHAR_TO_METHOD.items()
        }

        for tile_y, line in enumerate(self.data):
            for tile_x, char in enumerate(line):
                cords = (tile_x * 32, tile_y * 32)
                tile_cords = (tile_x, tile_y)
                method = methods.get(char, self.make_unknown)
                method(char, cords, tile_cords)

    def make_empty(self, char, cords, tile_cords):
        """
        Srsly do nothing
        """
        pass

    def make_brick(self, char, cords, tile_cords):
        x, y = cords
        for x_shift in range(0, Wall.SIZE, 8):
            for y_shift in range(0, Wall.SIZE, 8):
                wall = TinyWall(x + x_shift, y + y_shift)
                self.game.walls.append(wall)

    def make_coin(self, char, cords, tile_cords):
        coin = Coin(*cords)
        self.game.coins.append(coin)

    def make_water(self, char, cords, tile_cords):
        water = Water(*cords)
        self.game.walls.append(water)

    def make_metal(self, char, cords, tile_cords):
        metal = Metal(*cords)
        self.game.walls.append(metal)

    def make_player(self, char, cords, tile_cords):
        number = int(char) - 1
        spawner = Spawner(*cords)
        self.game.player_spawns[number] = spawner

    def make_spawn(self, char, cords, tile_cords):
        spawner = Spawner(*cords)
        self.game.npc_spawns.append(spawner)

    def make_unknown(self, char, cords, tile_cords):
        raise MapCharError(char, tile_cords)
