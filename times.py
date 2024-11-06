import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data = pd.read_csv("results_time.txt", sep=';', header=None, usecols=[0, 1, 2, 3])
    data.columns = ['Class', 'File', 'Time Knn', 'Time Normal']

    data_mean = data[['Class', 'Time Knn', 'Time Normal']].groupby('Class', as_index=False).mean()

    plt.figure(figsize=(10, 5))

    plt.plot(data_mean['Class'], data_mean['Time Normal'], label='Our Method', marker='x')
    plt.plot(data_mean['Class'], data_mean['Time Knn'], label='KNN', marker='o')

    plt.xlabel('Class')
    plt.ylabel('Mean Time Taken (seconds)')
    plt.title('Mean Time Taken by Class')
    plt.xticks(rotation=45, ha='right', fontsize=5)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
