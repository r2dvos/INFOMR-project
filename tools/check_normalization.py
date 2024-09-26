from vedo import Mesh
import numpy as np

# Two kinds of functions: gets & checks
# - gets: returns value of function for plotting
# - checks: returns error of function

#~~

def get_translation(shape: Mesh)
    barycenter = shape.center_of_mass()
    return barycenter

def check_translation(shape: Mesh):
    barycenter = shape.center_of_mass()
    return (barycenter[0] ** 3) + (barycenter[1] ** 3) + (barycenter[2] ** 3)

#~~

def get_rotation(shape: Mesh):
    cov_matrix = np.cov(shape.vertices, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    largest_eigenvector = eigenvectors[:, sorted_indices[0]]
    return largest_eigenvector

def check_rotation(shape: Mesh):
    cov_matrix = np.cov(shape.vertices, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    largest_eigenvector = eigenvectors[:, sorted_indices[0]]
    return ((largest_eigenvector[0] - 1)) + (largest_eigenvector[1]) + (largest_eigenvector[2])

#~~

def get_flip(shape: Mesh):
    points = shape.vertices ##
    moments = np.sum(points**2, axis=0)
    for i in range(3):
        if moments[i] < 0:
            moments[i] = -1
        else:
            moments[i] = 1
    return moments

def check_flip(shape: Mesh):
    points = shape.vertices ##
    moments = np.sum(points**2, axis=0)
    for i in range(3):
        if moments[i] < 0:
            moments[i] = -1
        else:
            moments[i] = 1
    return (-(moments[0] - 1) / 2) + (-(moments[1] - 1) / 2) + (-(moments[2] - 1) / 2)

#~~

def get_scaling(shape: Mesh):
    bounds = shape.bounds()
    max_bound = max([abs(bounds[1] - bounds[0]), abs(bounds[3] - bounds[2]), abs(bounds[5] - bounds[4])])
    return max_bound

def check_scaling(shape: Mesh):
    bounds = shape.bounds()
    max_bound = max([abs(bounds[1] - bounds[0]), abs(bounds[3] - bounds[2]), abs(bounds[5] - bounds[4])])
    return max_bound - 1
