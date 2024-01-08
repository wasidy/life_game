# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 17:23:06 2024

@author: Wasidy
"""

import builtins
import sys
import numpy as np
import pygame
from scipy.ndimage import gaussian_filter

class LifeGame:
    """Class of Conway's Game of Life"""
    def __init__(self, x_size = 64, y_size = 64, view_scale = 10):
        self.x_size = x_size
        self.y_size = y_size
        self.view_scale = view_scale
        self.world = np.random.randint(2,size =(y_size,x_size))
        self.world_ng = np.zeros((y_size,x_size), dtype=np.int16)
        # For visual effects
        self.world_dead1 = np.zeros((y_size,x_size), dtype=np.int16)
        self.world_dead2 = np.zeros((y_size,x_size), dtype=np.int16)

    def reset(self):
        self.world = np.random.randint(2,size =(self.y_size,self.x_size))

    def step(self):
        for active_y in range(self.y_size):
            for active_x in range(self.x_size):

                inhabited = builtins.sum(self.world[(y+active_y-1) % self.y_size,(x+active_x-1) % self.x_size] \
                    for x in range(3) for y in range(3) if not (y==1 and x==1))

                self.world_ng[active_y, active_x] = 1 if (inhabited==3 and self.world[active_y, active_x]==0) \
                    or (inhabited in range(2,4) and self.world[active_y, active_x] == 1) else 0

        # Optimize code?
        
        self.world_dead2 = self.world_dead1.copy()/2
        self.world_dead1 = (self.world-self.world_ng)/2
        
        self.world_dead1[self.world_dead1<0] = 0
        
        
        self.world = self.world_ng.copy()
        
        world_show= self.world_ng + self.world_dead1 + self.world_dead2
        world_show[world_show>1] = 1
        
        
        world_show = world_show[:,:,np.newaxis].repeat(3, axis = 2)
        world_show[:,:,0] *= 255 #Red
        world_show[:,:,1] *= 10 #Green
        world_show[:,:,2] *= 10 #Blue
        
        #world_show = world_show.repeat(self.view_scale, axis=0).repeat(self.view_scale, axis=1).repeat(3, axis=2)*255
        world_show = gaussian_filter(world_show.repeat(self.view_scale, axis=0).repeat(self.view_scale, axis=1), sigma = 0.7)
        #gaussian_filter(a, sigma=7)
        #world_show[:,:,0] *= 96 #Red
        #world_show[:,:,1] *= 190 #Green
        #world_show[:,:,2] *= 255 #Blue
        #print (world_show.shape)
        
        
        return np.uint8(world_show).tobytes()


if __name__ == '__main__':

    x_s = 128
    y_s = 96
    v_scale = 10
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
