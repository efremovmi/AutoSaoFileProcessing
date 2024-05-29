import os
import shutil

def find_and_move_files(src_directory, dst_directory, extension=".MMM"):
    # Проверяем, существует ли целевая директория, если нет - создаем
    if not os.path.exists(dst_directory):
        os.makedirs(dst_directory)

    # Рекурсивно проходим по всем файлам и поддиректориям
    for root, dirs, files in os.walk(src_directory):
        for file in files:
            if file.endswith(extension):
                src_path = os.path.join(root, file)
                dst_path = os.path.join(dst_directory, file)
                # Перемещаем файл в целевую директорию
                shutil.move(src_path, dst_path)
                print(f"Moved: {src_path} to {dst_path}")

# Пример использования
source_directory = "C:\\Users\\genri\\Рабочий стол\\data"
destination_directory = "C:\\Users\\genri\\Рабочий стол\\result"
find_and_move_files(source_directory, destination_directory)
