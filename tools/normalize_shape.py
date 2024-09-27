import sys
import os
from vedo import load, write
from vedo import Mesh
import numpy as np
import tkinter as tk
from tkinter import filedialog
from find_barycenter import compute_barycenter

def normalize_shape(shape: Mesh) -> Mesh:
    # Position normalization
    barycenter = compute_barycenter(shape)
    shape.vertices = (shape.vertices - barycenter)

    # Rotation normalization
    points = shape.vertices
    cov_matrix = np.cov(points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    largest_eigenvector = eigenvectors[:, sorted_indices[0]]
    second_largest_eigenvector = eigenvectors[:, sorted_indices[1]]
    rotation_matrix = np.eye(3)
    rotation_matrix[:, 0] = largest_eigenvector
    rotation_matrix[:, 1] = second_largest_eigenvector
    rotation_matrix[:, 2] = np.cross(largest_eigenvector, second_largest_eigenvector)
    rotated_points = np.dot(points, rotation_matrix)
    shape.vertices = rotated_points

    # Flip
    moments = np.sum(rotated_points**2, axis=0)
    for i in range(3):
        if moments[i] < 0:
            rotated_points[:, i] = -rotated_points[:, i]
    shape.vertices = rotated_points

    # Scale normalization
    bounds = shape.bounds()
    max_bound = max([abs(bounds[1] - bounds[0]), abs(bounds[3] - bounds[2]), abs(bounds[5] - bounds[4])])
    shape.scale(1 / max_bound)

    return shape
                

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    objFile = filedialog.askopenfilename(initialdir = "../../ShapeDatabase_INFOMR_copy")
    shape = load(objFile)

    normalized_shape = normalize_shape(shape)
    write(normalized_shape, objFile)
