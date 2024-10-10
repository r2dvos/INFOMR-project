import sys
import math
from enum import IntEnum
import os
import subprocess

import trimesh
import tkinter as tk
from tkinter import filedialog
import pandas as pd

from normalization import compute_eigenvectors

class Features(IntEnum):
    SurfaceArea = 0
    Compactness = 1
    ThreeDRegularity = 2
    Diameter = 3
    Convexity = 4
    Eccentricity = 5

def compute_features(mesh: trimesh.Trimesh, path: str) -> list[float]:
    features = []
    
    area = mesh.area
    volume = mesh.volume

    # Surface Area
    features.append(float(area))
    
    # Compactness
    compactness = (area ** 2) / (4 * math.pi * volume)
    features.append(float(compactness))
    
    # 3D Regularity
    obb_volume = mesh.bounding_box_oriented.volume
    three_d_regularity = volume / obb_volume
    features.append(float(three_d_regularity))
    
    # Diameter
    # Check: https://sarielhp.org/research/papers/00/diameter/diam_prog.html
    # for more details on the algorithm used to compute the diameter
    result = subprocess.run(["gdiam_test.exe", path], capture_output=True)
    diameter = float(result.stdout.strip())
    features.append(diameter)

    # Convexity
    convex_hull_volume = mesh.convex_hull.volume
    convexity = volume / convex_hull_volume
    features.append(float(convexity))
    
    # Eccentricity
    (_, _, largest_eigenvalue, second_largest_eigenvalue) = compute_eigenvectors(mesh.vertices)
    features.append(float(largest_eigenvalue / second_largest_eigenvalue))
    
    return features

if __name__ == "__main__":
    help = "Usage:\n-f: Print features of a single shape\n-a: Create a csv with the feature of all shapes in a directory. Args: database path, out csv\n-h: Display this help message"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print(help)
        sys.exit()

    if mode == "-f":
        root = tk.Tk()
        root.withdraw()

        objFile = filedialog.askopenfilename(initialdir = "../../ShapeDatabase_INFOMR_copy")
        shape = trimesh.load(objFile)

        features = compute_features(shape, objFile)
        print(features)
    elif mode == "-a" and len(sys.argv) > 3:
        columns = ["Surface Area", "Compactness", "3D Regularity", "Diameter", "Convexity", "Eccentricity"]
        df = pd.DataFrame(columns=columns)
        for root, _, files in os.walk(sys.argv[2]):
            for file in files:
                if file.endswith('.obj'):
                    full_path = os.path.join(root, file)
                    shape = trimesh.load(full_path)
                    features = compute_features(shape, full_path)
                    df.loc[len(df)] = features
                    print(f"Features for {full_path} computed.")
        df.to_csv(sys.argv[3], index=False)
    else:
        print(help)