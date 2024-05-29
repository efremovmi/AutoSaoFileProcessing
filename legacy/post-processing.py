import pandas as pd
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import seaborn as sns

plt_y_size = 30
plt_x_size = 15
xlim = (3, 15)
ylim = (0, 700)

df = pd.read_csv("formated_data.csv")

df['Pol_cluster'] = df['Pol'] < 0


# Обучите модель DBSCAN
dbscan = DBSCAN(eps=40, min_samples=20)

plt.figure(figsize=(plt_y_size, plt_x_size))

# Визуализация результатов
plt.subplot(1, 3, 1)
sns.scatterplot(x='Freq', y='Range', hue='Pol_cluster', data=df, palette='viridis', s=100)
plt.title('Исходные данные')
plt.xlabel('Freq')
plt.ylabel('Range')
plt.xlim(xlim)  # Границы для оси X
plt.ylim(ylim)  # Границы для оси Y

# Класстеризуем данные
df['Cluster'] = dbscan.fit_predict(df[['Range', 'Freq']])

# Визуализация результатов
plt.subplot(1, 3, 2)
sns.scatterplot(x='Freq', y='Range', hue='Cluster', data=df, palette='viridis', s=100)
plt.title('DBSCAN кластеризация')
plt.xlabel('Freq')
plt.ylabel('Range')
plt.xlim(xlim)
plt.ylim(ylim)


# Избавляемся от шума
df = df[df['Cluster'] != -1]

# Выбрать запись с самым низким значением для обоих полей
min_range_cluster = df.loc[df['Range'].idxmin(), 'Cluster']
df = df[df['Cluster'] == min_range_cluster]

# Визуализация результатов
plt.subplot(1, 3, 3)
sns.scatterplot(x='Freq', y='Range', hue='Pol_cluster', data=df, palette='viridis', s=100)
plt.title('Пост обработка')
plt.xlabel('Freq')
plt.ylabel('Range')
plt.xlim(xlim)  # Границы для оси X
plt.ylim(ylim)  # Границы для оси Y
plt.show()


