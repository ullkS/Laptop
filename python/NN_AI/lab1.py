import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA

# Загрузка датасета Iris
iris = datasets.load_iris()
X = iris.data[:, [2, 3]]  # длина и ширина лепестка
y = iris.target

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Создание и обучение персептрона
ppn = Perceptron(max_iter=40, eta0=0.1, random_state=42)
ppn.fit(X_train, y_train)

# Предсказание на тестовой выборке
y_pred = ppn.predict(X_test)

# Вычисление точности
accuracy = accuracy_score(y_test, y_pred)
print(f'Точность: {accuracy:.2f}')

# Визуализация результатов
def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = plt.cm.RdYlBu

    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    Z = Z.reshape(xx1.shape)

    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                    alpha=0.8, c=colors[idx],
                    marker=markers[idx], label=iris.target_names[cl])

    if test_idx:
        X_test, y_test = X[test_idx, :], y[test_idx]
        plt.scatter(X_test[:, 0], X_test[:, 1],
                    c='none', edgecolor='black', alpha=1.0,
                    linewidth=1, marker='o',
                    s=100, label='test set')       
      

# Визуализация результатов
X_combined = np.vstack((X_train, X_test))
y_combined = np.hstack((y_train, y_test))
plot_decision_regions(X_combined, y_combined, classifier=ppn, test_idx=range(105, 150))
plt.xlabel('длина лепестка [см]')
plt.ylabel('ширина лепестка [см]')
plt.legend(loc='upper left')
plt.title('Классификация ирисов персептроном')
plt.tight_layout()
plt.show()

# Вывод первых 5 строк датасета
print("\nПервые 5 строк датасета:")
print(iris.data[:5])
print("\nСоответствующие метки классов:")
print(iris.target[:5])
print("\nНазвания классов:")
print(iris.target_names)