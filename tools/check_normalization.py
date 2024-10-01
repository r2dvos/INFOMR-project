import numpy as np

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

from vedo import Mesh, load
import numpy as np
from normalization import compute_barycenter, compute_eigenvectors, compute_flip, compute_scaling


def check_translation(shape: Mesh):
    barycenter = compute_barycenter(shape)
    return abs(barycenter[0] ** 3) + abs(barycenter[1] ** 3) + abs(barycenter[2] ** 3)

def check_rotation(shape: Mesh):
    (largest_eigenvector, _) = compute_eigenvectors(shape)
    return (largest_eigenvector[0] - 1) + largest_eigenvector[1] + largest_eigenvector[2]

def check_flip(shape: Mesh):
    moments = compute_flip(shape)
    return (-(moments[0] - 1) / 2) + (-(moments[1] - 1) / 2) + (-(moments[2] - 1) / 2)

def check_scaling(shape: Mesh):
    max_bound = compute_scaling(shape)
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

                barycenter = compute_barycenter(shape)
                barycenter_err = check_translation(shape)
                rotation = compute_eigenvectors(shape)
                rotation_err = check_rotation(shape)
                flip = compute_flip(shape)
                flip_err = check_flip(shape)
                scaling = compute_scaling(shape)
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
