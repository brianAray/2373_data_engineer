import random

# CONFIGURATION
FILE_NAME = "raw_sales.csv"
NUM_RECORDS = 10000 
ITEMS = ["Widget_A", "Widget_B", "Widget_C", "Gadget_X", "Device_Y"]

with open(FILE_NAME, "w") as f:
    f.write("transaction_id,item_name,price,quantity\n")
    
    for i in range(NUM_RECORDS):
        txn_id = f"T{1000 + i}"
        item = random.choice(ITEMS)
        
        price = round(random.uniform(10.0, 100.0), 2)
        quantity = random.randint(1, 20)
        
        dice_roll = random.random()
        
        if dice_roll < 0.02:    # 2% chance of 'ERROR' string in price
            price_str = "ERROR"
            qty_str = str(quantity)
        elif dice_roll < 0.04:  # 2% chance of 'NaN' in quantity
            price_str = str(price)
            qty_str = "NaN"
        elif dice_roll < 0.06:  # 2% chance of being a 'REFUND'
            item = "REFUND"
            price_str = "0.00"
            qty_str = "0"
        else:                   # 94% chance of clean data
            price_str = str(price)
            qty_str = str(quantity)

        f.write(f"{txn_id},{item},{price_str},{qty_str}\n")

print(f"Done! {FILE_NAME} created with {NUM_RECORDS} rows.")