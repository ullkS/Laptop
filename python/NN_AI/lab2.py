import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Загрузка данных
data = pd.read_csv('C:\\Users\\rhsvp\\code\\Workers\\python\\NN_AI\\wine.csv')

# Предобработка данных, выбор числовых колонок для кластеризации
numeric_columns = data.select_dtypes(include=[np.number]).columns
X = data[numeric_columns]

# Стандартизация данных
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Применение K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
data['Cluster'] = kmeans.fit_predict(X_scaled)

# Тепловая карта 1: Средние значения признаков по кластерам
plt.figure(figsize=(10, 8))
cluster_means = data.groupby('Cluster')[numeric_columns].mean()
sns.heatmap(cluster_means, annot=True, cmap='YlGnBu', fmt='.2f')
plt.title('Средние значения признаков по кластерам')

# Тепловая карта 2: Корреляция признаков
plt.figure(figsize=(10, 8))
correlation_matrix = data[numeric_columns].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Корреляция признаков')

# Визуализация 3: Scatter plot кластеров в пространстве главных компонент
plt.figure(figsize=(10, 8))
pca = PCA(n_components=2)
pca_result = pca.fit_transform(X_scaled)
plt.scatter(pca_result[:, 0], pca_result[:, 1], c=data['Cluster'], cmap='viridis')
plt.title('Распределение кластеров в пространстве главных компонент')
plt.xlabel('Первая главная компонента')
plt.ylabel('Вторая главная компонента')
plt.colorbar(label='Кластер')

# Показать все графики
plt.show()