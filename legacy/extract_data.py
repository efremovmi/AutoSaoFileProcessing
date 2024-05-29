import csv
import re

# Открываем входной текстовый файл и выходной CSV-файл
input_file = 'input.txt'
output_file = 'formated_data.csv'

with open(input_file, 'r') as text_file, open(output_file, 'w', newline='') as csv_file:
    # Создаем объект для записи CSV
    csv_writer = csv.writer(csv_file)

    for line in text_file:
        # Используем регулярное выражение, чтобы заменить группу смежных пробелов на одну запятую
        line = re.sub(r'\s+', ',', line.strip())

        # Разделяем строку на значения, используя запятую как разделитель
        values = line.split(',')

        # Записываем значения в CSV-файл
        csv_writer.writerow(values)

print(f"Преобразование завершено. Результат сохранен в '{output_file}'.")
