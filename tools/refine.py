import sys
import os
from pebble import ProcessPool
from concurrent.futures import TimeoutError
from vedo import load, write, Mesh

TARGET: int = 5000
TARGET_RANGE: int = 500

def decimate(shape: Mesh) -> Mesh:
    vertex_count = len(shape.vertices)
    while vertex_count > TARGET + TARGET_RANGE:
        shape = shape.decimate_binned(use_clustering=True)
        new_vertex_count = len(shape.vertices)
        if new_vertex_count == vertex_count:
            break
        vertex_count = new_vertex_count
    return shape

def subdivide(shape: Mesh) -> Mesh:
    vertex_count = len(shape.vertices)
    while vertex_count < TARGET - TARGET_RANGE:
        shape = shape.subdivide(n=1, method=2)
        new_vertex_count = len(shape.vertices)
        if new_vertex_count == vertex_count:
            break
        vertex_count = new_vertex_count
    return shape

def distribute_faces(shape: Mesh, passes: int) -> Mesh:
    for _ in range(passes):
        shape = shape.subdivide(n=2, method=2) # anything more takes way too long
        shape = decimate(shape)
    return shape

def refine_mesh(file_path: str, passes: int) -> None:
    model = load(file_path)

    vertex_count = len(model.vertices)
    if vertex_count < TARGET - TARGET_RANGE:
        refined_model = subdivide(model)
    elif vertex_count > TARGET + TARGET_RANGE:
        refined_model = decimate(model)
    else:
        refined_model = model
    refined_model = distribute_faces(refined_model, passes)
    write(refined_model, file_path)
    print(f"Refined {file_path}")

def main(path: str, passes: int) -> None:
    errors = []
    with ProcessPool() as pool:
        futures = {}
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.obj'):
                    full_path = os.path.join(root, file)
                    future = pool.schedule(refine_mesh, args=(full_path, passes), timeout=120)
                    futures[future] = full_path
        print("Processing files...")
        
        for future in futures:
            file_path = futures[future]
            try:
                future.result()
            except TimeoutError:
                print(f"A task took too long and was terminated. File: {file_path}")
                errors.append(f"A task took too long and was terminated. File: {file_path}")
            except Exception as e:
                print(f"An error occurred with file {file_path}: {e}")
                errors.append(f"An error occurred with file {file_path}: {e}")
        
        if errors:
            print("\nErrors encountered during processing:")
            for error in errors:
                print(error)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[2], int(sys.argv[1]))
    else:
        print("Please provide the number of passes and the path to the database")