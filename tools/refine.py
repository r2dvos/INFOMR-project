import sys
import os
import trimesh

LOWER_LIMIT = 100

def main(path: str) -> None:
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.obj'):
                full_path = os.path.join(root, file)
                model = trimesh.load(full_path)
                
                vertex_count = len(model.vertices)
                face_count = len(model.faces)
                refined_model = None
                while vertex_count < LOWER_LIMIT or face_count < LOWER_LIMIT:
                    refined_model = model.subdivide()
                    new_vertex_count = len(refined_model.vertices)
                    new_face_count = len(refined_model.faces)
                    if new_vertex_count == vertex_count or new_face_count == face_count:
                        break
                    vertex_count = new_vertex_count
                    face_count = new_face_count
                if refined_model is not None:
                    refined_model.export(full_path)
                    print(f"Refined {full_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please provide a path to the database")