import random
import pygame
from data_structures import Vector
from consts import *
from direction import Direction

downVector = Vector(0, WALLSIZE)
rightVector = Vector(WALLSIZE, 0)


class Tile:
    B = rightVector
    C = rightVector + downVector
    D = downVector

    def __init__(self):
        self.left = None
        self.right = None
        self.up = None
        self.down = None

        self.clear_walls()
        self.visited = False

    def unlock(self, direction):
        self.locked[direction] = False

    def draw(self, vector, surface):
        if self.locked[Direction.Up]:
            pygame.draw.line(surface, BLACK, tuple(vector), tuple(vector + Tile.B))
        if self.locked[Direction.Right]:
            pygame.draw.line(surface, BLACK, tuple(vector + Tile.B), tuple(vector + Tile.C))
        if self.locked[Direction.Down]:
            pygame.draw.line(surface, BLACK, tuple(vector + Tile.D), tuple(vector + Tile.C))
        if self.locked[Direction.Left]:
            pygame.draw.line(surface, BLACK, tuple(vector), tuple(vector + Tile.D))

    def clear_walls(self):
        self.locked = [True] * 4

    def get_random_nbr(self):
        nones = [
            self.up is None or self.up.visited,
            self.right is None or self.right.visited,
            self.down is None or self.down.visited,
            self.left is None or self.left.visited
        ]
        possible = [i for i in range(4) if not nones[i]]

        if len(possible) == 0:
            return None

        direction = possible[random.randrange(len(possible))]
        return self.__get_nbr(direction), direction

    def __get_nbr(self, direction):
        if direction == Direction.Up:
            return self.up
        if direction == Direction.Right:
            return self.right
        if direction == Direction.Down:
            return self.down
        if direction == Direction.Left:
            return self.left

    @property
    def wall_count(self):
        return sum(self.locked)
