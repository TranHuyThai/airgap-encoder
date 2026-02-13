# data_processor.py
import random
import json
from datetime import datetime
from collections import defaultdict


def generate_sample_data(num_records=100):
    """Generate random sample data"""
    data = []
    cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Berlin"]
    products = ["Widget A", "Gadget B", "Tool C", "Device D"]

    for i in range(num_records):
        record = {
            "id": i + 1,
            "customer_id": f"CUST{random.randint(1000, 9999)}",
            "city": random.choice(cities),
            "product": random.choice(products),
            "quantity": random.randint(1, 50),
            "price": round(random.uniform(10.0, 500.0), 2),
            "timestamp": datetime.now().isoformat(),
        }
        data.append(record)

    return data


def analyze_data(data):
    """Analyze the generated data"""
    analysis = defaultdict(list)
    total_revenue = 0

    for record in data:
        revenue = record["quantity"] * record["price"]
        total_revenue += revenue
        analysis[record["city"]].append(revenue)
        analysis[record["product"]].append(record["quantity"])

    print(f"Total Records: {len(data)}")
    print(f"Total Revenue: ${total_revenue:,.2f}")

    print("\nAverage Revenue by City:")
    for city, revenues in list(analysis.items())[:5]:
        if city in ["New York", "London", "Tokyo", "Paris", "Sydney", "Berlin"]:
            avg = sum(revenues) / len(revenues) if revenues else 0
            print(f"  {city}: ${avg:,.2f}")

    return analysis


def save_to_json(data, filename="data_output.json"):
    """Save data to JSON file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nData saved to {filename}")


if __name__ == "__main__":
    print("=== Data Processor ===")
    sample_data = generate_sample_data(50)
    analysis = analyze_data(sample_data)
    save_to_json(sample_data)

# data_processor.py
import random
import json
from datetime import datetime
from collections import defaultdict


def generate_sample_data(num_records=100):
    """Generate random sample data"""
    data = []
    cities = ["New York", "London", "Tokyo", "Paris", "Sydney", "Berlin"]
    products = ["Widget A", "Gadget B", "Tool C", "Device D"]

    for i in range(num_records):
        record = {
            "id": i + 1,
            "customer_id": f"CUST{random.randint(1000, 9999)}",
            "city": random.choice(cities),
            "product": random.choice(products),
            "quantity": random.randint(1, 50),
            "price": round(random.uniform(10.0, 500.0), 2),
            "timestamp": datetime.now().isoformat(),
        }
        data.append(record)

    return data


def analyze_data(data):
    """Analyze the generated data"""
    analysis = defaultdict(list)
    total_revenue = 0

    for record in data:
        revenue = record["quantity"] * record["price"]
        total_revenue += revenue
        analysis[record["city"]].append(revenue)
        analysis[record["product"]].append(record["quantity"])

    print(f"Total Records: {len(data)}")
    print(f"Total Revenue: ${total_revenue:,.2f}")

    print("\nAverage Revenue by City:")
    for city, revenues in list(analysis.items())[:5]:
        if city in ["New York", "London", "Tokyo", "Paris", "Sydney", "Berlin"]:
            avg = sum(revenues) / len(revenues) if revenues else 0
            print(f"  {city}: ${avg:,.2f}")

    return analysis


def save_to_json(data, filename="data_output.json"):
    """Save data to JSON file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nData saved to {filename}")


if __name__ == "__main__":
    print("=== Data Processor ===")
    sample_data = generate_sample_data(50)
    analysis = analyze_data(sample_data)
    save_to_json(sample_data)
