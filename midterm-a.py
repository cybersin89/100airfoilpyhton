# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:20:18 2019

@author: etemo_000
"""

import os
import numpy as np



def airfoil_coordinates(filename):

  with open(filename) as f:
    contents = f.readlines()
#   readlines is reading the contents of the file line-by-line.
    
#  print(content)

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


for root, dir, files in os.walk("airfoildata/"):
  
  for i,j in enumerate(files):
  
    filename = 'airfoildata/' + j
    new_filename = 'Normalized Airfoil Dataset/' + j

    coords = airfoil_coordinates(filename)
    
    x,y = coords[:,0],coords[:,1]

                                   
    #normalizing
    x[0] = 1.
    y[0] = .0
    x[-1] = 1.
    y[-1]=.0
    np.savetxt(new_filename,coords)