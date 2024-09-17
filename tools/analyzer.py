import os
import numpy as np
import pandas as pd
import sys
from vedo import load

def get_shape_class(file_path: str) -> str:
    return os.path.basename(os.path.dirname(file_path))

def analyze_shape(file_path: str) -> tuple[int, int, str, list[float]]:
    shape = load(file_path)
    num_vertices = len(shape.vertices)
    num_faces = len(shape.cells)
    
    face_types = set(len(face) for face in shape.cells)
    if face_types == {3}:
        face_type = "Only triangles"
    elif face_types == {4}:
        face_type = "Only quads"
    else:
        face_type = "Mixed triangles and quads"
    
    bounding_box = shape.bounds()
    
    return num_vertices, num_faces, face_type, bounding_box

def main(path: str, output_csv: str) -> None:
    results = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.obj'):
                full_path = os.path.join(root, file)
                shape_class = get_shape_class(full_path)
                num_vertices, num_faces, face_type, bounding_box = analyze_shape(full_path)
                
                results.append([
                    file, shape_class, num_vertices, num_faces, face_type,
                    bounding_box[0], bounding_box[1], bounding_box[2],
                    bounding_box[3], bounding_box[4], bounding_box[5]
                ])
    
    results_array = np.array(results, dtype=object)
    
    columns = [
        "File Name", "Class", "Number of Vertices", "Number of Faces", "Face Type",
        "Bounding Box Xmin", "Bounding Box Xmax", "Bounding Box Ymin",
        "Bounding Box Ymax", "Bounding Box Zmin", "Bounding Box Zmax"
    ]
    df = pd.DataFrame(results_array, columns=columns)
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")
    
    avg_vertices = df["Number of Vertices"].astype(int).mean()
    avg_faces = df["Number of Faces"].astype(int).mean()
    print(f"Average number of vertices: {avg_vertices}")
    print(f"Average number of faces: {avg_faces}")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Please provide a path to the database and an output CSV file name")