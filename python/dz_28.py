# Напишите программу, которая принимает список слов от пользователя и использует
# генераторное выражение (comprehension) для создания нового списка, содержащего
# только те слова, которые начинаются с гласной буквы. Затем программа должна использовать
# функцию map, чтобы преобразовать каждое слово в верхний регистр. В результате программа
# должна вывести новый список, содержащий только слова, начинающиеся с гласной буквы и
# записанные в верхнем регистре.
import itertools
import operator


def separate_words(wordlist: list[str]) -> list[str]:
    vocals = "aeiuyo"
    # temp=[word for word in wordlist if word[0] in vocals]
    # new_list = list(map(lambda word: word.upper(), temp))
    new_list = list(map(lambda word: word.upper(), [word for word in wordlist if word[0] in vocals]))
    return new_list


words = ['apple', 'banana', 'dragonfruit', 'kiwi', 'apricot']
print(separate_words(words))



# Напишите программу, которая принимает список чисел от пользователя и использует функцию
# reduce из модуля functools, чтобы найти произведение всех чисел в списке. Затем программа
# должна использовать функцию itertools.accumulate для накопления произведений чисел в новом
# списке. В результате программа должна вывести список, содержащий накопленные произведения.

from functools import reduce
import operator

def sum_multiplied_nums(data:list[int]):
    total_num = reduce(lambda x, y: x*y, data)
    accumulated_nums = list(itertools.accumulate(data, operator.mul))
    return total_num, accumulated_nums

numbers = [1,2,3,4,5]
total_prod, sum_prod = sum_multiplied_nums(numbers)
print(f"total_production of numbers is {total_prod}")
print(f"sum_production of numbers is {sum_prod}")