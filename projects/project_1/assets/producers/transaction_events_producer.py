"""
Transaction Events Producer
Generates mock e-commerce transaction events and publishes them to a Kafka topic.

Usage:
    python transaction_events_producer.py --bootstrap-servers localhost:9094 --topic transaction_events --interval 2.0

Dependencies:
    pip install kafka-python faker
"""

import argparse
import json
import time
import random
from datetime import datetime
from faker import Faker
from kafka import KafkaProducer


fake = Faker()
Faker.seed(42)  # Fixed seed for reproducible user pool

# Shared user pool - generates the same 100 users when seed is fixed
# This enables joins with user_events_producer.py
USER_POOL = [Faker().uuid4()[:8] for _ in range(100)]

# Shared product pool - enables joins with user_events_producer.py
PRODUCT_POOL = [f"PROD_{1000 + i}" for i in range(200)]

TRANSACTION_TYPES = ["purchase", "refund", "chargeback"]
PAYMENT_METHODS = ["credit_card", "debit_card", "paypal", "apple_pay", "google_pay", "bank_transfer"]
CURRENCIES = ["USD", "EUR", "GBP", "CAD", "AUD"]
PRODUCT_CATEGORIES = ["electronics", "clothing", "home", "sports", "books", "toys", "food", "beauty"]
STATUSES = ["pending", "completed", "failed", "cancelled"]


def generate_product():
    """Generate a single product item."""
    category = random.choice(PRODUCT_CATEGORIES)
    return {
        "product_id": random.choice(PRODUCT_POOL),  # Select from shared pool for joinability
        "product_name": f"{fake.word().capitalize()} {category.capitalize()}",
        "category": category,
        "quantity": random.randint(1, 5),
        "unit_price": round(random.uniform(9.99, 499.99), 2)
    }


def generate_transaction_event():
    """Generate a single mock transaction event."""
    user_id = random.choice(USER_POOL)  # Select from shared pool for joinability
    transaction_type = random.choices(
        TRANSACTION_TYPES, 
        weights=[0.85, 0.12, 0.03]  # 85% purchases, 12% refunds, 3% chargebacks
    )[0]
    
    # Generate 1-5 products per transaction
    products = [generate_product() for _ in range(random.randint(1, 5))]
    subtotal = sum(p["quantity"] * p["unit_price"] for p in products)
    tax_rate = random.uniform(0.05, 0.10)
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax, 2)
    
    # For refunds/chargebacks, reference an original transaction
    original_transaction_id = None
    if transaction_type in ["refund", "chargeback"]:
        original_transaction_id = fake.uuid4()
        total = -total  # Negative amount for refunds
    
    event = {
        "transaction_id": fake.uuid4(),
        "user_id": user_id,
        "transaction_type": transaction_type,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": random.choices(STATUSES, weights=[0.05, 0.88, 0.05, 0.02])[0],
        "payment_method": random.choice(PAYMENT_METHODS),
        "currency": random.choice(CURRENCIES),
        "products": products,
        "subtotal": round(subtotal, 2),
        "tax": tax,
        "total": total,
        "billing_address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip_code": fake.zipcode(),
            "country": fake.country_code()
        },
        "shipping_address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip_code": fake.zipcode(),
            "country": fake.country_code()
        }
    }
    
    if original_transaction_id:
        event["original_transaction_id"] = original_transaction_id
    
    return event


def create_producer(bootstrap_servers):
    """Create and return a Kafka producer."""
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k else None
    )


def main():
    parser = argparse.ArgumentParser(description="Generate mock transaction events to Kafka")
    parser.add_argument("--bootstrap-servers", default="localhost:9092", help="Kafka bootstrap servers")
    parser.add_argument("--topic", default="transaction_events", help="Kafka topic name")
    parser.add_argument("--interval", type=float, default=2.0, help="Seconds between events")
    parser.add_argument("--count", type=int, default=None, help="Number of events to generate (infinite if not set)")
    args = parser.parse_args()
    
    producer = create_producer(args.bootstrap_servers)
    print(f"Connected to Kafka at {args.bootstrap_servers}")
    print(f"Publishing to topic: {args.topic}")
    print(f"Interval: {args.interval}s")
    print("-" * 50)
    
    event_count = 0
    try:
        while args.count is None or event_count < args.count:
            event = generate_transaction_event()
            key = event["user_id"]
            
            producer.send(args.topic, key=key, value=event)
            event_count += 1
            
            status_icon = "+" if event["total"] > 0 else "-"
            print(f"[{event_count}] {event['transaction_type']:12} | {status_icon}${abs(event['total']):>8.2f} | {len(event['products'])} items | {event['status']}")
            
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print(f"\nStopped. Total events published: {event_count}")
    finally:
        producer.close()


if __name__ == "__main__":
    main()
