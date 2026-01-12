# E-Commerce Database - Testing Environment

A realistic SQL database simulating a complete e-commerce company, designed for testing business SQL scripts and analytics queries.

## Database Overview

**Database Type:** SQLite
**Database File:** `ecommerce.db`
**Total Tables:** 15
**Sample Data:** Thousands of realistic records

## Database Schema

### Core Business Tables

#### **Departments** (8 records)
- `department_id` - Primary key
- `department_name` - Sales, Marketing, IT, HR, Finance, etc.
- `manager_id` - Department manager
- `budget` - Department budget

#### **Employees** (150 records)
- `employee_id` - Primary key
- `first_name`, `last_name`, `email`
- `department_id` - Foreign key to departments
- `position` - Job title
- `salary` - Employee salary
- `hire_date` - Date of hiring
- `manager_id` - Reports to employee

#### **Customers** (2,000 records)
- `customer_id` - Primary key
- `first_name`, `last_name`, `email`, `phone`
- `address`, `city`, `state`, `country`, `postal_code`
- `registration_date` - Account creation date
- `loyalty_points` - Reward points
- `is_active` - Account status

#### **Suppliers** (50 records)
- `supplier_id` - Primary key
- `supplier_name`, `contact_name`
- `email`, `phone`, `address`
- `rating` - Supplier rating (3.0-5.0)

#### **Categories** (20 records)
- `category_id` - Primary key
- `category_name` - Product category
- `parent_category_id` - For hierarchical categories
- `description` - Category description

#### **Products** (500 records)
- `product_id` - Primary key
- `product_name`, `sku`
- `category_id` - Foreign key to categories
- `supplier_id` - Foreign key to suppliers
- `unit_price` - Selling price
- `cost_price` - Cost from supplier
- `description` - Product details

#### **Inventory** (500 records)
- `inventory_id` - Primary key
- `product_id` - Foreign key to products
- `warehouse_location` - Storage location
- `quantity_on_hand` - Current stock
- `reorder_level` - Minimum stock threshold
- `reorder_quantity` - Quantity to reorder

#### **Orders** (3,000 records)
- `order_id` - Primary key
- `customer_id` - Foreign key to customers
- `employee_id` - Sales representative
- `order_date` - Order placement date
- `order_status` - Pending, Processing, Shipped, Delivered, Cancelled
- `total_amount` - Order total with tax and shipping
- `payment_method` - Payment type
- `ship_address`, `ship_city`, `ship_state`, etc.

#### **Order Items** (Variable records)
- `order_item_id` - Primary key
- `order_id` - Foreign key to orders
- `product_id` - Foreign key to products
- `quantity` - Number of units
- `unit_price` - Price at time of order
- `discount` - Discount percentage
- `subtotal` - Line item total

#### **Payments** (Thousands of records)
- `payment_id` - Primary key
- `order_id` - Foreign key to orders
- `payment_date` - Payment timestamp
- `payment_method` - Payment type
- `amount` - Payment amount
- `transaction_id` - Payment gateway transaction ID
- `payment_status` - Completed, Pending, Failed

#### **Shipping** (Thousands of records)
- `shipping_id` - Primary key
- `order_id` - Foreign key to orders
- `carrier` - FedEx, UPS, DHL, USPS
- `tracking_number` - Shipment tracking ID
- `shipping_date`, `estimated_delivery`, `actual_delivery`
- `shipping_status` - Processing, In Transit, Delivered

#### **Product Reviews** (1,500 records)
- `review_id` - Primary key
- `product_id` - Foreign key to products
- `customer_id` - Foreign key to customers
- `rating` - 1-5 stars
- `review_title`, `review_text`
- `is_verified_purchase` - Verified buyer
- `helpful_count` - Number of helpful votes

