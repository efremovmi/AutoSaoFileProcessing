import subprocess
import keyboard
import pyperclip
import pyautogui
from pywinauto import Desktop, WindowSpecification
import psutil
import os
import shutil
import time


def kill_process_by_name(process_name):
    """
        Завершает процесс по его имени.

        Args:
            process_name (str): Имя процесса.

        Returns:
            None
    """
    for process in psutil.process_iter():
        if process.name() == process_name:
            try:
                process.terminate()  # Или можно использовать process.kill() для принудительного завершения
                print(f"Процесс с именем {process_name} успешно завершен.")
            except psutil.AccessDenied:
                print(f"Отказано в доступе к процессу с именем {process_name}.")
            except psutil.NoSuchProcess:
                print(f"Процесс с именем {process_name} не найден.")

def get_dialog(window:  WindowSpecification):
    """
       Возвращает диалоговое окно для открытия входного файла

       Args:
           window (WindowSpecification): Объект окна, в котором есть диалоговое окно

       Returns:
           WindowSpecification: Диалоговое окно.

       Raises:
           Exception: Если не удалось найти указанное диалоговое окно.
    """
    children = window.children()
    for child in children:
        if child.element_info.name == 'Open one file or many files (use CTRL)':
            return child

    raise Exception("Can't found dialog menu 'Open one file or many files (use CTRL)'")

def file_processing(path_to_input_file: str):
    """
       Обрабатывает данные, используя входной файл.

       Args:
           path_to_input_file (str): Путь к входному файлу.

       Returns:
           None
    """
    desktop = Desktop(backend="uia")
    window = desktop.window(title='SAOExplorer v 3.6.1')

    # Открытие диалогового окна
    rect = window.rectangle()

    window_coords = (rect.left, rect.top)
    open_dialog_rel_coords = (50, 90)
    pyautogui.moveTo(window_coords[0] + open_dialog_rel_coords[0],
                     window_coords[1] + open_dialog_rel_coords[1], duration=0.1)
    pyautogui.click()


    # Ожидание открытия Dialog окна
    time.sleep(1)

    rect = get_dialog(window).rectangle()
    window_coords = (rect.left, rect.top)

    time.sleep(0.1)

    # Перемещение курсора к указанным координатам поля ввода
    input_text_field_rel_coords = (200, 330)
    pyautogui.moveTo(window_coords[0] + input_text_field_rel_coords[0],
                     window_coords[1] + input_text_field_rel_coords[1], duration=0.01)
    time.sleep(0.1)

    pyautogui.click()

    # # Ввод текста
    pyperclip.copy(path_to_input_file)
    keyboard.press_and_release('ctrl + v')

    # Запуск обработки
    ok_button_rel_coords = (500, 410)
    pyautogui.moveTo(window_coords[0] + ok_button_rel_coords[0],
                     window_coords[1] + ok_button_rel_coords[1], duration=0.01)
    pyautogui.click()

    # Ожидание обработки
    time.sleep(0.5)

