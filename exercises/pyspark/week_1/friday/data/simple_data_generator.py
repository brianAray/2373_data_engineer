# Run this once to create your practice file
with open("raw_sales.csv", "w") as f:
    f.write("transaction_id,item_name,price,quantity\n") # Header
    f.write("T101,Widget_A,15.50,2\n")
    f.write("T102,Widget_B,ERROR,5\n") # Dirty data
    f.write("T103,Widget_A,10.00,1\n")
    f.write("T104,REFUND,0.00,0\n")    # To be filtered
    f.write("T105,Widget_C,25.99,NaN\n") # More dirty data
    f.write("T106,Widget_B,12.50,10\n")
print("raw_sales.csv created.")