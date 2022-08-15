import os
import sys
import glob
import shutil
import time

path_source = os.path.join("/Users/sonic/Downloads/")
extension = "*.torrent"
path_destination0 = os.path.join("/Volumes/WD_4TB/+TORRENT/watch/")
path_destination1 = os.path.join("/Volumes/Seagate_2TB/+TORRENT/watch/")
destination_list = []

files_list = glob.glob(path_source + extension)

print("Скрипт для перемещения торрент файлов на загрузку Transmission\n".upper())


def select_destination():
    path_destination = ''

    if os.path.isdir(path_destination0):
        destination_list.append(path_destination0)

    if os.path.isdir(path_destination1):
        destination_list.append(path_destination1)

    print(destination_list)

    # if destination_list == [path_destination0, path_destination1]:
    #     machine = input("Выбрать машину для загрузки:\n"
    #                     "1 - Kenetic Ultra\n"
    #                     "2 - Kenetic Extra\n"
    #                     "Ввод:  ")
    #     if machine == '1':
    #         path_destination = path_destination0
    #     elif machine == '2':
    #         path_destination = path_destination1
    if destination_list:
        path_destination = destination_list[0]

        return path_destination

    else:
        sys.exit("Ошибка, путь не выбран")


def move_files():
    path = select_destination()

    if files_list:
        for file in files_list:
            try:
                shutil.copy(file, path)
                time.sleep(0.1)
                os.remove(file)
            except PermissionError:
                print("Ошибка работы с папкой на роутере!")
                sys.exit(1)
            else:
                file_name = file.split('/')
                _, _, _, _, file_name = file_name
                print(f"Файл перемещен: {file_name}")

    else:
        print("Файлов для перемещения нет")

    print("\nВыход")
    sys.exit(0)


if __name__ == '__main__':
    move_files()
