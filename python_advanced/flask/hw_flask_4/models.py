# from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
# from sqlalchemy.orm import declarative_base, relationship

# #Creating base class for all models
# Base = declarative_base()

# class Category(Base):
#     __tablename__ = 'categories'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#     decription = Column(String, nullable=True)
#     products = relationship('Product', back_populates='category', lazy='joined', cascade='all, delete-orphan')

#     def __repr__(self):
#         return f"<Category(id={self.id}, name='{self.name}')>"
    

# class Product(Base):
#     __tablename__ = 'products'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     price = Column(Float, nullable=False)
#     in_stock = Column(Boolean, default=True)
#     Category.id = Column(Integer, ForeignKey('categorie.id'), nullable=False)
#     category =relationship('Category', back_populates='products')

#     def __repr__(self):
#         return f"<Products(id={self.id}, name='{self.name}', price={self.price})>"
    
# models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Базовый класс для всех моделей
Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    products = relationship('Product', back_populates='category', lazy='joined', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)

    # --- ИСПРАВЛЕННАЯ СТРОКА ---
    # category_id - это имя колонки в таблице 'products'
    # 'categories.id' - это ссылка на таблицу 'categories' и её колонку 'id'
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    # Это отношение SQLAlchemy для удобного доступа к объекту Category
    category = relationship('Category', back_populates='products')

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"