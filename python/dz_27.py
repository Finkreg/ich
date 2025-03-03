# Напишите функцию, которая принимает на вход список чисел и возвращает сумму квадратов
# только четных чисел из списка, используя функциональные подходы
# (например, map, filter и reduce).
#
# Пример вывода:
# Введите числа: 4, 6, 3, 4, 2, 3, 9, 0, 7
# Результат: 72

def make_squares(data: list[int]):
    # only_even = [num for num in data if num % 2 == 0]
    only_even = list(filter(lambda x : x % 2 == 0, data))
    return map(lambda x: x ** 2, only_even)

def sum_nums(numlist):
    return sum(numlist)

my_list = [4, 6, 3, 4, 2, 3, 9, 0, 7]
print(sum_nums(make_squares(my_list)))



# Напишите функцию, которая принимает на вход список функций и значение, а затем применяет
# композицию этих функций к значению, возвращая конечный результат.
#
#
# Пример использования:
# add_one = lambda x: x + 1
# double = lambda x: x * 2
# subtract_three = lambda x: x - 3
# functions = [add_one, double, subtract_three]
# compose_functions(functions, 5) должно вывести 9

add_one = lambda x: x + 1
double = lambda x: x * 2
subtract_three = lambda x: x - 3

function_list = [add_one, double, subtract_three]

def compose_functions(functions, x):
    for function in functions:
        x = function(x)
    return x

print(compose_functions(function_list,5))