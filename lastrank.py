import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":

    data_knn = pd.read_csv("results_knn_lastrank.txt", sep=';', header=None, usecols=[0, 1, 2])
    data_knn.columns = ['Class', 'File', 'Last Rank']

    data_normal = pd.read_csv("results_normal_lastrank.txt", sep=';', header=None, usecols=[0, 1, 2])
    data_normal.columns = ['Class', 'File', 'Last Rank']

    data_ideal = data_normal.copy()
    data_ideal['Last Rank'] = data_ideal.groupby('Class')['Class'].transform('count')

    data_knn_mean = data_knn[['Class', 'Last Rank']].groupby('Class', as_index=False).mean()
    data_normal_mean = data_normal[['Class', 'Last Rank']].groupby('Class', as_index=False).mean()
    data_ideal_mean = data_ideal[['Class', 'Last Rank']].groupby('Class', as_index=False).mean()

    plt.figure(figsize=(10, 5))

    plt.plot(data_knn_mean['Class'], data_knn_mean['Last Rank'], label='KNN', marker='o')
    plt.plot(data_normal_mean['Class'], data_normal_mean['Last Rank'], label='Normal', marker='x')
    plt.plot(data_ideal_mean['Class'], data_ideal_mean['Last Rank'], label='Ideal', marker='^')

    plt.xlabel('Class')
    plt.ylabel('Mean Last Rank')
    plt.title('Mean Last Rank by Class')
    plt.xticks(rotation=45, ha='right', fontsize=5)
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
