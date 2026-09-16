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
    """Основная функция для перемещения файлов из исходной папки в выбранную папку назначения"""
    # Получаем путь назначения с помощью select_destination()
    path = select_destination()
    # Если в исходной папке есть файлы, соответствующие маске
    if files_list:
        for file in files_list:
            # Максимальное количество попыток копирования
            max_attempts = 3
            # Флаг успешного копирования
            copied = False
            # Получаем имя файла
            file_name = os.path.basename(file)
            # Делаем до 3 попыток копирования
            for attempt in range(1, max_attempts + 1):
                try:
                    print(
                        f"Копирование файла: {file_name} "
                        f"(попытка {attempt}/{max_attempts})"
                    )
                    # Копируем файл на QNAP NAS
                    shutil.copy(file, path)
                    # Небольшая пауза после копирования
                    time.sleep(0.3)
                    # Если copy() завершился без ошибки,
                    # считаем копирование успешным
                    copied = True
                    print(
                        f"Копирование успешно: {file_name} "
                        f"(попытка {attempt}/{max_attempts})"
                    )
                    # Выходим из цикла попыток
                    break
                except PermissionError as e:
                    print(
                        f"Ошибка доступа при копировании "
                        f"{file_name}: {e}"
                    )
                except FileNotFoundError as e:
                    print(
                        f"Файл не найден при копировании "
                        f"{file_name}: {e}"
                    )
                except OSError as e:
                    # Другие ошибки файловой системы / сетевого ресурса
                    print(
                        f"Ошибка ОС при копировании "
                        f"{file_name}: {e}"
                    )
                # Если попытка не последняя — ждём и пробуем снова
                if not copied and attempt < max_attempts:
                    print(
                        f"Повторная попытка через 1 секунду: "
                        f"{file_name}"
                    )
                    time.sleep(1)
            # Если после 3 попыток файл так и не скопировался
            if not copied:
                print(
                    f"ОШИБКА: файл не удалось скопировать "
                    f"после {max_attempts} попыток: {file_name}"
                )
                print("Ошибка работы с каталогом/файлом на QNAP NAS!")
                sys.exit(1)
            # ---------------------------------------------------------
            # Удаляем оригинальный файл ТОЛЬКО после успешного копирования
            # ---------------------------------------------------------
            try:
                os.remove(file)
                print(f"Исходный файл удален: {file_name}")
                print(f"Файл перемещен: {file_name}")
            except PermissionError as e:
                print(
                    f"Ошибка удаления исходного файла "
                    f"{file_name}: {e}"
                )
                sys.exit(1)
            except FileNotFoundError:
                # Файл уже отсутствует — возможно, его удалил другой процесс
                print(
                    f"Исходный файл уже отсутствует: {file_name}"
                )
    else:
        # Если файлов для перемещения нет
        print("Файлов для перемещения нет")
    # После завершения работы
    print("\nЗавершение")
    sys.exit(0)


# Точка входа при запуске скрипта
if __name__ == '__main__':
    print(f"Родительский каталог: {path_source}")
    # print(*files_list)
    move_files()
