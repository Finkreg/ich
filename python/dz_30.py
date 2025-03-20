# 1. Создайте класс Rectangle для представления прямоугольника. 
# Класс должен иметь атрибуты width (ширина) и height (высота) со значениями по умолчанию, а также методы calculate_area() 
# для вычисления площади прямоугольника и calculate_perimeter() для вычисления периметра прямоугольника. 
# Переопределить методы __str__, __repr__.
# Затем создайте экземпляр класса Rectangle и выведите информацию о нем,                           его площадь и периметр.

# class Rectangle:

#     def __init__(self, width, height):
#         self.width = width
#         self.height = height

#     def calculate_area(self):
#         return self.width * self.height
    
#     def calculate_perimeter(self):
#         return (self.height + self.width) * 2
    
#     def __str__(self):
#         return f"Rectangle of: width = {self.width}, height = {self.height}"
    
#     def __repr__(self):
#         return f"class: Rectangle, width:{self.width}, height:{self.height}"
    

# figure_1 = Rectangle(3, 4)
# print(repr(figure_1))
# print(str(figure_1))



# 2. Создайте класс BankAccount для представления банковского счета. Класс должен иметь атрибуты account_number (номер счета)
# и balance (баланс), а также методы deposit() для внесения денег на счет и withdraw() для снятия денег со счета. Затем 
# создайте экземпляр класса BankAccount, внесите на счет некоторую сумму и снимите часть денег. Выведите оставшийся баланс.
# Не забудьте предусмотреть вариант, при котором при снятии баланс может стать меньше нуля. В этом случае уходить в минус 
# не будем, вместо чего будем возвращать сообщение "Недостаточно средств на счете".

class BankAccount:

    def __init__(self):
        self.account_number = 735562
        self.balance = 1000


    def deposit(self, dep_ammount):
        self.dep_ammount = dep_ammount
        print(f"peeep.....peeeep....  {self.dep_ammount}$ have been added to your account")
        self.balance += self.dep_ammount
        self.check_balance()


    def withdraw(self, withdraw_ammount):
        self.withdraw_ammount = withdraw_ammount
        if self.balance - self.withdraw_ammount < 0:
            print("Insufficient Funds")
            raise ValueError("Withdrawal amount exceeds available balance.")
        self.balance -= self.withdraw_ammount
        print(f"peeeep....peeeep... {self.withdraw_ammount}$ have been withdrawn from your account")
        self.check_balance()
        
    
    def check_balance(self):
        print(f"your current balance is: {self.balance}")

my_acc = BankAccount()
my_acc.withdraw(1200)
my_acc.deposit(3798)
