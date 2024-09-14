import sys
import os
from vedo import load, write

def normalize_shape(shape):
    barycenter = shape.center_of_mass()
    shape.vertices = (shape.vertices - barycenter)

    bounds = shape.bounds()
    max_bound = max([abs(bounds[1] - bounds[0]), abs(bounds[3] - bounds[2]), abs(bounds[5] - bounds[4])])
    shape.scale(1 / max_bound)
    return shape

def main(path):
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