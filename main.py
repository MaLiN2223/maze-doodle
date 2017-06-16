import pygame
from maze import Maze
from consts import *

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
done = False

maze = Maze(100, 100)
generator = Maze.randomize(maze)
Maze.randomize_exits(maze)

try:
    while next(generator):
        if ANIMATE:
            screen.fill(WHITE)
            maze.display(screen)
            pygame.display.flip()
        else:
            pass
except StopIteration:
    pass

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(WHITE)
    maze.display(screen)
    pygame.display.flip()

pygame.quit()
