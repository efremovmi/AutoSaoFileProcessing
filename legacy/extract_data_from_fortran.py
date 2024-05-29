import csv
import re
from math import ceil



# Открываем входной текстовый файл и выходной CSV-файл
input_file = 'ionogram.dat'
output_file = 'formated_data.csv'

def fix_data(inp):
    output = re.sub(r'\d{4} \d{3} \d{2}:\d{2}:\d{2}', '', inp)
    return output
    # year = re.findall(r'\d{4}', find_str)[0]
    # time = re.f
    # day_count = re.findall(r' \d{3} ', find_str)[0]
    # month = ceil(day_count / 20)




with open(input_file, 'r') as text_file, open(output_file, 'w', newline='') as csv_file:
    # Создаем объект для записи CSV
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Freq", "Range", "Polarize", "Noise", "Doppler", "Az", "Zn", "Ampltude", "Phase"])
    for line in text_file:
        if line[0] == '#':
            continue

        # Используем регулярное выражение, чтобы заменить группу смежных пробелов на одну запятую

        line = fix_data(line)
        line = re.sub(r'\s+', ',', line.strip())

        # Разделяем строку на значения, используя запятую как разделитель
        values = line.split(',')

        # Записываем значения в CSV-файл
        csv_writer.writerow(values)

print(f"Преобразование завершено. Результат сохранен в '{output_file}'.")
