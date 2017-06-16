import pygame
from data_structures import Vector
from direction import Direction
from maze import Maze
from consts import *


moves = {
    pygame.K_RIGHT: Direction.Right,
    pygame.K_DOWN: Direction.Down,
    pygame.K_UP: Direction.Up,
    pygame.K_LEFT: Direction.Left,
}

class Game:
    player_offset = Vector(WALLSIZE // 2, WALLSIZE // 2) + Vector(*MAZEOFFSET)

    def __init__(self):
        self.maze = Maze(30, 30)

    def start(self):
        self.maze.init()
        generator = Maze.randomize(self.maze)
        Maze.randomize_exits(self.maze)
        try:
            while next(generator):
                pass
        except StopIteration:
            pass
        self.player_position = Vector(self.maze.entrance, 0)

    def process_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.start()
                return True
            if event.key in moves:
                self.move_player(moves[event.key])
                return True
        return False

    def display(self, screen):
        self.maze.display(screen)
        pos = Vector(WALLSIZE * self.player_position.X,
                     WALLSIZE * self.player_position.Y) + Game.player_offset
        pygame.draw.circle(screen, RED, tuple(pos), WALLSIZE // 3)

    def move_player(self, direction):
        if self.maze.board[self.player_position.X][self.player_position.Y].locked[direction]:
            return
        move = (0, 0)
        if direction == Direction.Right and self.player_position.X < self.maze.length:
            move = (1, 0)
        if direction == Direction.Left and self.player_position.X > 0:
            move = (-1, 0)
        if direction == Direction.Down and self.player_position.Y < self.maze.height:
            move = (0, 1)
        if direction == Direction.Up and self.player_position.Y > 0:
            move = (0, -1)
        self.player_position += Vector(*move)
