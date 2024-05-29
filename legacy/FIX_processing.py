import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Замените 'input.csv' на путь к вашему CSV-файлу
input_file = 'formated_data.csv'

# Загрузите данные из CSV-файла в объект DataFrame с использованием pandas
df = pd.read_csv(input_file)

# Добавляем новую колонку среднего значения 'AMP PROCESSING' по группе 'Freq'
df['Noise'] = df.groupby('Freq')['Ampltude'].transform('mean')
# df['MPA']=df['MPA']-6

# df['MPA'] = round(df['MPA'] / 6) * 6

# df['MPA']=df['MPA']+15

# df = df[df['Ampltude'] > df['Noise']]
df = df[df['Noise'] != 0]

df = df[df['Ampltude'] > df['Noise'] ]

df.to_csv('processing_data.csv', index=False, float_format='%.3f')
