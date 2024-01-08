# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 17:23:06 2024

@author: Wasidy
"""

import numpy as np
#import matplotlib as mlib
import matplotlib.pyplot as plt
import time
from PIL import Image, ImageTk

import tkinter as tk

x_size = 512
y_size = 256

view_scale = 4



root = tk.Tk()

canvas = tk.Canvas(root,width=x_size*view_scale, height=y_size*view_scale)
canvas.pack()

#w = tk.Canvas(root, width = 900, height = 900)
#w.pack()


# Define life grid


world = np.random.randint(2,size =(y_size,x_size))

world_ng = np.zeros((y_size,x_size), dtype=np.int16)




while True:
#def life_game(world, world_ng, x_size, y_size, view_scale):
    
    canvas.delete("all")
    for active_y in range(y_size):
        for active_x in range(x_size):
            inhabited = 0
            cell_status = world[active_y, active_x]
            
            for y in range(-1,2,1):
                for x in range(-1,2,1):
                    if y==0 and x==0:
                        
                        continue
                    n_y = (active_y + y) % y_size
                    n_x = (active_x + x) % x_size
                    inhabited += world[n_y, n_x]
            
            
            if cell_status == 0:
                if inhabited ==3:
                    world_ng[active_y, active_x] = 1 #New life is born!

            if cell_status == 1:
            
                if 2<= inhabited <=3:
                    world_ng[active_y, active_x] = 1 #Lives
                else:
                    world_ng[active_y, active_x] = 0 #Dies


    world_show = world_ng[:,:,np.newaxis]
    world_show = world_show.repeat(view_scale, axis=0).repeat(view_scale, axis = 1).repeat(3, axis = 2)*255

    img = ImageTk.PhotoImage(image=Image.fromarray(np.uint8(world_show)))

    world = world_ng.copy()   

    canvas.create_image(0,0, anchor="nw", image=img)
    canvas.update()
    #root.after(10, life_game(world, world_ng, x_size, y_size, view_scale))
    #time.sleep(0.2)

#root.mainloop()
    #w.update()
    #time.sleep(0.2)

    #plt.pause(0.2)

#life_game(world, world_ng, x_size, y_size, view_scale)
print ("fuck")
#root.mainloop()



#for x in range(min, min+max):
#    print ((x-1)%max)
    
