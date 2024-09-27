import sys
import os
import multiprocessing as mp
from manipulations import refine_mesh, final_decimate

TARGET: int = 5000
TARGET_RANGE: int = 1000
DISTRIBUTION_SUBDIVISIONS: int = 3
BATCH_SIZE: int = 10

def refine_pass(function, path: str, passes: int, lower: int, upper: int) -> None:
    max_duration = 120
    errors = []
    processes = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.obj'):
                full_path = os.path.join(root, file)
                process = mp.Process(name=full_path, target=function, args=(full_path, passes, lower, upper))
                processes.append(process)

    for i in range(0, len(processes), BATCH_SIZE):
        batch = processes[i:i + BATCH_SIZE]
        for process in batch:
            process.start()

        for process in batch:
            process.join(timeout=max_duration + 0.01)
            if process.is_alive():
                process.terminate()
                print(f"A task took too long and was terminated. File: {process.name}")
                errors.append(f"A task took too long and was terminated. File: {process.name}")

    if errors:
        print("\nErrors encountered during processing:")
        for error in errors:
            print(error)

def main(path: str, passes: int) -> None:
    refine_pass(refine_mesh, path, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE)
    refine_pass(final_decimate, path, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE * 2)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[2], int(sys.argv[1]))
    else:
        print("Please provide the number of passes and the path to the database")

