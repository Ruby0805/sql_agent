"""
E-Commerce Database Data Generator
Generates realistic sample data for testing business SQL scripts
"""

import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# Configuration
NUM_DEPARTMENTS = 8
NUM_EMPLOYEES = 150
NUM_CUSTOMERS = 2000
NUM_SUPPLIERS = 50
NUM_CATEGORIES = 20
NUM_PRODUCTS = 500
NUM_ORDERS = 3000
NUM_REVIEWS = 1500
NUM_PROMOTIONS = 25

def create_database():
    """Create database and execute schema"""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()

    # Read and execute schema
    with open('schema.sql', 'r') as f:
        schema = f.read()
        cursor.executescript(schema)

    conn.commit()
    return conn, cursor

def generate_departments(cursor):
    """Generate department data"""
    departments = [
        'Sales', 'Marketing', 'IT', 'Human Resources',
        'Finance', 'Operations', 'Customer Service', 'Logistics'
    ]

    for dept in departments:
        budget = random.uniform(100000, 1000000)
        cursor.execute("""
            INSERT INTO departments (department_name, budget)
            VALUES (?, ?)
        """, (dept, budget))

    print(f"✓ Generated {len(departments)} departments")

def generate_employees(cursor, num_employees):
    """Generate employee data"""
    positions = {
        1: ['VP of Sales', 'Sales Manager', 'Sales Representative'],
        2: ['Marketing Director', 'Marketing Manager', 'Marketing Specialist'],
        3: ['CTO', 'IT Manager', 'Software Developer', 'System Administrator'],
        4: ['HR Director', 'HR Manager', 'HR Coordinator'],
        5: ['CFO', 'Finance Manager', 'Accountant'],
        6: ['Operations Director', 'Operations Manager', 'Operations Analyst'],
        7: ['Customer Service Manager', 'Customer Service Representative'],
        8: ['Logistics Manager', 'Warehouse Supervisor', 'Shipping Clerk']
    }

    for i in range(num_employees):
        dept_id = random.randint(1, 8)
        position = random.choice(positions[dept_id])
        hire_date = fake.date_between(start_date='-10y', end_date='today')

        # Salary ranges by position level
        if 'VP' in position or 'Director' in position or 'CTO' in position or 'CFO' in position:
            salary = random.uniform(120000, 250000)
        elif 'Manager' in position:
            salary = random.uniform(70000, 130000)
        else:
            salary = random.uniform(40000, 85000)

        manager_id = random.randint(1, max(1, i-1)) if i > 5 and 'Representative' in position or 'Specialist' in position or 'Clerk' in position else None

        cursor.execute("""
            INSERT INTO employees (first_name, last_name, email, phone, hire_date,
                                 department_id, position, salary, manager_id, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fake.first_name(), fake.last_name(), fake.unique.email(),
            fake.phone_number(), hire_date, dept_id, position, salary,
            manager_id, random.choice([1, 1, 1, 0])  # 75% active
        ))

    print(f"✓ Generated {num_employees} employees")

def generate_customers(cursor, num_customers):
    """Generate customer data"""
    for _ in range(num_customers):
        registration_date = fake.date_time_between(start_date='-3y', end_date='now')
        last_login = fake.date_time_between(start_date=registration_date, end_date='now')

        cursor.execute("""
            INSERT INTO customers (first_name, last_name, email, phone, address, city,
                                 state, country, postal_code, registration_date, last_login,
                                 loyalty_points, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fake.first_name(), fake.last_name(), fake.unique.email(),
            fake.phone_number(), fake.street_address(), fake.city(),
            fake.state(), fake.country(), fake.postcode(),
            registration_date, last_login,
            random.randint(0, 5000), random.choice([1, 1, 1, 1, 0])  # 80% active
        ))

    print(f"✓ Generated {num_customers} customers")

