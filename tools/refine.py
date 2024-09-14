import sys
import os
import trimesh

LOWER_LIMIT = 100

def main(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.obj'):
                full_path = os.path.join(root, file)
                model = trimesh.load(full_path)
                
                vertex_count = len(model.vertices)
                face_count = len(model.faces)
                if vertex_count < LOWER_LIMIT or face_count < LOWER_LIMIT:
                    refined_model = model.subdivide()
                    refined_model.export(full_path)
                    print(f"Refined {full_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide a path to the database")