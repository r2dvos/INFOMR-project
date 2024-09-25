import sys
import os
import multiprocessing as mp
from manipulations import refine_mesh

TARGET: int = 5000
TARGET_RANGE: int = 500
DISTRIBUTION_SUBDIVISIONS: int = 3

def main(path: str, passes: int) -> None:
    max_duration = 120
    errors = []

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.obj'):
                full_path = os.path.join(root, file)
                process = mp.Process(target=refine_mesh, args=(full_path, passes, TARGET - TARGET_RANGE, TARGET + TARGET_RANGE))
                process.start()
                process.join(timeout=max_duration + 0.01)

                if process.is_alive():
                    process.terminate()
                    print(f"A task took too long and was terminated. File: {full_path}")
                    errors.append(f"A task took too long and was terminated. File: {full_path}")

    if errors:
        print("\nErrors encountered during processing:")
        for error in errors:
            print(error)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[2], int(sys.argv[1]))
    else:
        print("Please provide the number of passes and the path to the database")
