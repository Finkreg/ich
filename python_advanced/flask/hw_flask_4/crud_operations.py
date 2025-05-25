from sqlalchemy import func
from database import get_db
from models import Category, Product

def read_all_data():
    with get_db() as db:
        categories = db.query(Category).all()
        if not categories:
            print("Nocategories found")
        else:
            for  category in categories:
                print(f"Category: {category.name} (Description: {category.description})")
                if category.products:
                    for product in category.products:
                        print(f" - Product {product.name}, Price: {product.price}")
                else:
                    print("No products in this category")


def update_product_price(product_name, new_price):
    with get_db() as db:
        product = db.query(Product).filter_by(name=product_name).first()
        if product:
            product.price = new_price
            db.commit()
        else:
            print(f"no product found")

    
def get_product_counts_by_category():
    with get_db() as db:
        product_counts = db.query(Category.name, func.count(Product.id))\
                                    .join(Product)\
                                    .group_by(Category.name)\
                                    .all()
        print("Total ammount of products in each category: ")
        if not product_counts:
            print("No data to count")
        else:
            for category_name, count in product_counts:
                print(f"Category {category_name}, Products: {count}")
            return product_counts
        

def get_categories_with_multiple_products():
    with get_db() as db:
        categories_with_multiple_products = db.query(Category.name, func.count(Product.id))\
                                            .join(Product)\
                                            .group_by(Category.name)\
                                            .having(func.count(Product.id) > 1)\
                                            .all()
        print("Categories that have more than one product")
        if not categories_with_multiple_products:
            print("No categories with more than one product")
        else:
            for category_name, count in categories_with_multiple_products:
                print(f"  Category: {category_name}, Products: {count}")
        return categories_with_multiple_products
