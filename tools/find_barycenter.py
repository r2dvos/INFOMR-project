import sys
import os
from vedo import load, write, show
from vedo import Mesh, Sphere, Spheres
import numpy as np

def compute_barycenter(shape: Mesh):
    faces = shape.cells
    vertices = shape.vertices
    cell_centers = shape.cell_centers
    for face in faces:
        point_array = np.array
        for point_id in face:
            point_array.append(vertices[point_id])
        A = point_array[0]
        B = point_array[1]
        C = point_array[2]
        AB = np.linalg.norm(A-B)
        AC = np.linalg.norm(A-C)


def main(path: str) -> None:
    shape = load(path)
    # barycenter = compute_barycenter(shape)
    #cell_centers = shape.cell_centers
    testball = Sphere( r=0.01)
    show(shape, testball)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide a path to an object")