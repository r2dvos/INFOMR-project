import sys
import os
import multiprocessing as mp
import time
from tkinter import filedialog
import tkinter as tk
import trimesh
import vedo
import vedo.mesh

TARGET: int = 5000
TARGET_RANGE: int = 1000
DISTRIBUTION_SUBDIVISIONS: int = 3
BATCH_SIZE: int = 10

def decimate_trimesh(file_path: str, target: int) -> None:
    mesh: trimesh.Trimesh = trimesh.load(file_path)
    while len(mesh.vertices) > target:
        mesh = mesh.simplify_quadric_decimation(percent = 0.2, aggression=4)
    mesh.export(file_path)

def decimate_binned(file_path: str, target: int) -> None:
    mesh: vedo.Mesh = vedo.load(file_path)
    while len(mesh.vertices) > target:
        mesh = mesh.decimate_binned(use_clustering=True)
    vedo.write(mesh, file_path)

def decimate(file_path: str, target: int) -> None:
    mesh: vedo.Mesh = vedo.load(file_path)
    loops = 0.0
    last_vert = len(mesh.vertices)
    while len(mesh.vertices) > target:
        mesh = mesh.decimate(fraction = 0.9, preserve_volume=False, regularization=0.05)
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

def final_decimate_fallback(file_path: str, passes: int, lower_target: int, upper_target: int) -> None:
    mesh = vedo.load(file_path)
    if len(mesh.vertices) > upper_target:
        decimate_binned(file_path, upper_target)
        mesh = vedo.load(file_path)
        if len(mesh.vertices) < lower_target:
            distribute_faces(file_path, passes, lower_target, upper_target)
        print(f"Final decimation fallback saved to {file_path}")
    else:
        print(f"Mesh already within target range. Skipping final decimation fallback for {file_path}")

def refine_pass(function, path: str, passes: int, lower: int, upper: int) -> None:
    max_duration = 60
    errors = []
    tasks = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.obj'):
                full_path = os.path.join(root, file)
                tasks.append((full_path, passes, lower, upper))

    active_processes = []

    while tasks or active_processes:
        while tasks and len(active_processes) < BATCH_SIZE:
            task = tasks.pop(0)
            full_path, passes, lower, upper = task
            process = mp.Process(name=full_path, target=function, args=(full_path, passes, lower, upper))
            process.start()
            start_time = time.time()
            active_processes.append((process, full_path, start_time))

        for process, full_path, start_time in active_processes[:]:
            process.join(timeout=0.1)
            if not process.is_alive():
                active_processes.remove((process, full_path, start_time))
                if process.exitcode != 0:
                    print(f"Process for {full_path} exited with errors.")
                    errors.append(f"Process for {full_path} exited with errors. Error code: {process.exitcode}")
            else:
                elapsed_time = time.time() - start_time
                if elapsed_time > max_duration:
                    process.terminate()
                    active_processes.remove((process, full_path, start_time))
                    print(f"A task took too long and was terminated. File: {process.name}")
                    errors.append(f"A task took too long and was terminated. File: {process.name}")

    if errors:
        print("Errors occurred during processing:")
        for error in errors:
            print(error)

if __name__ == "__main__":
    help = "Usage:\n-f: Refine a single file\n-a: Refine all files in a directory. Arg: dir path\n-h: Display this help message"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        print(help)
        sys.exit()

    if mode == "-f" and len(sys.argv) > 2:
        root = tk.Tk()
        root.withdraw()

        objFile = filedialog.askopenfilename(initialdir = "../../ShapeDatabase_INFOMR_copy")
        passes = int(sys.argv[2])
        refine_mesh(objFile, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE)
    elif mode == "-a" and len(sys.argv) > 3:
        passes = int(sys.argv[2])
        path = sys.argv[3]
        refine_pass(refine_mesh, path, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE)
        refine_pass(final_decimate, path, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE)
        refine_pass(final_decimate_fallback, path, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE)
    else:
        print(help)
