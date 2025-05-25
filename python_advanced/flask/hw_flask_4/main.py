# main.py
from database import create_tables
from seed_data import seed_initial_data
from crud_operations import (
    read_all_data,
    update_product_price,
    get_product_counts_by_category,
    get_categories_with_multiple_products
)

def run_app():

    # 1. Creating tables
    create_tables()

    # 2. Filling data
    seed_initial_data()

    # 3. Reading data
    read_all_data()

    # 4. Update data
    update_product_price("Smartphone", 349.99)
    read_all_data() # reading again to be sure that the function worked 

    # 5. Aggregation and grouping
    get_product_counts_by_category()

    # 6. Grouping and filtration
    get_categories_with_multiple_products()

    print("\n--- Application finished operation---")

if __name__ == "__main__":
    run_app()