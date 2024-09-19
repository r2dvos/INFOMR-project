import sys
import os
from vedo import load, write, Mesh

TARGET: int = 5000
TARGET_RANGE: int = 500

def decimate(shape: Mesh) -> Mesh:
    vertex_count = len(shape.vertices)
    while vertex_count > TARGET + TARGET_RANGE:
        shape = shape.decimate(0.9)
        vertex_count = len(shape.vertices)
    return shape

def subdivide(shape: Mesh) -> Mesh:
    vertex_count = len(shape.vertices)
    while vertex_count < TARGET - TARGET_RANGE:
        shape = shape.subdivide(n = 1, method = 4)
        vertex_count = len(shape.vertices)
    #return decimate(shape)
    return shape

def main(path: str) -> None:
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.obj'):
                full_path = os.path.join(root, file)
                model = load(full_path)

                vertex_count = len(model.vertices)
                if vertex_count > TARGET + TARGET_RANGE:
                    refined_model = decimate(model)
                elif vertex_count < TARGET - TARGET_RANGE:
                    refined_model = subdivide(model)
                else:
                    refined_model = model
                write(refined_model, full_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide a path to the database")