#### **Promotions** (25 records)
- `promotion_id` - Primary key
- `promotion_name`, `promotion_code`
- `discount_type` - Percentage, Fixed Amount, Free Shipping
- `discount_value` - Discount amount
- `start_date`, `end_date` - Promotion period
- `usage_limit`, `times_used` - Usage tracking

## Getting Started

### Prerequisites
```bash
# Install required Python packages
pip install -r requirements.txt
```

### Generate the Database
```bash
# Run the data generation script
python generate_data.py
```

This will create `ecommerce.db` with all tables populated.

### Connect to Database

#### Using SQLite Command Line
```bash
sqlite3 ecommerce.db
```

#### Using Python
```python
import sqlite3

conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Run your queries
cursor.execute("SELECT * FROM products LIMIT 5")
results = cursor.fetchall()

conn.close()
```

#### Using DB Browser for SQLite
1. Download [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open `ecommerce.db`
3. Browse data and run queries

## Example Queries

The `example_queries.sql` file contains 25+ business analytics queries including:

### Sales Analysis
- Total revenue by month
- Best-selling products
- Revenue by category
- Sales growth rate

### Customer Analysis
- Top customers by spend
- Customer retention and segments
- Geographic distribution
- Customer Lifetime Value (CLV)
- Churn analysis

### Inventory Management
- Low stock alerts
- Inventory value by warehouse
- Slow-moving products

### Employee Performance
- Sales by employee
- Department performance and budgets

### Product Analysis
- Profit margins
- Product ratings by category
- ABC classification (Pareto analysis)

### Order & Shipping Analysis
- Order status distribution
- Processing time metrics
- Shipping carrier performance
- Payment method analysis

### Advanced Analytics
- Cohort analysis
- Promotion effectiveness
- Supplier performance

## Database Statistics

```
Departments:     8
Employees:       150
Customers:       2,000
Suppliers:       50
Categories:      20
Products:        500
Orders:          3,000
Reviews:         1,500
Promotions:      25
```

## Key Features

- **Realistic Data**: Names, addresses, emails generated with Faker library
- **Proper Relationships**: Foreign keys maintain referential integrity
- **Historical Data**: 2-3 years of transaction history
- **Various Scenarios**:
  - Active and inactive customers/employees/products
  - Multiple order statuses (pending, processing, shipped, delivered, cancelled)
  - Different payment methods
  - Product reviews with verified purchases
  - Multiple warehouse locations
  - Hierarchical categories
  - Promotions with usage tracking

## Use Cases

Perfect for testing:
- Sales reporting and dashboards
- Customer analytics and segmentation
- Inventory management systems
- Business intelligence queries
- Data warehouse ETL processes
- Performance optimization
- SQL training and education
- Interview question practice

## Regenerating Data

To create a fresh database with new random data:

```bash
rm ecommerce.db
python generate_data.py
```

## Customization

Edit `generate_data.py` to adjust:
- Number of records per table (see configuration constants at top)
- Date ranges for historical data
- Product categories and types
- Geographic distribution
- Price ranges

## Database Indexes

Indexes are created for commonly queried fields:
- `customers.email`
- `products.sku`
- `products.category_id`
- `orders.customer_id`
- `orders.order_date`
- `order_items.order_id`
- `order_items.product_id`
- `employees.department_id`

## Tips for Testing

1. **Start with simple queries** - Explore the data with `SELECT * FROM table LIMIT 10`
2. **Check relationships** - Use JOIN queries to understand table connections
3. **Test edge cases** - Cancelled orders, inactive products, null values
4. **Performance testing** - Try complex queries with aggregations and subqueries
5. **Data integrity** - Verify foreign key relationships are maintained

## Files

- `schema.sql` - Database schema definition
- `generate_data.py` - Python script to populate database
- `example_queries.sql` - 25+ sample business queries
- `requirements.txt` - Python dependencies
- `ecommerce.db` - SQLite database file (generated)
- `README.md` - This documentation

## License

Free to use for educational and testing purposes.
