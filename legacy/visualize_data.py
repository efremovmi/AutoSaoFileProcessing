import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Замените 'input.csv' на путь к вашему CSV-файлу
input_file = 'processing_data.csv'

# Загрузите данные из CSV-файла в объект DataFrame с использованием pandas
df = pd.read_csv(input_file)

# Извлеките столбцы "Range" и "Freq" в переменные X и Y
Y = df['Range']
X = df['Freq']
Pol = df['Polarize']
Doppler = df['Doppler']

colors_positive = ['cyan', 'blue', 'purple', 'pink', 'red', 'orange', 'yellow', 'burlywood']

colors_negative = ['green', 'lightgreen']

colors = []
for i in range(len(Doppler)):
    if Pol[i] == 90:
        colors.append(colors_positive[4])
        # if Doppler[i] >= 4:
        #     colors.append(colors_positive[7])
        # if 4 > Doppler[i] >= 3:
        #     colors.append(colors_positive[6])
        # if 3 > Doppler[i] >= 2:
        #     colors.append(colors_positive[5])
        # if 2 > Doppler[i] >= 0:
        #     colors.append(colors_positive[4])
        # if 0 > Doppler[i] >= -2:
        #     colors.append(colors_positive[3])
        # if -2 > Doppler[i] >= -3:
        #     colors.append(colors_positive[2])
        # if -3 > Doppler[i] >= -4:
        #     colors.append(colors_positive[1])
        # if -4 >= Doppler[i]:
        #     colors.append(colors_positive[0])
    else:
        # if Doppler[i] >= 0:
        colors.append(colors_negative[0])
        # else:
        #     colors.append(colors_negative[1])


# Постройте график
plt.scatter(X, Y, c=np.array(colors), s=1)
plt.xlabel('Freq')
plt.ylabel('Range')
plt.title('График Range от Freq')
plt.grid(True)

# Отобразите график
plt.show()