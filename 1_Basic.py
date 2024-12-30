"""
Basic Queries
1. List all unique cities where customers are located.
2. Count the number of orders placed in 2017.
3. Find the total sales per category.
4. Calculate the percentage of orders that were paid in installments.
5. Count the number of customers from each state.

"""
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

db = mysql.connector.connect(
    host="localhost",
    user="Kavish",
    password="Theboss@2019",
    database="e_commerce"
)

cursor = db.cursor()

# 1. List all unique cities where customers are located.
query_1 = ("SELECT DISTINCT(customer_city) AS Unique_cities "
         "FROM customers")

cursor.execute(query_1)
data_unique_cities = cursor.fetchall()

print("---------------------------------------------------------------------------------------------------")
print("Unique cities: {}".format(data_unique_cities))

# 2. Count the number of orders placed in 2017.
query_2 = """
SELECT COUNT(order_purchase_timestamp) AS Counting
FROM orders
WHERE Year(order_approved_at) = 2017;
"""

cursor.execute(query_2)
data = cursor.fetchall()

print("---------------------------------------------------------------------------------------------------")
print("Number of orders placed in the year 2017 are: {}".format(data[0][0]))
print("---------------------------------------------------------------------------------------------------")

# 3. Find the total sales per category.
query_3 = """
SELECT LOWER(product_category), SUM(payment_value) AS "Total Sales"
FROM order_items AS oi
INNER JOIN payments AS p ON
oi.order_id = p.order_id
INNER JOIN products AS pr
ON pr.product_id = oi.product_id
WHERE product_category IS NOT NULL
GROUP BY product_category;
"""

cursor.execute(query_3)
data = cursor.fetchall()
# df = pd.DataFrame(data, columns=["Product_Category", "Sales"])
# print(df)
for product_category, sales in data:
    print("{0:50} - ${1:.2f}".format(product_category, sales))
print("---------------------------------------------------------------------------------------------------")
# 4. Calculate the percentage of orders that were paid in installments.

query_4 = """
SELECT (COUNT(payment_installments)/(SELECT COUNT(*) AS Total_payments FROM payments))*100 AS "pay_done_in_installment_%"
FROM payments
WHERE payment_installments >= 1;
"""

cursor.execute(query_4)
data = cursor.fetchall()

print("Payments made via installments are: {}%".format(data[0][0]))

print("---------------------------------------------------------------------------------------------------")
# 5. Count the number of customers from each state.


query_5 = """SELECT customer_state, COUNT(*) AS State_Count
FROM customers
GROUP BY customer_state
ORDER BY State_Count DESC;
"""

cursor.execute(query_5)
data = cursor.fetchall()

print("Customers per each State:")
for state, count in data:
    print("{}) - {}".format(state, count))

states_df = pd.DataFrame(data, columns=["State", "Customers"])
print(states_df)

plt.figure(figsize=(12, 6))  # Adjust the size of the figure
plt.bar(states_df["State"], states_df["Customers"], color='skyblue', edgecolor='black')

plt.title("Number of Customers from Each State", fontsize=16, fontweight='bold')
plt.xlabel("State", fontsize=12)
plt.ylabel("Number of Customers", fontsize=12)

plt.xticks(rotation=45, fontsize=10, ha='right')  # Rotate and align for readability
plt.yticks(fontsize=10)

plt.grid(axis='y', linestyle='--', alpha=0.7)

for index, value in enumerate(states_df["Customers"]):
    plt.text(index, value + 500, str(value), ha='center', fontsize=8, color='black')

plt.tight_layout()
plt.show()

print("---------------------------------------------------------------------------------------------------")
