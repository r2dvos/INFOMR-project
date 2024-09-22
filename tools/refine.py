import sys
import os
from vedo import load, write, Mesh
import numpy as np

TARGET: int = 5000
TARGET_RANGE: int = 500

def decimate(shape: Mesh) -> Mesh:
    vertex_count = len(shape.vertices)
    while vertex_count > TARGET + TARGET_RANGE:
        shape = shape.decimate(fraction = 0.8, regularization=0.05)
        vertex_count = len(shape.vertices)
    return shape

def subdivide(shape: Mesh, passes: int = 1) -> Mesh:
    for _ in range(passes):
        vertex_count = len(shape.vertices)
        n = int(np.ceil(np.log(4 * TARGET / vertex_count) / np.log(4)))
        shape = shape.subdivide(n = n, method = 2)
        shape = decimate(shape)
    return shape

def main(path: str, passes: int) -> None:
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.obj'):
                full_path = os.path.join(root, file)
                model = load(full_path)

                vertex_count = len(model.vertices)
                if vertex_count > TARGET + TARGET_RANGE:
                    refined_model = decimate(model)
                elif vertex_count < TARGET - TARGET_RANGE:
                    refined_model = subdivide(model, passes)
                else:
                    refined_model = model
                write(refined_model, full_path)
                print(f"Refined {full_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[2], int(sys.argv[1]))
    else:
        print("Please provide a path to the database")