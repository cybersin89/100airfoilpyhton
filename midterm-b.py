# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 17:00:07 2019

@author: etemo_000
"""
import os
import numpy as np
import matplotlib.pyplot as plt


def airfoil_coordinates(filename):

  with open(filename) as f:
    contents = f.readlines()


  coords = []
  for i in contents:

    elements = i.strip().split()
    
    if len(elements) == 2:
    
      try:    
        x,y = float(elements[0]), float(elements[1])
        coords.append([x,y])
      except:
        pass
  return np.array(coords)


for root, dir, files in os.walk("Normalized Airfoil Dataset/"):
  
  for i,j in enumerate(files):
   
    
    new_filename = 'Normalized Airfoil Dataset/' + j
    coords=airfoil_coordinates(new_filename)

    x, y = coords[:,0], coords[:,1]

                                
    
    
    
    def thickness_chord_meancamber(x,y):
            t,k,m=[],[],[]
            for j in range (int((len(x)-1)/2)):
                t.append(abs(y[j+1]-y[len(x)-2-j]))#thickness
                k.append((x[j+1]+x[len(x)-2-j])/2)#mean camber line
                m.append((y[j+1]+y[len(x)-2-j])/2)
            u=max(t)
            c=t.index(u)
            o=[x[c+1],x[len(x)-2-c]]
            p=[y[c+1],y[len(x)-2-c]]
            a=[1,0]#chord point cause of normalized all= 1
            b=[0,0]#
            return k,m,o,p,a,b,u
        
    k,m,o,p,a,b,u=thickness_chord_meancamber(x,y)
    plt.title(files[i].replace('.dat',''))
    plt.xlim(-0.2,1.2)
    plt.ylim(-0.2,0.2)
    plt.grid(True)
    plt.xlabel('X', fontsize=10)
    plt.ylabel('Y', fontsize=10)
    plt.text(0.2, 0.15,'MAX THICKNESS=%f'%u)
    plt.plot(x,y)
    plt.plot(a,b)
    plt.plot(x,y,'o')
    plt.plot(o,p)
    plt.plot(k,m,'o')
    pathB='PART B/'+ j.replace('.dat','')
    plt.savefig(pathB+  '.jpg')
    plt.show()