def save_to_csv(path_to_input_file: str):
    """
       Сохраняет результаты в CSV файл.

       Returns:
           None
    """
    desktop = Desktop(backend="uia")
    window = desktop.window(title='SAOExplorer v 3.6.1')

    rect = window.rectangle()
    window_coords = (rect.left, rect.top)

    # Перемещение курсора к указанным координатам поля ввода
    bulk_processing_field_rel_coords = (200, 40)
    pyautogui.moveTo(window_coords[0] + bulk_processing_field_rel_coords[0],
                     window_coords[1] + bulk_processing_field_rel_coords[1], duration=0.01)
    pyautogui.click()

    time.sleep(0.1)

    export_field_rel_coords = (200, 70)
    pyautogui.moveTo(window_coords[0] + export_field_rel_coords[0],
                     window_coords[1] + export_field_rel_coords[1], duration=0.01)
    pyautogui.click()

    time.sleep(0.1)

    amplitudes_field_rel_coords = (500, 120)
    pyautogui.moveTo(window_coords[0] + amplitudes_field_rel_coords[0],
                     window_coords[1] + amplitudes_field_rel_coords[1], duration=0.01)
    pyautogui.click()

    time.sleep(0.1)

    # Сохранение файла
    window = desktop.window(title='Save All Ionogram Amplitudes to a text file')

    rect = window.rectangle()
    window_coords = (rect.left, rect.top)

    # Перемещение курсора к указанным координатам поля ввода
    input_text_field_rel_coords = (400, 500)
    pyautogui.moveTo(window_coords[0] + input_text_field_rel_coords[0],
                     window_coords[1] + input_text_field_rel_coords[1], duration=0.01)
    pyautogui.click()

    time.sleep(0.1)  # Небольшая пауза для надежности
    # Выделить все
    keyboard.press_and_release('ctrl + a')
    time.sleep(0.1)  # Небольшая пауза для надежности

    # Удалить все
    keyboard.press_and_release('delete')
    time.sleep(0.1)  # Небольшая пауза для надежности

    # # Ввод текста
    pyperclip.copy(path_to_input_file+".txt")
    keyboard.press_and_release('ctrl + v')

    # Сохранение
    ok_button_rel_coords = (700, 500)
    pyautogui.moveTo(window_coords[0] + ok_button_rel_coords[0],
                     window_coords[1] + ok_button_rel_coords[1], duration=0.01)
    pyautogui.click()


# ======================================================================================================================
if __name__ == "__main__":
    # ======================================================================================================================
    # Блок констант
    PATH_WITH_SAO_JAVA = "C:/Users/genri/Рабочий стол/SAOExplorer_3.6"
    JAVA_COMM_ARG = ["java", "-classpath",
                     "lib/SAOExplorer-3.6.1.jar;lib/jaybird-full-3.0.9.jar;lib/epsgraphics.jar;lib/JimiProClasses.zip;lib/Jama-1.0.1.jar;lib/xerces.jar;lib/exp4j-0.4.8.jar",
                     "SAOExplorer.SAOExplorer", "-ud"]

    # Путь к исходной директории, где находятся входные файлы
    INPUT_DIR = "C:\\Users\\genri\\Рабочий стол\\диплом\\dataset_raw"
    # Путь к директории, где будут находиться выходные файлы
    OUTPUT_DIR = "C:\\Users\\genri\\Рабочий стол\\диплом\\dataset_txt"
    # ======================================================================================================================


    start_time = time.time()

    os.chdir(PATH_WITH_SAO_JAVA)

    # Запуск файла
    process = subprocess.Popen(JAVA_COMM_ARG)

    # Подождем немного, чтобы приложение загрузилось
    time.sleep(8)

    input_files = []

    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith('.MMM') or file.endswith('.RSF'):
                file_path = os.path.join(root, file)
                input_files.append(file_path)

    # Обработка файлов
    i = 0
    delta = 8
    for input_file in input_files:
        start = time.time()
        print(f"Обработано {i}/{len(input_files)} файлов. Осталось примерно: {(len(input_files) - i) * delta} секунд")
        file_processing(input_file)
        save_to_csv(input_file[:-4])
        time.sleep(0.1)
        end = time.time()
        delta = end - start
        i+=1


    kill_process_by_name('java.exe')

    # Перебираем все файлы в исходной директории
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            # Проверяем, является ли файл текстовым файлом
            if file.endswith('.txt'):
                # Полный путь к текущему файлу
                file_path = os.path.join(root, file)
                try:
                    # Перемещаем файл в целевую директорию
                    shutil.move(file_path, OUTPUT_DIR)
                    print(f"Файл {file} перемещен успешно.")
                except Exception as e:
                    print(f"Ошибка при перемещении файла {file}: {e}")


    print("Обработка закончена")
    print("--- Затрачено %s секунд ---" % (time.time() - start_time))
# ======================================================================================================================