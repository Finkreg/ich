# 1. Реализовать класс Counter, который представляет счетчик. Класс должен поддерживать следующие операции:
# - Увеличение значения счетчика на заданное число (оператор +=)
# - Уменьшение значения счетчика на заданное число (оператор -=)
# - Преобразование счетчика в строку (метод __str__)
# - Получение текущего значения счетчика (метод __int__)
#
# Пример использования:
# counter = Counter(5)
# counter += 3
# print(counter)  # Вывод: 8
# counter -= 2
# print(int(counter))  # Вывод: 6
import functools


class Counter:
    def __init__(self, initial_value):
        self.initial_value = initial_value

    def __iadd__(self, other):
        self.initial_value += other
        return self

    def __isub__(self, other):
        self.initial_value -= other
        return self.initial_value

    def __str__(self):
        return str(self.initial_value)

    def __int__(self):
        return int(self.initial_value)

counter = Counter(5)
counter += 3
print(counter)
counter -= 2
print(int(counter))




# 2. Реализовать класс Email, представляющий электронное письмо. Класс должен поддерживать следующие операции:
# - Сравнение писем по дате (операторы <, >, <=, >=, ==, !=)
# - Преобразование письма в строку (метод __str__)
# - Получение длины текста письма (метод __len__)
# - Получение хеш-значения письма (метод __hash__)
# - Проверка наличия текста в письме (метод __bool__)
#
# Пример использования:
# email1 = Email("john@example.com", "jane@example.com", "Meeting", "Hi Jane, let's have a meeting tomorrow.", "2022-05-10")
# email2 = Email("jane@example.com", "john@example.com", "Re: Meeting", "Sure, let's meet at 2 PM.", "2022-05-10")
# email3 = Email("alice@example.com", "bob@example.com", "Hello", "Hi Bob, how are you?", "2022-05-09")
# print(email1)  # Вывод:
# """
# From: john@example.com
# To: jane@example.com
# Subject: Meeting
# Hi Jane, let's have a meeting tomorrow.
# """
# print(len(email2))  # Вывод: 24
# print(hash(email3))  # Вывод: -920444056
# print(bool(email1))  # Вывод: True
# print(email2 > email3)  # Вывод: True

from datetime import datetime

@functools.total_ordering
class Email:
    def __init__(self, from_, to_, subject, message, date):
        self.from_ = from_
        self.to_ = to_
        self.subject = subject
        self.message = message
        self.date = datetime.fromisoformat(date).date()

    def __str__(self):
        return str(f'"""\nFrom: {self.from_},\nTo: {self.to_},\nSubject: {self.subject},\n{self.message},\n{self.date}\n""" ')


    def __len__(self):
        return len(self.message)


    def __hash__(self):
        return hash(self.message)


    def __bool__(self):
        return bool(self.message)


    def __eq__(self, other):
        if isinstance(other, Email):
            return self.date == other.date


    def __lt__(self, other):
        if isinstance(other, Email):
            return self.date < other.date

email1 = Email("john@example.com", "jane@example.com", "Meeting", "Hi Jane, let's have a meeting tomorrow.", "2022-05-10")
email2 = Email("jane@example.com", "john@example.com", "Re: Meeting", "Sure, let's meet at 2 PM.", "2022-05-10")
email3 = Email("alice@example.com", "bob@example.com", "Hello", "Hi Bob, how are you?", "2022-05-09")
print(email1)
print(len(email1))
print(hash(email1))
print(bool(email1))
print(email2 > email3)

