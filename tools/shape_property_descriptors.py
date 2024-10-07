import sys
import os
from vedo import load, write
from vedo import Mesh
import numpy as np

def A3(V1: tuple, V2: tuple, V3: tuple):
    #angle between three vertices
    V12 = V2 - V1
    V23 = V3 - V2
    V12_mag = np.linalg.norm(V12)
    V23_mag = np.linalg.norm(V23)
    angle = np.arccos(np.dot(V12,V23)/(V12_mag*V23_mag))
    return angle

def D1(V1: tuple):
    #distance between barycenter and vertex (assuming barycenter is (0,0,0))
    return np.linalg.norm(V1)

def D2(V1: tuple, V2: tuple):
    #distance between two vertices
    V12 = V2 - V1
    return np.linalg.norm(V12)

def D3(V1: tuple, V2: tuple, V3: tuple):
    #square root of area of triangle given by 3 vertices
    V12 = np.linalg.norm(V2-V1)
    V23 = np.linalg.norm(V3-V2)
    area = (V12*V23)/2
    return np.sqrt(area)

def D4(V1: tuple, V2: tuple, V3: tuple, V4: tuple):
    #cube root of volume of tetrahedron formed by 4 vertices
    #Cayley-Menger formula
    a = np.linalg.norm(V1-V2)
    b = np.linalg.norm(V1-V3)
    c = np.linalg.norm(V1-V4)
    d = np.linalg.norm(V2-V3)
    e = np.linalg.norm(V2-V4)
    f = np.linalg.norm(V3-V4)
    X = b**2 + c**2 - e**2
    Y = a**2 + c**2 - f**2
    Z = a**2 + b**2 - d**2
    Volume = np.sqrt(4*a**2*b**2*c**2 - a**2*X - b**2*Y - c**2*Z + X*Y*Z)/12
    return np.cbrt(Volume)
