
import random
from tile import Tile
from direction import Direction
from data_structures import Vector, Stack
from consts import *


class Maze:
    def __init__(self, length, height):
        self.length = length
        self.height = height
        self.board = [[Tile() for j in range(length)] for i in range(height)]

        for i in range(height):
            for j in range(length):
                self.board[i][j] = Tile()

        for i in range(height):
            for j in range(length):
                if i < height - 1:
                    self.board[i][j].right = self.board[i + 1][j]
                    self.board[i + 1][j].left = self.board[i][j]
                if j < length - 1:
                    self.board[i][j].down = self.board[i][j + 1]
                    self.board[i][j + 1].up = self.board[i][j]

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
        entrance = random.randrange(maze.length)
        exit = random.randrange(maze.length)
        maze.board[entrance][0].unlock(Direction.Up)
        maze.board[exit][maze.height - 1].unlock(Direction.Down)
