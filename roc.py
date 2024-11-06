import pandas as pd
import matplotlib.pyplot as plt

def plot_sensitivity_vs_specificity(sensitivity_knn, specificity_knn, sensitivity_normal, specificity_normal, class_label):
    plt.figure(figsize=(10, 6))
    plt.plot(sensitivity_knn, specificity_knn)
    plt.plot(sensitivity_normal, specificity_normal)
    plt.xlabel('Sensitivity')
    plt.ylabel('Specificity')
    plt.title(f'ROC for {class_label}')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend(['KNN', 'Our Method'])
    plt.show()

def calculate_sensitivity_specificity(data, class_counts, d):
    sensitivities = []
    specificities = []
    for tau in range(1, 2485):
        sensitivity = 0.0
        specificity = 0.0
        count = 0
        for index, row in data.iterrows():
            cls = row['Class']
            tp = row[f'Tau_{tau}']
            c = class_counts[cls]
            tn = d - c - (tau - tp)
            sensitivity = sensitivity + tp / c
            specificity = specificity + tn / (d - c)
            count = count + 1
        sensitivities.append(sensitivity/count)
        specificities.append(specificity/count)
        print(f'calculated tau {tau}')
    return sensitivities, specificities

if __name__ == "__main__":
    df = pd.read_csv('database.csv')
    class_counts = df['Class'].value_counts().to_dict()
    d = df.shape[0]

    data_knn = pd.read_csv("results_knn_tau.txt", sep=';', header=None)
    data_knn.columns = ['Class'] + [f'Tau_{i+1}' for i in range(data_knn.shape[1] - 1)]

    data_normal = pd.read_csv("results_normal_tau.txt", sep=';', header=None)
    data_normal.columns = ['Class'] + [f'Tau_{i+1}' for i in range(data_normal.shape[1] - 1)]

    sensitivities_knn, specificities_knn = calculate_sensitivity_specificity(data_knn, class_counts, d)
    sensitivities_normal, specificities_normal = calculate_sensitivity_specificity(data_normal, class_counts, d)

    plot_sensitivity_vs_specificity(sensitivities_knn, specificities_knn, sensitivities_normal, specificities_normal, "Entire DB")