def generate_suppliers(cursor, num_suppliers):
    """Generate supplier data"""
    for _ in range(num_suppliers):
        cursor.execute("""
            INSERT INTO suppliers (supplier_name, contact_name, email, phone, address,
                                 city, country, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fake.company(), fake.name(), fake.company_email(),
            fake.phone_number(), fake.street_address(), fake.city(),
            fake.country(), round(random.uniform(3.0, 5.0), 2)
        ))

    print(f"✓ Generated {num_suppliers} suppliers")

def generate_categories(cursor, num_categories):
    """Generate product categories"""
    main_categories = [
        'Electronics', 'Clothing & Apparel', 'Home & Garden', 'Sports & Outdoors',
        'Books & Media', 'Toys & Games', 'Health & Beauty', 'Food & Beverage',
        'Automotive', 'Office Supplies'
    ]

    # Insert main categories
    for cat in main_categories:
        cursor.execute("""
            INSERT INTO categories (category_name, description)
            VALUES (?, ?)
        """, (cat, fake.sentence()))

    # Insert subcategories
    subcategories = [
        (1, 'Laptops'), (1, 'Smartphones'), (1, 'Cameras'),
        (2, 'Men\'s Clothing'), (2, 'Women\'s Clothing'), (2, 'Shoes'),
        (3, 'Furniture'), (3, 'Kitchen'), (3, 'Bedding'),
        (4, 'Exercise Equipment'), (4, 'Camping Gear'), (4, 'Team Sports'),
        (5, 'Fiction'), (5, 'Non-Fiction'), (5, 'Movies'),
        (6, 'Board Games'), (6, 'Action Figures'), (6, 'Puzzles'),
        (7, 'Skincare'), (7, 'Vitamins'), (7, 'Personal Care')
    ]

    for parent_id, sub_name in subcategories[:num_categories - len(main_categories)]:
        cursor.execute("""
            INSERT INTO categories (category_name, parent_category_id, description)
            VALUES (?, ?, ?)
        """, (sub_name, parent_id, fake.sentence()))

    print(f"✓ Generated {num_categories} categories")

def generate_products(cursor, num_products):
    """Generate product data"""
    product_templates = [
        'Premium {}', 'Professional {}', 'Deluxe {}', 'Standard {}',
        'Economy {}', 'Classic {}', 'Modern {}', 'Vintage {}'
    ]

    product_types = [
        'Laptop', 'Monitor', 'Keyboard', 'Mouse', 'Headphones',
        'T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Boots',
        'Chair', 'Desk', 'Lamp', 'Bookshelf', 'Sofa',
        'Tent', 'Sleeping Bag', 'Backpack', 'Bicycle', 'Yoga Mat',
        'Novel', 'Cookbook', 'Magazine', 'DVD', 'Board Game'
    ]

    for i in range(num_products):
        product_name = random.choice(product_templates).format(random.choice(product_types))
        sku = f'SKU-{fake.unique.random_int(10000, 99999)}'
        category_id = random.randint(1, 20)
        supplier_id = random.randint(1, NUM_SUPPLIERS)

        cost_price = random.uniform(10, 500)
        unit_price = cost_price * random.uniform(1.5, 3.0)  # markup

        cursor.execute("""
            INSERT INTO products (product_name, sku, category_id, supplier_id, description,
                                unit_price, cost_price, weight, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            product_name, sku, category_id, supplier_id, fake.text(200),
            round(unit_price, 2), round(cost_price, 2), round(random.uniform(0.1, 20), 2),
            random.choice([1, 1, 1, 0])  # 75% active
        ))

    print(f"✓ Generated {num_products} products")

