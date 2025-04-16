# В базе данных ich_edit три таблицы. Users с полями (id, name, age), 
# Products с полями (pid, prod, quantity) и 
# Sales с полями (sid, id, pid).
# Программа должна запросить у пользователя название таблицы и 
# вывести все ее строки или сообщение, что такой таблицы нет.

import mysql.connector


dbconfig = {'host': 'ich-edit.edu.itcareerhub.de',
'user': 'ich1',
'password': 'ich1_password_ilovedbs',
'database': 'ich_edit'}
connection = mysql.connector.connect(**dbconfig)

cursor = connection.cursor()

table_name = input("Please enter the name of the table to connect to: ")

if not table_name.isidentifier():
    raise ValueError("Not a valid table name!")
try: 
    cursor.execute(f"Select * from {table_name}")
    result = cursor.fetchall()
    for row in result:
        print(row)
except mysql.connector.Error as e:
    print(f"Database error {e}")

cursor.close()
connection.close()


#     В базе данных ich_edit три таблицы. Users с полями (id, name, age), 
# Products с полями (pid, prod, quantity) и Sales с полями (sid, id, pid).

# Программа должна вывести все имена из таблицы users, дать пользователю 
# выбрать одно из них и вывести все покупки этого пользователя.

dbconfig = {'host': 'ich-edit.edu.itcareerhub.de',
'user': 'ich1',
'password': 'ich1_password_ilovedbs',
'database': 'ich_edit'}
connection = mysql.connector.connect(**dbconfig)

cursor = connection.cursor()


try: 
    cursor.execute(f"Select * from Users")
    result = cursor.fetchall()
    for user in result:
        print(f"{user[0]}: {user[1]}")
except mysql.connector.Error as e:
    print(f"Database error {e}")

select_user = input("Select the id of the user: ")

query = """
SELECT prod, quantity 
from Products
JOIN Sales on Products.pid = Sales.pid
Where Sales.id = %s"""

cursor.execute(query, params=(select_user,))
purchases = cursor.fetchall()
if purchases:
    for purchase in purchases:
        print(f"product: {purchase[0]}")

cursor.close()
connection.close()


