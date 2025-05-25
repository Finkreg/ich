from sqlalchemy.exc import IntegrityError
from database import get_db
from models import Category, Product


def seed_initial_data():
    """we're adding the initial data to DB"""
    with get_db() as db:

        try:
            print("trying to seed in the data....")

            #check if the categories have already been created
            existing_electronics = db.query(Category).filter_by(name='Electronics').first()
            existing_books = db.query(Category).filter_by(name='Books').first()
            existing_clothing = db.query(Category).filter_by(name='Clothing').first()

            if not existing_electronics:
                print("Filling in the Electronics Category")
                electronics = Category(name='Electronics', description="Gadgets and stuff")
                db.add(electronics)
                # to receive the id we have to commit or update the objects
                db.flush() #updates the objects in db but does not commit

                #we're adding the products of the new category
                db.add_all([
                    Product(name='Smartphone', price=299.99, in_stock=True, category=electronics),
                    Product(name='Laptop', price=499.99, in_stock=True, category=electronics)
                ])
            else:
                print("Category 'Electronics' already exists")
                electronics = existing_electronics


            if not existing_books:
                print("Filling in the Books Category")
                books = Category(name='Books', description="Books, journals, newspapers")
                db.add(books)
                # to receive the id we have to commit or update the objects
                db.flush() #updates the objects in db but does not commit

                #we're adding the products of the new category
                db.add_all([
                    Product(name='Harry Potter set', price=199.99, in_stock=True, category=books),
                    Product(name='Lord of the Rings', price=49.50, in_stock=True, category=books)
                ])
            else:
                print("Category 'Books' already exists")
                books = existing_books

            if not existing_clothing:
                print("Filling in the Clothing Category")
                clothing = Category(name='Clothing', description="Men and women clothing")
                db.add(clothing)
                # to receive the id we have to commit or update the objects
                db.flush() #updates the objects in db but does not commit

                #we're adding the products of the new category
                db.add_all([
                    Product(name='Jeans', price=39.99, in_stock=True, category=clothing),
                    Product(name='T-shirt', price=20.00, in_stock=True, category=clothing)
                ])
            else:
                print("Category 'Clohing' already exists")
                clothing = existing_clothing

            db.commit()
            print("Finished seeding data")


        except IntegrityError:
            db.rollback()
            print("Some categories already exist or the Integrity error! Rollback")
        except Exception as e:
            db.rollback()
            print(f"Unknown error {e}. Rollback")