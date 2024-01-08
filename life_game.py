# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 17:23:06 2024

@author: Wasidy
"""

import builtins
import sys
import numpy as np
import pygame


class LifeGame:
    """Class of Conway's Game of Life"""
    def __init__(self, x_size = 64, y_size = 64, view_scale = 10):
        self.x_size = x_size
        self.y_size = y_size
        self.view_scale = view_scale
        self.world = np.random.randint(2,size =(y_size,x_size))
        self.world_ng = np.zeros((y_size,x_size), dtype=np.int16)

    def reset(self):
        self.world = np.random.randint(2,size =(self.y_size,self.x_size))

    def step(self):
        for active_y in range(self.y_size):
            for active_x in range(self.x_size):

                inhabited = builtins.sum(self.world[(y+active_y-1) % self.y_size,(x+active_x-1) % self.x_size] \
                    for x in range(3) for y in range(3) if not (y==1 and x==1))

                self.world_ng[active_y, active_x] = 1 if (inhabited==3 and self.world[active_y, active_x]==0) \
                    or (inhabited in range(2,4) and self.world[active_y, active_x] == 1) else 0

        self.world = self.world_ng.copy()

        world_show = self.world_ng[:,:,np.newaxis]
        world_show = world_show.repeat(self.view_scale, axis=0).repeat(self.view_scale, axis=1).repeat(3, axis=2)*255
        return np.uint8(world_show).tobytes()


if __name__ == '__main__':

    x_s = 256
    y_s = 128
    v_scale = 5
    my_life = LifeGame(x_size = x_s, y_size = y_s, view_scale = v_scale)

    pygame.init()
    screen = pygame.display.set_mode((x_s*v_scale,y_s*v_scale), vsync=1)
    clock = pygame.time.Clock()

    while True:
        clock.tick(10)
        im2 = my_life.step()
        pygame_surface = pygame.image.fromstring(im2, (x_s*v_scale,y_s*v_scale), "RGB")
        screen.blit(pygame_surface, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                my_life.reset()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
