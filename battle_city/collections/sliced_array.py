from collections import defaultdict
from itertools import chain, product

from pygame.rect import Rect


class SlicedArray(object):
    """
    Used to find collision with static monsters like walls or coins
    Future: maybe quadtree? or something else?
    """
    _parts = None  # type: dict
    # parts[x_tile, y_tile] = list of objects
    _grid = 16  # type: int

    def __init__(self, monsters=None, grid=64):
        self._parts = defaultdict(list)
        self._grid = grid
        if monsters is not None:
            self.multiple_append(monsters)

    def multiple_append(self, monsters):
        for monster in monsters:
            self.append(monster)

    def append(self, static_monster):
        part = self._get_part_by_monster(static_monster)
        part.append(static_monster)

    def remove(self, static_monster):
        part = self._get_part_by_monster(static_monster)
        part.remove(static_monster)

    def _get_part_by_monster(self, static_monster) -> list:
        position = static_monster.position
        tile_x = position.x // self._grid
        tile_y = position.y // self._grid

        return self._parts[tile_x, tile_y]

    def __iter__(self):
        return chain.from_iterable(part for part in self._parts.values())

    def __len__(self):
        return sum(len(part) for part in self._parts.values())

    def find_nearest(self, position: Rect) -> list:
        grid = self._grid
        tile_start_x = max((position.left // grid) - 1, 0)
        tile_start_y = max((position.top // grid) - 1, 0)
        tile_stop_x = (position.right // grid) + 1
        tile_stop_y = (position.bottom // grid) + 1

        cords = product(
            range(tile_start_x, tile_stop_x),
            range(tile_start_y, tile_stop_y)
        )

        return list(chain.from_iterable(self._parts[x, y] for x, y in cords))