def generate_inventory(cursor):
    """Generate inventory data for all products"""
    cursor.execute("SELECT product_id FROM products")
    products = cursor.fetchall()

    warehouses = ['Warehouse A', 'Warehouse B', 'Warehouse C', 'Distribution Center']

    for (product_id,) in products:
        quantity = random.randint(0, 500)
        reorder_level = random.randint(10, 50)

        cursor.execute("""
            INSERT INTO inventory (product_id, warehouse_location, quantity_on_hand,
                                 reorder_level, reorder_quantity, last_restock_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            product_id, random.choice(warehouses), quantity, reorder_level,
            random.randint(50, 200), fake.date_between(start_date='-6m', end_date='today')
        ))

    print(f"✓ Generated inventory records for {len(products)} products")

def generate_orders_and_items(cursor, num_orders):
    """Generate orders and order items"""
    cursor.execute("SELECT customer_id FROM customers WHERE is_active = 1")
    customers = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT product_id, unit_price FROM products WHERE is_active = 1")
    products = cursor.fetchall()

    cursor.execute("SELECT employee_id FROM employees WHERE department_id = 1 AND is_active = 1")
    sales_employees = [row[0] for row in cursor.fetchall()]

    order_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery']

    for _ in range(num_orders):
        customer_id = random.choice(customers)
        order_date = fake.date_time_between(start_date='-2y', end_date='now')
        required_date = order_date + timedelta(days=random.randint(3, 14))

        status = random.choices(order_statuses, weights=[5, 10, 25, 55, 5])[0]
        shipped_date = order_date + timedelta(days=random.randint(1, 5)) if status in ['Shipped', 'Delivered'] else None

        # Generate shipping address
        cursor.execute("SELECT address, city, state, country, postal_code FROM customers WHERE customer_id = ?", (customer_id,))
        address_data = cursor.fetchone()

        cursor.execute("""
            INSERT INTO orders (customer_id, employee_id, order_date, required_date, shipped_date,
                              ship_address, ship_city, ship_state, ship_country, ship_postal_code,
                              order_status, payment_method)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            customer_id, random.choice(sales_employees) if sales_employees else None,
            order_date, required_date, shipped_date,
            address_data[0], address_data[1], address_data[2], address_data[3], address_data[4],
            status, random.choice(payment_methods)
        ))

        order_id = cursor.lastrowid

        # Generate order items
        num_items = random.randint(1, 8)
        selected_products = random.sample(products, min(num_items, len(products)))

        order_total = 0
        for product_id, unit_price in selected_products:
            quantity = random.randint(1, 5)
            discount = random.choice([0, 0, 0, 5, 10, 15])  # Most items no discount
            subtotal = unit_price * quantity * (1 - discount / 100)
            order_total += subtotal

            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (order_id, product_id, quantity, unit_price, discount, round(subtotal, 2)))

        # Update order totals
        tax_rate = 0.08
        shipping_fee = random.choice([0, 5.99, 9.99, 14.99])
        tax_amount = order_total * tax_rate
        total_amount = order_total + tax_amount + shipping_fee

        cursor.execute("""
            UPDATE orders SET total_amount = ?, tax_amount = ?, shipping_fee = ?
            WHERE order_id = ?
        """, (round(total_amount, 2), round(tax_amount, 2), shipping_fee, order_id))

        # Generate payment record for completed orders
        if status != 'Cancelled':
            payment_status = 'Completed' if status in ['Processing', 'Shipped', 'Delivered'] else 'Pending'
            cursor.execute("""
                INSERT INTO payments (order_id, payment_date, payment_method, amount,
                                    transaction_id, payment_status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                order_id, order_date, random.choice(payment_methods),
                round(total_amount, 2), fake.uuid4(), payment_status
            ))

        # Generate shipping record for shipped/delivered orders
        if status in ['Shipped', 'Delivered']:
            carriers = ['FedEx', 'UPS', 'DHL', 'USPS']
            estimated_delivery = shipped_date + timedelta(days=random.randint(3, 7))
            actual_delivery = estimated_delivery if status == 'Delivered' else None

            cursor.execute("""
                INSERT INTO shipping (order_id, carrier, tracking_number, shipping_date,
                                    estimated_delivery, actual_delivery, shipping_status, shipping_cost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order_id, random.choice(carriers), fake.uuid4()[:16],
                shipped_date.date(), estimated_delivery.date(),
                actual_delivery.date() if actual_delivery else None,
                'Delivered' if status == 'Delivered' else 'In Transit',
                shipping_fee
            ))

    print(f"✓ Generated {num_orders} orders with items, payments, and shipping records")

