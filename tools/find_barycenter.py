import sys
import os
from vedo import load, write, show
from vedo import Mesh, Sphere, Spheres
import numpy as np
import tkinter as tk
from tkinter import filedialog

def compute_barycenter(shape: Mesh):
    faces = shape.cells
    vertices = shape.vertices
    cell_centers = shape.cell_centers
    count = 0
    point_total = [0, 0, 0]
    for face in faces:
        point_array = []
        for point_id in face:
            point_array.append(vertices[point_id])
        A = point_array[0]
        B = point_array[1]
        C = point_array[2]
        AB = np.linalg.norm(A-B)
        AC = np.linalg.norm(A-C)
        area = (AB*AC)/2
        point_total[0] = point_total[0] + cell_centers[count][0] * area
        point_total[1] = point_total[1] + cell_centers[count][1] * area
        point_total[2] = point_total[2] + cell_centers[count][2] * area
        count = count + 1
    barycenter = [point_total[0]/count, point_total[1]/count, point_total[2]/count]
    return barycenter


def main(objFile: str) -> None:
    shape = load(objFile)
    barycenter = compute_barycenter(shape)
    print(barycenter)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    objFile = filedialog.askopenfilename(initialdir = "../../ShapeDatabase_INFOMR_copy")
    main(objFile)
