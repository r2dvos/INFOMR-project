import sys
import os
from vedo import load, write
from vedo import Mesh
import numpy as np
import tkinter as tk
from tkinter import filedialog

def compute_barycenter(faces: np.ndarray, vertices: np.ndarray, cell_centers: np.ndarray):
    count = 0
    count_total = 0
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
        count_total = count_total + area
    barycenter = [point_total[0]/count_total, point_total[1]/count_total, point_total[2]/count_total]
    return barycenter

def compute_eigenvectors(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    cov_matrix = np.cov(points, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    sorted_indices = np.argsort(eigenvalues)[::-1]
    largest_eigenvector = eigenvectors[:, sorted_indices[0]]
    second_largest_eigenvector = eigenvectors[:, sorted_indices[1]]
    largest_eigenvalue = eigenvalues[sorted_indices[0]]
    second_largest_eigenvalue = eigenvalues[sorted_indices[1]]
    return (largest_eigenvector, second_largest_eigenvector, largest_eigenvalue, second_largest_eigenvalue)

def compute_flip(points: np.ndarray) -> list[int]:
    moment_x = 0
    moment_y = 0
    moment_z = 0
    for i in range(len(points)):
        moment_x = moment_x + np.sign(points[i][0]) * (points[i][0]**2)
        moment_y = moment_y + np.sign(points[i][1]) * (points[i][1]**2)
        moment_z = moment_z + np.sign(points[i][2]) * (points[i][2]**2)

    moments = [moment_x, moment_y, moment_z]
    for i in range(3):
        if moments[i] < 0:
            moments[i] = -1
        else:
            moments[i] = 1
    return moments

def compute_scaling(bounds: np.ndarray) -> float:
    max_bound = max([abs(bounds[1] - bounds[0]), abs(bounds[3] - bounds[2]), abs(bounds[5] - bounds[4])])
    return max_bound

def normalize_shape(shape: Mesh) -> Mesh:
    # Position normalization
    barycenter = compute_barycenter(shape.cells, shape.vertices, shape.cell_centers)
    shape.vertices = (shape.vertices - barycenter)

    # Rotation normalization
    points = shape.vertices
    (largest_eigenvector, second_largest_eigenvector, _, _) = compute_eigenvectors(shape.vertices)
    rotation_matrix = np.eye(3)
    rotation_matrix[:, 0] = largest_eigenvector
    rotation_matrix[:, 1] = second_largest_eigenvector
    rotation_matrix[:, 2] = np.cross(largest_eigenvector, second_largest_eigenvector)
    rotated_points = np.dot(points, rotation_matrix)
    shape.vertices = rotated_points

    # Flip
    (moment_x, moment_y, moment_z) = compute_flip(shape.vertices)
    flip_table = [[np.sign(moment_x), 0, 0], [0, np.sign(moment_y), 0], [0, 0, np.sign(moment_z)]]
    fliped_points = np.dot(rotated_points,flip_table)
    shape.vertices = fliped_points

    # Scale normalization
    max_bound = compute_scaling(shape.bounds())
    shape.scale(1 / max_bound)

    return shape

if __name__ == "__main__":
    help = "Usage:\n-f: Normalize a single file\n-a: Normalize all files in a directory. Arg: dir path\n-b: Compute barycenter of a single file\n-h: Display this help message"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print(help)
        sys.exit()

    if mode == "-f":
        root = tk.Tk()
        root.withdraw()

        objFile = filedialog.askopenfilename(initialdir = "../../ShapeDatabase_INFOMR_copy")
        shape = load(objFile)

        normalized_shape = normalize_shape(shape)
        write(normalized_shape, objFile)
    elif mode == "-a" and len(sys.argv) > 2:
        for root, _, files in os.walk(sys.argv[2]):
            for file in files:
                if file.endswith('.obj'):
                    full_path = os.path.join(root, file)
                    shape = load(full_path)
                    normalized_shape = normalize_shape(shape)
                    print("Normalized shape " + full_path)
                    write(normalized_shape, full_path)
    elif mode == "-b":
        root = tk.Tk()
        root.withdraw()
        objFile = filedialog.askopenfilename(initialdir = "../../ShapeDatabase_INFOMR_copy")
        print(compute_barycenter(load(objFile)))
    else:
        print(help)