def generate_reviews(cursor, num_reviews):
    """Generate product reviews"""
    cursor.execute("""
        SELECT DISTINCT o.customer_id, oi.product_id
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_status = 'Delivered'
        ORDER BY RANDOM()
        LIMIT ?
    """, (num_reviews,))

    review_combinations = cursor.fetchall()

    for customer_id, product_id in review_combinations:
        rating = random.choices([1, 2, 3, 4, 5], weights=[2, 3, 10, 35, 50])[0]

        review_titles = {
            5: ['Excellent product!', 'Love it!', 'Highly recommend', 'Perfect!'],
            4: ['Very good', 'Happy with purchase', 'Good quality', 'Worth it'],
            3: ['It\'s okay', 'Average', 'Decent product', 'As expected'],
            2: ['Disappointed', 'Not great', 'Expected better', 'Below average'],
            1: ['Terrible', 'Waste of money', 'Do not buy', 'Very poor quality']
        }

        cursor.execute("""
            INSERT INTO product_reviews (product_id, customer_id, rating, review_title,
                                        review_text, is_verified_purchase, helpful_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            product_id, customer_id, rating,
            random.choice(review_titles[rating]),
            fake.paragraph(nb_sentences=random.randint(2, 5)),
            1, random.randint(0, 50)
        ))

    print(f"✓ Generated {num_reviews} product reviews")

def generate_promotions(cursor, num_promotions):
    """Generate promotional offers"""
    promo_types = [
        ('Percentage', 'SAVE{}', 10, 50),
        ('Fixed Amount', 'GET{}OFF', 5, 100),
        ('Free Shipping', 'FREESHIP', 0, 0)
    ]

    for i in range(num_promotions):
        discount_type, code_template, min_val, max_val = random.choice(promo_types)

        if discount_type == 'Free Shipping':
            discount_value = 0
            code = f'{code_template}{i}'
        else:
            discount_value = random.randint(min_val, max_val)
            code = f'{code_template.format(discount_value)}{i}'

        start_date = fake.date_between(start_date='-1y', end_date='today')
        end_date = fake.date_between(start_date=start_date, end_date='+6m')

        cursor.execute("""
            INSERT INTO promotions (promotion_name, promotion_code, discount_type, discount_value,
                                  start_date, end_date, min_purchase_amount, max_discount_amount,
                                  usage_limit, times_used, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            fake.catch_phrase(), code, discount_type, discount_value,
            start_date, end_date, random.choice([0, 25, 50, 100]),
            random.choice([None, 50, 100, 200]), random.randint(100, 10000),
            random.randint(0, 500), random.choice([1, 1, 0])
        ))

    print(f"✓ Generated {num_promotions} promotions")

def main():
    """Main function to generate all data"""
    print("Starting E-Commerce Database Generation...")
    print("=" * 60)

    try:
        conn, cursor = create_database()
        print("✓ Database and schema created")

        generate_departments(cursor)
        generate_employees(cursor, NUM_EMPLOYEES)
        generate_customers(cursor, NUM_CUSTOMERS)
        generate_suppliers(cursor, NUM_SUPPLIERS)
        generate_categories(cursor, NUM_CATEGORIES)
        generate_products(cursor, NUM_PRODUCTS)
        generate_inventory(cursor)
        generate_orders_and_items(cursor, NUM_ORDERS)
        generate_reviews(cursor, NUM_REVIEWS)
        generate_promotions(cursor, NUM_PROMOTIONS)

        conn.commit()
        conn.close()

        print("=" * 60)
        print("✓ Database generation completed successfully!")
        print(f"✓ Database file: ecommerce.db")
        print("\nDatabase Statistics:")
        print(f"  - Departments: {NUM_DEPARTMENTS}")
        print(f"  - Employees: {NUM_EMPLOYEES}")
        print(f"  - Customers: {NUM_CUSTOMERS}")
        print(f"  - Suppliers: {NUM_SUPPLIERS}")
        print(f"  - Categories: {NUM_CATEGORIES}")
        print(f"  - Products: {NUM_PRODUCTS}")
        print(f"  - Orders: {NUM_ORDERS}")
        print(f"  - Reviews: {NUM_REVIEWS}")
        print(f"  - Promotions: {NUM_PROMOTIONS}")

    except Exception as e:
        print(f"✗ Error: {e}")
        raise

if __name__ == '__main__':
    main()
