"""
modified from trimesh.remesh, only subdivide the longest edge
"""
import trimesh
import vedo
import vedo.mesh

def decimate_trimesh(file_path: str, target: int) -> None:
    mesh: trimesh.Trimesh = trimesh.load(file_path)
    while len(mesh.vertices) > target:
        mesh = mesh.simplify_quadric_decimation(percent = 0.2, aggression=4)
    mesh.export(file_path)

def decimate(file_path: str, target: int) -> None:
    mesh: vedo.Mesh = vedo.load(file_path)
    loops = 0.0
    last_vert = len(mesh.vertices)
    while len(mesh.vertices) > target:
        mesh = mesh.decimate(fraction = 0.9, regularization=0.05)
        loops = loops + 1.0
        if last_vert - len(mesh.vertices) < 10 * loops:
            break
        last_vert = len(mesh.vertices)
    vedo.write(mesh, file_path)

def subdivide(file_path: str, target: int) -> None:
    mesh: trimesh.Trimesh = trimesh.load(file_path)
    while len(mesh.vertices) < target:
        mesh = mesh.subdivide()
    mesh.export(file_path)

def distribute_faces(file_path: str, passes: int, lower_target: int, upper_target: int) -> None:
    for _ in range(passes):
        subdivide(file_path, lower_target * 4)
        decimate(file_path, upper_target)

def refine_mesh(file_path: str, passes: int, lower_target: int, upper_target: int) -> None:
    mesh = trimesh.load(file_path)
    vertex_count = len(mesh.vertices)
    loops = 0
    total_loops = 0
    extra_ranges = 0
    extra_range_length = (upper_target - lower_target)/4
    while vertex_count < lower_target - (extra_range_length*extra_ranges) or vertex_count > upper_target + (extra_range_length*extra_ranges):
        if vertex_count < lower_target - (extra_range_length*extra_ranges):
            subdivide(file_path, lower_target - (extra_range_length*extra_ranges))
        if vertex_count > upper_target + (extra_range_length*extra_ranges):
            decimate(file_path, upper_target + (extra_range_length*extra_ranges))

        mesh = trimesh.load(file_path)
        vertex_count = len(mesh.vertices)
        loops = loops + 1
        total_loops = total_loops + 1
        if loops >= 5:
            extra_ranges = extra_ranges + 1
            loops = 0

    distribute_faces(file_path, passes, lower_target, upper_target)
    print(f"Refined mesh saved to {file_path} in {loops} loops")

def final_decimate(file_path: str, passes: int, lower_target: int, upper_target: int) -> None:
    mesh = trimesh.load(file_path)
    if len(mesh.vertices) > upper_target:
        decimate_trimesh(file_path, upper_target)
        print(f"Final decimation saved to {file_path}")
    else:
        print(f"Mesh already within target range. Skipping final decimation for {file_path}")
