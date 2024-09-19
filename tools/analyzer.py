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
                print("analyzing " + file)
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

    analyze(output_csv)
    
    # ~~

def analyze(input_csv: str) -> None:
    df = pd.read_csv(input_csv)

    # Vertices

    smallest_vertice_count = df.nsmallest(3, ['Number of Vertices'], keep='first')[['Class', 'File Name', 'Number of Vertices', 'Number of Faces']]
    print("Shapes with smallest Vertex count:\n" + str(smallest_vertice_count) + "\n")

    largest_vertice_count = df.nlargest(3, ['Number of Vertices'], keep='first')[['Class', 'File Name', 'Number of Vertices', 'Number of Faces']]
    print("Shapes with largest Vertex count:\n" + str(largest_vertice_count) + "\n")

    avg_vertices = df["Number of Vertices"].astype(int).mean()
    print(f"Average number of vertices: {avg_vertices}" + "\n")

    avg_vertice_shapes = df.iloc[(df['Number of Vertices']-avg_vertices).abs().argsort()[:2]][['Class', 'File Name', 'Number of Vertices', 'Number of Faces']]
    print("Shapes with most average Vertex count:\n" + str(avg_vertice_shapes) + "\n")

    print("~~\n")

    # Faces

    smallest_face_count = df.nsmallest(3, ['Number of Faces'], keep='first')[['Class', 'File Name', 'Number of Vertices', 'Number of Faces']]
    print("Shapes with smallest Face count:\n" + str(smallest_face_count) + "\n")

    largest_face_count = df.nlargest(3, ['Number of Faces'], keep='first')[['Class', 'File Name', 'Number of Vertices', 'Number of Faces']]
    print("Shapes with largest Face count:\n" + str(largest_face_count) + "\n")

    avg_faces = df["Number of Faces"].astype(int).mean()
    print(f"Average number of faces: {avg_faces}" + "\n")

    avg_faces_shapes = df.iloc[(df['Number of Faces']-avg_faces).abs().argsort()[:2]][['Class', 'File Name', 'Number of Vertices', 'Number of Faces']]
    print("Shapes with most average Face count:\n" + str(avg_faces_shapes) + "\n")

    print("~~\n")

    # Bounding Boxes

    print("Bounding Box Calculations:\n")

    print("Corner Xmin")
    avg_Xmin = df["Bounding Box Xmin"].astype(float).mean()
    print(f"Average Xmin: {avg_Xmin}")
    max_Xmin_error = max(df["Bounding Box Xmin"].astype(float).max() - avg_Xmin, df["Bounding Box Xmin"].astype(float).min() - avg_Xmin)
    print(f"Max error from average Xmin: {max_Xmin_error}\n")

    print("Corner Xmax")
    avg_Xmax = df["Bounding Box Xmax"].astype(float).mean()
    print(f"Average Xmax: {avg_Xmax}")
    max_Xmax_error = max(df["Bounding Box Xmax"].astype(float).max() - avg_Xmax, df["Bounding Box Xmax"].astype(float).min() - avg_Xmax)
    print(f"Max error from average Xmax: {max_Xmax_error}\n")

    print("Corner Ymin")
    avg_Ymin = df["Bounding Box Ymin"].astype(float).mean()
    print(f"Average Ymin: {avg_Ymin}")
    max_Ymin_error = max(df["Bounding Box Ymin"].astype(float).max() - avg_Ymin, df["Bounding Box Ymin"].astype(float).min() - avg_Ymin)
    print(f"Max error from average Ymin: {max_Ymin_error}\n")

    print("Corner Ymax")
    avg_Ymax = df["Bounding Box Ymax"].astype(float).mean()
    print(f"Average Ymax: {avg_Ymax}")
    max_Ymax_error = max(df["Bounding Box Ymax"].astype(float).max() - avg_Ymax, df["Bounding Box Ymax"].astype(float).min() - avg_Ymax)
    print(f"Max error from average Ymax: {max_Ymax_error}\n")

    print("Corner Zmin")
    avg_Zmin = df["Bounding Box Zmin"].astype(float).mean()
    print(f"Average Zmin: {avg_Zmin}")
    max_Zmin_error = max(df["Bounding Box Zmin"].astype(float).max() - avg_Zmin, df["Bounding Box Zmin"].astype(float).min() - avg_Zmin)
    print(f"Max error from average Zmin: {max_Zmin_error}\n")

    print("Corner Zmax")
    avg_Zmax = df["Bounding Box Zmax"].astype(float).mean()
    print(f"Average Zmax: {avg_Zmax}")
    max_Zmax_error = max(df["Bounding Box Zmax"].astype(float).max() - avg_Zmax, df["Bounding Box Zmax"].astype(float).min() - avg_Zmax)
    print(f"Max error from average Zmax: {max_Zmax_error}\n")

    # ~~

if __name__ == "__main__":
    if len(sys.argv) == 2:
        analyze(sys.argv[1])
    elif len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Please provide: \n 1 - a csv file to read data from or \n 2 - a path to the database and an output CSV file name")
