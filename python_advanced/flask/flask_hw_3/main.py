from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, create_engine, Boolean
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.
engine = create_engine('sqlite///test.db')
Base = declarative_base()

# Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.
Session = sessionmaker(bind=engine)
session = Session()

# Задача 3: Определите модель продукта Product со следующими типами колонок:
#     id: числовой идентификатор
#     name: строка (макс. 100 символов)
#     price: числовое значение с фиксированной точностью
#     in_stock: логическое значение
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Numeric(10, 2))
    in_stock = Column(Boolean)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', backref='products')


# Задача 4: Определите связанную модель категории Category со следующими типами колонок:
#     id: числовой идентификатор
#     name: строка (макс. 100 символов)
#     description: строка (макс. 255 символов)
# Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id.
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(250))

