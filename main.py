import os                 # Работа с операционной системой: пути, проверка директорий и т.д.
import sys                # Выход из программы с кодом ошибки и другие системные функции
import glob               # Поиск файлов, соответствующих шаблону (маске)
import shutil             # Копирование и удаление файлов
import time               # Тайминги (здесь — паузы между операциями)

# Исходный путь с файлами для перемещения — папка ~/Downloads
path_source = os.path.join("/Users/sonic/Downloads/")  # Лучше развернуть ~ в полный путь

# Пути возможных папок назначения для копирования файлов
path_destination0 = os.path.join("/Volumes/WD_4TB/+TORRENT/watch/")
path_destination1 = os.path.join("/Volumes/Common/+Torrent/.watch")

# Список путей к папкам назначения (будет заполняться динамически)
destination_list = []

# Вывод приветствия и описания скрипта (заглавными буквами)
print("Скрипт для перемещения торрент файлов на загрузку Transmission\n".upper())


def find_pornolab_torrents(path_source_=path_source):
    """
    Ищет в заданной папке файлы, начинающиеся с '[pornolab.net]' и с расширением .torrent.
    Возвращает список найденных файлов с полными путями.
    """
    list_ = []
    # os.chdir(path_source_)
    pattern = os.path.join(path_source_, "*pornolab*")
    # pattern = "*pornolab*"
    # print(pattern)
    # list_.append(glob.glob(pattern))
    return glob.glob(pattern)


files_list = find_pornolab_torrents(path_source_=path_source)


def select_destination():
    # Функция выбирает одну из папок назначения, если они существуют

    # Проверяем, существует ли path_destination0 как директория
    if os.path.isdir(path_destination0):
        destination_list.append(path_destination0)  # Добавляем в список возможных назначений

    # Аналогично для path_destination1
    if os.path.isdir(path_destination1):
        destination_list.append(path_destination1)

    # Печатаем найденные пути назначения (для информирования)
    print(f"Целевой каталог: {destination_list[0]}\n")

    # Если список названий не пуст — выбираем первый как путь назначения
    if destination_list:
        path_destination = destination_list[0]
        return path_destination
    else:
        # Если ни одна папка не доступна, завершаем программу с сообщением об ошибке
        sys.exit("Ошибка, путь не выбран")


def move_files():
    # Основная функция для перемещения файлов из исходной папки в выбранную папку назначения

    # Получаем путь назначения с помощью select_destination()
    path = select_destination()

    # Если в исходной папке есть файлы, соответствующие маске
    if files_list:
        for file in files_list:
            try:
                # Копируем файл из исходной папки в папку назначения
                shutil.copy(file, path)

                # Пауза между операциями, чтобы избежать возможных конфликтов доступа
                time.sleep(0.3)

                # После успешного копирования удаляем оригинальный файл
                os.remove(file)

            except PermissionError:
                # Обработка ошибки недостатка прав доступа
                print("Ошибка работы с каталогом на роутере!")
                sys.exit(1)  # Завершаем программу с ошибкой

            except FileNotFoundError:
                # Обработка ситуации, когда файл внезапно не найден (например, удалён другим процессом)
                print("Ошибка работы с файлом на роутере!")

            else:
                # Если ошибки не возникло — выводим имя перемещенного файла

                # Разбиваем путь по разделителям /, чтобы получить имя файла
                file_name = file.split('/')
                # По исходному пути ожидается 5-элементная структура, берем последний элемент - имя файла
                _, _, _, _, file_name = file_name

                print(f"Файл перемещен: {file_name}")

    else:
        # Если файлов для перемещения нет, выводим соответствующее сообщение
        print("Файлов для перемещения нет")

    # После завершения работы выводим сообщение о выходе и завершаем программу без ошибки
    print("\nЗавершение")
    sys.exit(0)


# Точка входа при запуске скрипта
if __name__ == '__main__':
    print(f"Родительский каталог: {path_source}")
    # print(*files_list)
    move_files()
