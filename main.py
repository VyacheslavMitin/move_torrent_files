import os
import sys
import glob
import shutil
import time

path_source = os.path.join("/Users/sonic/Downloads/")
path_destination = os.path.join("/Volumes/WD_4TB/+TORRENT/watch/")
extension = "*.torrent"

files_list = glob.glob(path_source + extension)

print("Скрипт для перемещения торрент файлов на загрузку Transmission\n".upper())

if files_list:
    for file in files_list:
        try:
            shutil.copy(file, path_destination)
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
