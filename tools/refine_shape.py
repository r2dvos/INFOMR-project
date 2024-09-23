import sys
import os
from vedo import load, write, Mesh
import numpy as np
import tkinter as tk
from tkinter import filedialog

TARGET: int = 5000
TARGET_RANGE: int = 500

def decimate(shape: Mesh) -> Mesh:
    vertex_count = len(shape.vertices)
    while vertex_count > TARGET + TARGET_RANGE:
        shape = shape.decimate_binned(use_clustering=True)
        new_vertex_count = len(shape.vertices)
        print(f"Decimated to {new_vertex_count} vertices")
        if new_vertex_count == vertex_count:
            break
        vertex_count = new_vertex_count
    return shape

def subdivide(shape: Mesh, passes: int = 1) -> Mesh:
    for _ in range(passes):
        vertex_count = len(shape.vertices)
        while vertex_count < 4 * TARGET:
            print(f"Current vertex count: {vertex_count}")
            shape = shape.subdivide(n = 1, method = 2)
            new_vertex_count = len(shape.vertices)
            print(f"Subdivided to {new_vertex_count} vertices")
            if new_vertex_count == vertex_count:
                break
            vertex_count = new_vertex_count
        shape = decimate(shape)
    return shape

def main(objFile: str, passes: int) -> None:
    model = load(objFile)
    print(f"Loaded {objFile}")

    vertex_count = len(model.vertices)
    if vertex_count > TARGET + TARGET_RANGE:
        print("Decimating")
        refined_model = decimate(model)
    elif vertex_count < TARGET - TARGET_RANGE:
        print("Subdividing")
        refined_model = subdivide(model, passes)
    else:
        print("Skipping")
        refined_model = model
    write(refined_model, objFile)
    print(f"Refined {objFile}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    objFile = filedialog.askopenfilename(initialdir = "../ShapeDatabase_INFOMR_copy")
    main(objFile, int(sys.argv[1]))
