# 1. Вывести список таблиц в базе данных
# 2. Предоставить пользователю выбрать таблицу из предложенных:
# 3. Вывести список полей выбранной таблицы:
# 4. Позволить искать значение по определенному полю:
# 5. При вводе искомого значения добавить возможность выбора знака - найти записи в которых
# выбранное поле больше меньше или равно введеному значению.
import mysql.connector
DB = 'hr'

def call_database(data):
    global DB
    dbconfig = {'host': 'ich-db.edu.itcareerhub.de',
            'user': 'ich1',
            'password': 'password',
            'database': DB}

    connection = mysql.connector.connect(**dbconfig)

    cursor = connection.cursor()
    try:
        cursor.execute(data)
        result = cursor.fetchall()
        print("=== ***** RESULT ***** ===")
        for table in result:
            print(table)
    except mysql.connector.Error as err:
        print("Query error: ", err)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def show_databases():
    database_query = """SHOW DATABASES"""
    call_database(database_query)

def change_database():
    global DB
    new_db = input("Enter the database to connect to: ")
    DB = new_db
    print(f"Switched to database: {DB}")

def show_tables():
    all_tables_query = """SHOW TABLES"""
    call_database(all_tables_query)


def show_table_fields():
    user_selected_table = input("Please enter the name of the table: ")
    table_fields_query = f"DESCRIBE {user_selected_table}"
    call_database(table_fields_query)


def search_specific_values():
    table = input("Please enter the name of the table: ")
    field = input("Please enter the desired field to search: ")
    operator = input("Please enter the criteria '<', '>' or '=' : ")
    value = input(f"Please select the value to search within {field}: ")
    if value.isdigit():
        final_value = value
    else:
        final_value = f"'{value}'"
    user_query = f"SELECT * FROM {table} WHERE {field} {operator} {final_value}"
    call_database(user_query)


def main_menu():
    while True:
        print("\n=== Main Menu ===")
        print("1. Show all tables")
        print("2. Describe table fields")
        print("3. Search for values")
        print("4. Change database")
        print("5. Show database list")
        print("6. Exit")
        print()
        
        choice = input("Your choice: ")
        if choice == "1":
            show_tables()
        elif choice == "2":
            show_table_fields()
        elif choice == "3":
            search_specific_values()
        elif choice == "4":
            change_database()
        elif choice == "5":
            show_databases()
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")
            
main_menu()