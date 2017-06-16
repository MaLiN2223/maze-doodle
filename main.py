import pygame
from consts import *
from game import Game

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
done = False
game = Game()
game.start()


while not done:
    for event in pygame.event.get():
        processed = game.process_event(event)

        if not processed:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True


    screen.fill(WHITE)
    game.display(screen)
    pygame.display.flip()

pygame.quit()
