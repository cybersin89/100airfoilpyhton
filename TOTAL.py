# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 17:07:29 2019

@author: etemo_000
"""

import os, time
import numpy as np
import matplotlib.pyplot as plt


def airfoil_coordinates(filename):

  with open(filename) as f:
    content = f.readlines()
#   readlines is reading the contents of the file line-by-line.
    
#  print(content)

  arr = []
  for i in content:

    elements = i.strip().split()
    
    if len(elements) == 2:
    
      try:    
        x,y = float(elements[0]), float(elements[1])
        arr.append([x,y])
      except:
        pass
  return np.array(arr)

# os.walk : It allows you to walk down a directory tree structure.
for root, dir, files in os.walk("airfoildata/"):
  
  for i,j in enumerate(files):
#Enumerate() method adds a counter to an iterable and returns it in a form of enumerate object. 
#This enumerate object can then be used directly in for loops or be converted into a list of tuples using list() method.    
    filename = 'airfoildata/' + j
    new_filename = 'Normalized Airfoil Dataset/' + j

    arr = airfoil_coordinates(filename)
    
    x, y = arr[:,0], arr[:,1]

                                    #PART A :
    #Initialize :
    x[0] = 1.0
    y[0] = 0.0
    x[-1] = 1.0
    y[-1]=0.0
    np.savetxt(new_filename,arr)
    arr= airfoil_coordinates(new_filename)
#panel circle
    def thickness_chord_meancamber(x,y):
            t,k,m=[],[],[]
            for j in range (int((len(x)-1)/2)):#thickness
                t.append(abs(y[j+1]-y[len(x)-2-j]))
                k.append((x[j+1]+x[len(x)-2-j])/2)
                m.append((y[j+1]+y[len(x)-2-j])/2)
            u=max(t)
            c=t.index(u)
            o=[x[c+1],x[len(x)-2-c]]
            p=[y[c+1],y[len(x)-2-c]]
            a=[1,0]#chord point cause of normalized all= 1
            b=[0,0]#
            return k,m,o,p,a,b,u
    def panel_definition(x,y,N):
        
        
        R=(x.max() - x.min()) / 2 #circle radius
        circle_center_x= (x.max() + x.min())/2 #x coordinate of center point
        circle_x=circle_center_x+R*np.cos(np.linspace(0.0,2*np.pi,N+1)) #x coordinate of circle
    
        x_pa=np.copy(circle_x)  #projection of the x coord on the surface
        y_pa=np.empty_like(x_pa) 
    
        #x,y=np.append(x,x[0]),np.append(y,y[0])
        K=0
        for i in range(N):
            while K<len(x)-1:
                if(x[K]<=x_pa[i]<=x[K+1]) or (x[K+1] <= x_pa[i] <= x[K]):
                    break
                else:
                    K+= 1
            a = (y[K + 1] - y[K]) / (x[K + 1] - x[K])
            b = y[K + 1] - a * x[K + 1]
            y_pa[i] = a * x_pa[i] + b
        y_pa[N] = y_pa[0]
     #point that seperate upper and lower surface at 0,0
     #which causes a plot problem so that the point defined separately
        a1=(y[int((len(y)-1)/2)+1] - y[int((len(y)-1)/2)]) / (x[int((len(y)-1)/2)+1] - x[int((len(y)-1)/2)])
        b1= 1*(y[int((len(y)-1)/2) + 1] - a1 * x[int((len(y)-1)/2) + 1])
        y_pa[int((N/2)+1)]= a1 * x_pa[int((N/2)+1)] + b1
    
        x_pa[20]=0
        y_pa[20]=0
        return x_pa,y_pa
    
    def normal_of_panels(x_pa,y_pa,N):
        h,l,theta=[],[],[]
        hip=[]
        for j in range (N):
            hip.append(np.sqrt((x_pa[j+1]-x_pa[j])**2+(y_pa[j+1]-y_pa[j])**2))
            h.append((x_pa[j+1]+x_pa[j])/2)
            l.append((y_pa[j+1]+y_pa[j])/2)
        
            if x_pa[j+1]-x_pa[j]>0:
            
                theta.append(np.pi+np.arccos(-(y_pa[j+1]-y_pa[j])/hip[j]))
      
            else:
            
                theta.append(np.arccos((y_pa[j+1]-y_pa[j])/hip[j]))
                
        return hip,h,l,theta
    def cusped_sharped(x_pa,y_pa,N):
        
        m1=(y_pa[2]-y_pa[1])/(x_pa[2]-x_pa[1])
        m2=(y_pa[N]-y_pa[N-1])/(x_pa[N]-x_pa[N-1])
        beta=abs((m1-m2)/(1+(m1*m2)))
        if beta<=np.deg2rad(15):
            ta_shape='CUSPED'
        else:
            ta_shape='POINTED'
        return beta,ta_shape
    N=40
    k,m,o,p,a,b,u=thickness_chord_meancamber(x,y)
    x_pa,y_pa=panel_definition(x,y,N)
    hip,h,l,theta=normal_of_panels(x_pa,y_pa,N)
    beta,ta_shape=cusped_sharped(x_pa,y_pa,N)
    plt.title(files[i])
    plt.xlim(-0.2,1.2)
    plt.ylim(-0.2,0.2)
    plt.grid(True)
    plt.xlabel('X', fontsize=10)
    plt.ylabel('Y', fontsize=10)
    plt.text(0.2, 0.15,'MAX THICKNESS=%f'%u)
    plt.text(0.2, -0.15,'TRAILING EDGE=%s'%ta_shape)
    plt.plot(x,y)
#   plt.plot(x_pa,y_pa)
#   plt.plot(h,l,'o')
    plt.quiver(h,l,np.cos(theta),np.sin(theta))
    plt.plot(a,b)
    plt.plot(o,p)
    plt.plot(k,m,'o')
#   plt.savefig(files[i] +  '.jpg')
    plt.show()
    
   