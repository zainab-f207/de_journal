# print("Hello Data World")
# print("This is my first Data Engineering script")
# order_id=1
# customer_name="John Doe"
# amount=100.50
# print("Order:",order_id,"Customer:",customer_name,"Amount:$",amount)
# print("Type of amount is: ", type(amount))


# Control flow
# values = [49.99, 120.50, 15.00]
# for value in values:
#     if value >100:
#         print("High value order:", value)
#     elif 20<value<100:
#         print("Medium value order:", value)
#     else:
#         print("Low value order:", value)

# Functions
# def classify_order(amount):
#     if amount > 100:
#         return "High value order"
#     elif 20 < amount <= 100:
#         return "Medium value order"
#     else:
#         return "Low value order"

# amounts = [49.99, 120.50, 15.00]
# for amount in amounts:
#     result=classify_order(amount)
#     print (amount, "->", result)

# new_value=classify_order(100)
# print("The classification for 100 is:", new_value)

# Combined version
# import csv

# def classify_order(amount):
#     if amount > 100:
#         return "High value order"
#     elif 20 < amount <= 100:
#         return "Medium value order"
#     else:
#         return "Low value order"
    
# with open("sample_orders.csv","r") as file:
#     reader= csv.DictReader(file)
#     for row in reader:
#         amount=row["amount"]
#         name= row["customer_name"]
#         result=classify_order(amount)
#         print("Customer:", name, "Amount:", amount, "->", result)

# Writing into File
# import csv
# def classify_order(amount):
#     if amount>100:
#         return "High order value"
#     elif 20 < amount <=100:
#         return "Medium order value"
#     else:
#         return "Low order value"

# with open("sample_orders.csv", "r") as infile, open("classified_orders.csv","w",newline="") as outfile:
#     reader = csv.DictReader(infile)
#     fieldname=["order_id", "customer_name", "amount", "classification"]
#     writer=csv.DictWriter(outfile,fieldnames=fieldname)
#     writer.writeheader()

#     for row in reader:
#         amount = float(row["amount"])
#         classification = classify_order(amount)
#         writer.writerow({
#             "order_id" : row["order_id"],
#             "customer_name": row["customer_name"],
#             "amount": amount,
#             "classification": classification
#         })
# print("Done — check classified_orders.csv")

# Try/Except
import csv
def classify_order(amount):
    if amount>100:
        return "High order value"
    elif 20 < amount <=100:
        return "Medium order value"
    else:
        return "Low order value"

with open("sample_orders.csv", "r") as infile, open("classified_orders.csv","w",newline="") as outfile:
    reader = csv.DictReader(infile)
    fieldname=["order_id", "customer_name", "amount", "classification"]
    writer=csv.DictWriter(outfile,fieldnames=fieldname)
    writer.writeheader()

    for row in reader:
        try:
            amount = float(row["amount"])
            classification = classify_order(amount)
            writer.writerow({
                "order_id" : row["order_id"],
                "customer_name": row["customer_name"],
                "amount": amount,
                "classification": classification
            })
            print("Customer:", row["customer_name"], ", Amount:", amount, "->", classification)
        except ValueError:
            print(f"Skipping invalid amount value for order_id {row['order_id']}: {row['amount']}")
        
print("Done — check classified_orders.csv")

