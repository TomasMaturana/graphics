# coding=utf-8
#from OpenGL.GL import *
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def groundFun1(x, y):
    if np.sqrt(x*x+y*y)>45:
        return 0
    elif (x>=y+25 and x<25) or (np.sqrt(x*x+y*y)>37 and np.sqrt(x*x+y*y)<41) or (np.sqrt(x*x+y*y)>25 and np.sqrt(x*x+y*y)<30) or (np.sqrt(x*x+y*y)>15 and np.sqrt(x*x+y*y)<19):
        return (50-np.sqrt(x*x+y*y)*0.8)*0.5-2
    else:
        return (50-np.sqrt(x*x+y*y))*0.5+10

def skyFun1(x, y):
    if np.sqrt(x*x+y*y)>45:
        return 0
    else:
        return (50-np.sqrt(x*x+y*y)*0.8)*0.5-2*np.cos(x)+np.sin(y)+10
        

def groundFun2(x, y):
    return np.cos(y*np.sin(x))+np.cos(x/50)+5

def skyFun2(x, y):
    if x<-45 or y<-45:
        return 5/(x*y+1)+4
    elif x>45:
        return 5/(x)+4
    elif y>45:
        return np.sin(y/-8)*15+4
    else:
        return np.cos(y*x*0.01)+np.cos(x/2)*4+10


def generateMap(xs, ys, gFun, sFun):
    skyHeight = np.empty([xs, ys])
    groundHeight = np.empty([xs, ys])
    skyTexture = np.empty([xs, ys])
    groundTexture = np.empty([xs, ys])

    xh = int(xs/2)
    yh = int(ys/2)

    for i in range(xs):
        for j in range(ys):
            skyHeight[i, j] = sFun(i-xh, j-yh)
            skyTexture[i, j] = np.random.choice([0, 4, 5])
            groundHeight[i, j] = gFun(i-xh, j-yh)
            groundTexture[i, j] = np.random.choice([1, 2, 3])

    return np.array([groundHeight, skyHeight, groundTexture, skyTexture])


if __name__ == "__main__":

    map1 = generateMap(100, 100, groundFun1, skyFun1)
    np.save('map1.npy', map1)

    map2 = generateMap(100,100, groundFun2, skyFun2)
    np.save('map2.npy', map2)
