from vedo import Mesh
import numpy as np

def check_translation(shape: Mesh) -> bool:
    barycenter = shape.center_of_mass()
    return barycenter == [0, 0, 0]

def check_rotation(shape: Mesh) -> bool:
    cov_matrix = np.cov(shape.vertices, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    largest_eigenvector = eigenvectors[:, sorted_indices[0]]
    return largest_eigenvector == [1, 0, 0]

def check_flip(shape: Mesh) -> bool:
    return True

def check_scaling(shape: Mesh) -> bool:
    bounds = shape.bounds()
    max_bound = max([abs(bounds[1] - bounds[0]), abs(bounds[3] - bounds[2]), abs(bounds[5] - bounds[4])])
    return max_bound == 1