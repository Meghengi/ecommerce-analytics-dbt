"""
Generates synthetic seed data for the ecommerce-analytics-dbt demo project.

All data is fully synthetic (randomly generated), written with no
third-party dependencies (stdlib only) so this script runs anywhere with
plain Python 3. Output lands in ../seeds/ as dbt seed CSVs.

Run:
    python3 generate_seed_data.py
"""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)  # deterministic output so the repo's data is reproducible

SEED_DIR = Path(__file__).resolve().parent.parent / "seeds"
SEED_DIR.mkdir(exist_ok=True)

FIRST_NAMES = [
    "Olivia", "Liam", "Emma", "Noah", "Ava", "Elijah", "Sophia", "James",
    "Isabella", "Benjamin", "Mia", "Lucas", "Charlotte", "Henry", "Amelia",
    "Alexander", "Harper", "Daniel", "Evelyn", "Michael", "Abigail", "Ethan",
    "Emily", "Jacob", "Elizabeth", "Logan", "Sofia", "Jackson", "Avery",
    "Sebastian",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson",
]
STATES = ["CA", "TX", "NY", "FL", "WA", "IL", "PA", "OH", "GA", "NC", "MA", "CO"]
CHANNELS = ["organic_search", "paid_social", "email", "referral", "direct", "paid_search"]

CATEGORIES = {
    "Outdoor": ["Trail Backpack", "Insulated Water Bottle", "Camp Lantern", "Rain Shell Jacket", "Trekking Poles"],
    "Home": ["Ceramic Mug Set", "Linen Throw Blanket", "Cast Iron Skillet", "Standing Desk Mat", "Air Plant Holder"],
    "Fitness": ["Adjustable Dumbbell Set", "Yoga Mat", "Resistance Band Kit", "Foam Roller", "Jump Rope"],
    "Electronics": ["Wireless Earbuds", "USB-C Charging Hub", "Mechanical Keyboard", "Portable SSD 1TB", "Smart Plug 2-Pack"],
    "Office": ["Ergonomic Chair Cushion", "Monitor Stand", "Notebook 3-Pack", "Desk Organizer", "Fountain Pen"],
}

STATUSES = ["completed", "completed", "completed", "completed", "refunded", "cancelled"]  # weighted


def random_date(start: date, end: date) -> date:
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def gen_customers(n=400):
    start_signup = date(2024, 1, 1)
    end_signup = date(2025, 12, 31)
    rows = []
    for i in range(1, n + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        signup = random_date(start_signup, end_signup)
        rows.append({
            "customer_id": i,
            "first_name": first,
            "last_name": last,
            "email": f"{first.lower()}.{last.lower()}{i}@example.com",
            "state": random.choice(STATES),
            "signup_date": signup.isoformat(),
            "marketing_channel": random.choice(CHANNELS),
        })
    return rows


def gen_products():
    rows = []
    pid = 1
    for category, names in CATEGORIES.items():
        for name in names:
            cost = round(random.uniform(4, 60), 2)
            margin = random.uniform(1.6, 3.2)
            price = round(cost * margin, 2)
            rows.append({
                "product_id": pid,
                "product_name": name,
                "category": category,
                "unit_cost": cost,
                "unit_price": price,
                "is_active": 1 if random.random() > 0.08 else 0,
            })
            pid += 1
    return rows


def gen_orders_and_items(customers, products, n_orders=2200):
    start_order = date(2024, 2, 1)
    end_order = date(2025, 12, 31)
    order_rows, item_rows = [], []
    item_id = 1
    for order_id in range(1, n_orders + 1):
        customer = random.choice(customers)
        signup = date.fromisoformat(customer["signup_date"])
        order_window_start = max(signup, start_order)
        if order_window_start > end_order:
            order_window_start = end_order
        order_date = random_date(order_window_start, end_order)
        status = random.choice(STATUSES)
        n_items = random.choices([1, 2, 3, 4], weights=[45, 30, 17, 8])[0]
        chosen_products = random.sample(products, k=min(n_items, len(products)))

        order_rows.append({
            "order_id": order_id,
            "customer_id": customer["customer_id"],
            "order_date": order_date.isoformat(),
            "status": status,
            "shipping_cost": round(random.choice([0, 0, 4.99, 6.99, 9.99]), 2),
        })

        for product in chosen_products:
            qty = random.choices([1, 1, 1, 2, 3], weights=[55, 20, 15, 7, 3])[0]
            item_rows.append({
                "order_item_id": item_id,
                "order_id": order_id,
                "product_id": product["product_id"],
                "quantity": qty,
                "unit_price_at_purchase": product["unit_price"],
            })
            item_id += 1

    return order_rows, item_rows


def write_csv(rows, filename):
    path = SEED_DIR / filename
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows):>5} rows -> {path.relative_to(SEED_DIR.parent)}")


def main():
    customers = gen_customers()
    products = gen_products()
    orders, order_items = gen_orders_and_items(customers, products)

    write_csv(customers, "raw_customers.csv")
    write_csv(products, "raw_products.csv")
    write_csv(orders, "raw_orders.csv")
    write_csv(order_items, "raw_order_items.csv")


if __name__ == "__main__":
    main()
