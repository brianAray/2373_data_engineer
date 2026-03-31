import json

data = [
    {"id": 101, "info": {"name": "Alice", "city": "New York", "age": 30}},
    {"id": 102, "info": {"name": "Bob", "city": "Los Angeles", "age": 25}},
    {"id": 103, "info": {"name": "Charlie", "city": "New York", "age": 35}},
    {"id": 104, "info": {"name": "David", "city": "Chicago", "age": 40}},
    {"id": 105, "info": {"name": "Eve", "city": "Los Angeles", "age": 22}},
    {"id": 106, "info": {"name": None, "city": "Chicago", "age": 29}} # Testing Nulls
]

with open("raw_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Successfully created raw_data.json")