# 1. Напишите функцию find_longest_word, которая будет принимать список слов и возвращать самое
# длинное слово из списка. Аннотируйте типы аргументов и возвращаемого значения функции.
#
def find_longest_word(data: list[str]) -> str:
    temp = ''
    for i in range(len(data)):
        if len(data[i]) > len(temp):
            temp = data[i]
    return temp

words = ["apple", "banana", "cherry", "dragonfruit"]
print(find_longest_word(words))



# 2. Напишите программу, которая будет считывать данные о продуктах из файла и использовать
# аннотации типов для аргументов и возвращаемых значений функций. Создайте текстовый файл "products.txt",
# в котором каждая строка будет содержать информацию о продукте в формате "название, цена, количество". Например:
# Apple, 1.50, 10
# Banana, 0.75, 15
# В программе определите функцию calculate_total_price, которая будет принимать список продуктов и возвращать
# общую стоимость. Продумайте, какая аннотация должна быть у аргумента! Считайте данные из файла, разделите
# строки на составляющие и создайте список продуктов. Затем вызовите функцию calculate_total_price с этим
# списком и выведите результат.


#В первом варианте я передаю в функцию файл.

from typing import TextIO

def calculate_total_price(data: TextIO) -> float:
    total = 0
    for line in data:
        line = line.strip().split(",")
        total += float(line[1])
    return total

with open("products.txt", "r") as file:
    print(f"The total sum of all products is: {calculate_total_price(file)}")

#===================SECOND==VARIANT=========================================
#Во втором варианте я передаю в функцию список из списков продуктов

def calculate_total_price(data: list[list[str]]) -> float:
    total_sum = 0
    for item in data:
        total_sum += float(item[1])
    return total_sum

with open("products.txt", "r") as file:
    product_list = []
    for line in file:
        line = line.strip().split(",")
        product_list.append(line)

print(f"The total sum of all products is: {calculate_total_price(product_list)}")
