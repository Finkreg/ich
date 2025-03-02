import sys
import os
# 1. Напишите программу, которая принимает в качестве аргумента командной строки путь к файлу .py и
# запускает его. При запуске файла программа должна выводить сообщение "Файл <имя файла> успешно запущен".
# Если файл не существует или не может быть запущен, программа должна вывести соответствующее сообщение об ошибке.
#
arguments = sys.argv
fpath = arguments[1]

def run_python_file(filepath):
    if os.path.isfile(filepath):
        print(f"Success, file {arguments[1]} loaded")
        exec(open(filepath).read())
    elif not filepath.endswith('.py'):
        print("This is no a python file")
    elif not os.path.isfile(filepath):
        print("Failure, file not found")

run_python_file(fpath)

# 2. Напишите программу, которая принимает в качестве аргумента командной строки путь к директории и
# выводит список всех файлов и поддиректорий внутри этой директории. Для этой задачи используйте модуль
# os и его функцию walk. Программа должна выводить полный путь к каждому файлу и директории.

arguments = sys.argv
directory_path = arguments[1]

def show_all_names(dirpath):
    for root, dirs, files in os.walk(dirpath):
        for name in dirs:
            print(os.path.join(root, name))
        for name in files:
            print(os.path.join(root, name))

show_all_names(directory_path)