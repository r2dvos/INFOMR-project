import sys
import os
import multiprocessing as mp
import time
from manipulations import refine_mesh, final_decimate, final_decimate_fallback

TARGET: int = 5000
TARGET_RANGE: int = 1000
DISTRIBUTION_SUBDIVISIONS: int = 3
BATCH_SIZE: int = 10

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

def main(path: str, passes: int) -> None:
    refine_pass(refine_mesh, path, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE)
    refine_pass(final_decimate, path, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE)
    refine_pass(final_decimate_fallback, path, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[2], int(sys.argv[1]))
    else:
        print("Please provide the number of passes and the path to the database")

