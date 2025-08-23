import numpy as np 
import pygame as pg  

# np.dot( Object,rotxa(np.pi)) # Rotation by the x axis

Cube = np.array([[-1,-1, 1],[-1,-1, -1],[-1,1, 1],[-1,1, -1],[1,-1, 1],[1,-1, -1],[1,1, 1],[1,1, -1]])

def rotxa(object, angle):
    return np.dot( object,np.array([[1,0,0],[0,np.cos(angle),-np.sin(angle)],[0,np.sin(angle),np.cos(angle)]]) )

def rotya(object, angle):
    return np.dot( object,np.array([[np.cos(angle),0,np.sin(angle)],[0,1,0],[-np.sin(angle),0,np.cos(angle)]]) )

def rotza(object, angle):
    return np.dot( object,np.array([[np.cos(angle),-np.sin(angle),0],[np.sin(angle),np.cos(angle),0],[0,0,1]]) )
