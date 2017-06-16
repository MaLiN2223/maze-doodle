import random
from tile import Tile
from direction import Direction
from data_structures import Vector, Stack
from consts import *


class Maze:
    def __init__(self, length, height):
        self.length = length
        self.height = height
        self.board = [[Tile() for j in range(self.length)] for i in range(self.height)]
        for i in range(self.height):
            for j in range(self.length):
                if i < self.height - 1:
                    self.board[i][j].right = self.board[i + 1][j]
                    self.board[i + 1][j].left = self.board[i][j]
                if j < self.length - 1:
                    self.board[i][j].down = self.board[i][j + 1]
                    self.board[i][j + 1].up = self.board[i][j]

        self.init()

    def init(self):
        self.entrance = None
        self.exit = None

        for i in range(self.height):
            for j in range(self.length):
                self.board[i][j].clear_walls()
                self.board[i][j].visited = False


    def display(self, surface):
        offset = Vector(*MAZEOFFSET)
        for i in range(self.height):
            for j in range(self.length):
                self.board[i][j].draw(offset + Vector(i * WALLSIZE, j * WALLSIZE), surface)

    @staticmethod
    def randomize(maze):
        stack = Stack()
        current = maze.board[0][0]
        visited_count = 0

        while True:
            q = current.get_random_nbr()
            if not current.visited:
                visited_count += 1

            current.visited = True
            if q is None:
                if stack.size > 0:
                    current = stack.pop()
                else:
                    raise StopIteration()
            else:
                next, x = q
                stack.push(current)
                current.unlock(x)
                next.unlock((x + 2) % 4)
                current = next

            if visited_count >= maze.length * maze.height:
                raise StopIteration()

            yield current

    @staticmethod
    def randomize_exits(maze):
        maze.entrance = random.randrange(maze.length)
        maze.exit = random.randrange(maze.length)
        maze.board[maze.entrance][0].unlock(Direction.Up)
        maze.board[maze.exit][maze.height - 1].unlock(Direction.Down)
