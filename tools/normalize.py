import sys
import os
from vedo import load, write
from vedo import Mesh
import numpy as np

def normalize_shape(shape: Mesh) -> Mesh:
    # Position normalization
    barycenter = shape.center_of_mass()
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

def main(path: str) -> None:
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.obj'):
                full_path = os.path.join(root, file)
                shape = load(full_path)
                normalized_shape = normalize_shape(shape)
                write(normalized_shape, full_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide a path to the database")