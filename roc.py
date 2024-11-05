import pandas as pd
import matplotlib.pyplot as plt

def plot_sensitivity_vs_specificity(sensitivity, specificity, class_label):
    plt.figure(figsize=(10, 6))
    plt.plot(sensitivity, specificity)
    plt.xlabel('Sensitivity')
    plt.ylabel('Specificity')
    plt.title(f'Sensitivity vs Specificity for Class {class_label}')
    plt.xlim(0, 1)
    plt.ylim(0.9, 1)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    df = pd.read_csv('database.csv')
    class_counts = df['Class'].value_counts().to_dict()
    d = df.shape[0]

    data = pd.read_csv("results_normal_tau.txt", sep=';', header=None)
    data.columns = ['Class'] + [f'Tau_{i+1}' for i in range(data.shape[1] - 1)]

    class_sensitivity_specificity = {}
    for tau in range(1, 101):
        for index, row in data.iterrows():
            cls = row['Class']
            tp = row[f'Tau_{tau}']
            c = class_counts[cls]
            tn = d - c - (tau - tp)
            sensitivity = tp / c
            specificity = tn / (d - c)
            if cls not in class_sensitivity_specificity:
                class_sensitivity_specificity[cls] = {'sensitivity': [0]*100, 'specificity': [0]*100, 'count': [0]*100}
            class_sensitivity_specificity[cls]['sensitivity'][tau-1] += sensitivity
            class_sensitivity_specificity[cls]['specificity'][tau-1] += specificity
            class_sensitivity_specificity[cls]['count'][tau-1] += 1

    for cls, values in class_sensitivity_specificity.items():
        avg_sensitivity = [values['sensitivity'][i] / values['count'][i] if values['count'][i] != 0 else 0 for i in range(100)]
        avg_specificity = [values['specificity'][i] / values['count'][i] if values['count'][i] != 0 else 0 for i in range(100)]
        plot_sensitivity_vs_specificity(avg_sensitivity, avg_specificity, cls)