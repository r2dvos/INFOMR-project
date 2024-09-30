import pip
import numpy as np

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

from vedo import Mesh, load
import numpy as np

# Two kinds of functions: gets & checks
# - gets: returns value of function for plotting
# - checks: returns error of function

#~~

def get_translation(shape: Mesh):
    barycenter = shape.center_of_mass()
    return barycenter

def check_translation(shape: Mesh):
    barycenter = shape.center_of_mass()
    return abs(barycenter[0] ** 3) + abs(barycenter[1] ** 3) + abs(barycenter[2] ** 3)

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
    return (largest_eigenvector[0] - 1) + largest_eigenvector[1] + largest_eigenvector[2]

#~~

def get_flip(shape: Mesh):
    points = shape.vertices

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

def check_flip(shape: Mesh):
    points = shape.vertices

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

#
#~~~~~~~~~
#

def get_shape_class(file_path: str) -> str:
    return os.path.basename(os.path.dirname(file_path))

def write_normals(path: str, output_csv: str) -> None:
    results = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.obj'):
                print("analyzing " + file)
                full_path = os.path.join(root, file)

                shape_class = get_shape_class(full_path)
                shape = load(full_path)

                barycenter = get_translation(shape)
                barycenter_err = check_translation(shape)
                rotation = get_rotation(shape)
                rotation_err = check_rotation(shape)
                flip = get_flip(shape)
                flip_err = check_flip(shape)
                scaling = get_scaling(shape)
                scaling_err = check_scaling(shape)
                
                results.append([
                    file, shape_class, barycenter, barycenter_err, rotation,
                    rotation_err, flip, flip_err, scaling, scaling_err
                ])
    
    results_array = np.array(results, dtype=object)
    
    columns = [
        "File Name", "Class", "Barycenter", "Barycenter Error", "Rotation",
        "Rotation Error", "Flip", "Flip Error", "Scaling", "Scaling Error"
    ]
    df = pd.DataFrame(results_array, columns=columns)
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

    get_normals(output_csv)

def get_normals(input_csv: str) -> None:
    df = pd.read_csv(input_csv)

    # Barycenter

    avg_barycenter_error = df["Barycenter Error"].astype(int).mean()
    print(f"Average barycenter error: {avg_barycenter_error}" + "\n")

    greatest_barycenter_error = df.nlargest(5, ['Barycenter Error'], keep='first')[['Class', 'File Name', 'Barycenter', 'Barycenter Error']]
    print("Shapes with greatest barycenter error:\n" + str(greatest_barycenter_error) + "\n")

    print("~~\n")

    plt.hist(df['Barycenter Error'], bins=20)
    plt.title("Barycenter Error")
    plt.xlabel("Error")
    plt.ylabel("Shapes")
    plt.show()

    # Rotation

    avg_rotation_error = df["Rotation Error"].astype(int).mean()
    print(f"Average rotation error: {avg_rotation_error}" + "\n")

    greatest_rotation_error = df.nlargest(5, ['Rotation Error'], keep='first')[['Class', 'File Name', 'Rotation', 'Rotation Error']]
    print("Shapes with greatest rotation error:\n" + str(greatest_rotation_error) + "\n")

    print("~~\n")

    plt.hist(df['Rotation Error'], bins=20)
    plt.title("Rotation Error")
    plt.xlabel("Error")
    plt.ylabel("Shapes")
    plt.show()

    # Flip

    avg_flip_error = df["Flip Error"].astype(int).mean()
    print(f"Average flip error: {avg_flip_error}" + "\n")

    greatest_flip_error = df.nlargest(5, ['Flip Error'], keep='first')[['Class', 'File Name', 'Flip', 'Flip Error']]
    print("Shapes with greatest flip error:\n" + str(greatest_flip_error) + "\n")

    print("~~\n")

    plt.hist(df['Flip Error'], bins=20)
    plt.title("Flip Error")
    plt.xlabel("Error")
    plt.ylabel("Shapes")
    plt.show()

    # Scaling

    avg_scaling_error = df["Scaling Error"].astype(int).mean()
    print(f"Average scaling error: {avg_scaling_error}" + "\n")

    greatest_scaling_error = df.nlargest(5, ['Scaling Error'], keep='first')[['Class', 'File Name', 'Scaling', 'Scaling Error']]
    print("Shapes with greatest scaling error:\n" + str(greatest_scaling_error) + "\n")

    print("~~\n")

    plt.hist(df['Scaling Error'], bins=20)
    plt.title("Scaling Error")
    plt.xlabel("Error")
    plt.ylabel("Shapes")
    plt.show()

#
#~~~~~~~~~
#

if __name__ == "__main__":
    if len(sys.argv) == 2:
        get_normals(sys.argv[1])
    elif len(sys.argv) > 2:
        write_normals(sys.argv[1], sys.argv[2])
    else:
        print("Please provide: \n 1 - a csv file to read data from or \n 2 - a path to the database and an output CSV file name")
