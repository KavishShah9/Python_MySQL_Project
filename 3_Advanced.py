"""
Advanced Queries
11. Calculate the moving average of order values for each customer over their order history. (3 months)
12. Calculate the cumulative sales per month for each year.
13. Calculate the year-over-year growth rate of total sales.
14. Identify the top 3 customers who spent the most money in each year.
"""

import mysql.connector
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

db = mysql.connector.connect(
    host="localhost",
    user="Kavish",
    password="Theboss@2019",
    database="e_commerce"
)

cursor = db.cursor()

# print("------------------------------------------------------------------------------------------------")
#
# query_11 = """
# SELECT customer_id, order_purchase_timestamp, payment,
# AVG(payment) OVER(PARTITION BY customer_id ORDER BY order_purchase_timestamp
# ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS mov_avg
# FROM
# (SELECT orders.customer_id, orders.order_purchase_timestamp,
#  payments.payment_value AS payment
#  FROM payments JOIN orders
#  ON payments.order_id = orders.order_id) AS a
# """
#
# cursor.execute(query_11)
# data = cursor.fetchall()
#
# df = pd.DataFrame(data, columns=["Customer_ID", "Date_Time", "$", "Moving_Avg"])
# print(df)
# print("------------------------------------------------------------------------------------------------")
#
# query_12 = """
# SELECT years, months, payment, ROUND(SUM(payment)
# OVER(PARTITION BY years ORDER BY years, months), 2) AS cumulative_sales
# FROM
# (SELECT YEAR(orders.order_purchase_timestamp) AS years,
#         MONTH(orders.order_purchase_timestamp) AS months,
#         ROUND(SUM(payments.payment_value), 2) AS payment
#  FROM orders
#  JOIN payments
#  ON orders.order_id = payments.order_id
#  GROUP BY years, months
#  ORDER BY years, months) AS a;
# """
#
# cursor.execute(query_12)
# data = cursor.fetchall()
#
# df = pd.DataFrame(data, columns=["Years", "Months", "Payments", "Cumulative Sales"])
# print(df)
#
# # Plotting
# plt.figure(figsize=(14, 7))
#
# # Plot cumulative sales as a line graph
# plt.plot(df["Months"] + (df["Years"] - df["Years"].min()) * 12,  # Create a continuous x-axis using months
#          df["Cumulative Sales"], label="Cumulative Sales", color='blue', linewidth=2)
#
# # Plot monthly payments as a bar graph
# plt.bar(df["Months"] + (df["Years"] - df["Years"].min()) * 12,
#         df["Payments"], label="Monthly Payments", color='orange', alpha=0.6)
#
# # Add titles and labels
# plt.title("Monthly Payments and Cumulative Sales Over Time", fontsize=16, fontweight='bold')
# plt.xlabel("Time (Months)", fontsize=12)
# plt.ylabel("Amount (in currency units)", fontsize=12)
#
# # Add legend
# plt.legend(fontsize=12)
#
# # Enhance x-axis with year labels
# x_ticks = np.arange(df["Months"].min(), (df["Years"].max() - df["Years"].min() + 1) * 12 + 1, 3)
# x_labels = [f"{(tick - 1) % 12 + 1}-{df['Years'].min() + (tick - 1) // 12}" for tick in x_ticks]
# plt.xticks(ticks=x_ticks, labels=x_labels, rotation=45, ha='right', fontsize=10)
#
# # Add grid lines
# plt.grid(axis='y', linestyle='--', alpha=0.7)
#
# # Show the plot
# plt.tight_layout()
# plt.show()
#
# print("------------------------------------------------------------------------------------------------")
#
# query_13 = """
# SELECT YEAR(o.order_purchase_timestamp) AS Years, ROUND(SUM(p.payment_value), 2) AS Sales
# FROM orders AS o
# INNER JOIN
# payments AS p ON
# p.order_id = o.order_id
# GROUP BY Years
# ORDER BY Years;
# """
#
# cursor.execute(query_13)
# data = cursor.fetchall()
#
# df = pd.DataFrame(data, columns=["Years", "Sales"])
# print(df)
# print()
#
# sales = df["Sales"]
# years = df["Years"]
#
# for x in range(3):
#     if 1 <= x <= 2:
#         print("For year {0}, % increase in sales was : {1:.2f} %"
#               .format(years[x],100 * (sales.iloc[x] - sales.iloc[x - 1])/sales.iloc[x - 1]))
#
print("------------------------------------------------------------------------------------------------")

query_14 = """
WITH CTE AS 
(SELECT c.customer_id, YEAR(order_purchase_timestamp) AS Years, SUM(p.payment_value) AS payments,
RANK() OVER(PARTITION BY YEAR(order_purchase_timestamp) ORDER BY SUM(p.payment_value) DESC) AS Ranking
FROM orders AS o
INNER JOIN payments AS p
ON p.order_id = o.order_id
INNER JOIN customers AS c
ON c.customer_id = o.customer_id
GROUP BY Years, c.customer_id
ORDER BY Years)

SELECT customer_id, Years, payments, Ranking
FROM CTE
WHERE Ranking <= 3;
"""

cursor.execute(query_14)
data = cursor.fetchall()

df = pd.DataFrame(data, columns=["Customer", "Year", "Payments", "Ranking"])
print(df)

# Plotting
plt.figure(figsize=(10, 6))
for year in df["Year"].unique():
    subset = df[df["Year"] == year]
    plt.bar(
        subset["Ranking"] + (year - 2016) * 0.2,
        subset["Payments"],
        width=0.2,
        label=f"Year {year}"
    )

plt.xlabel("Ranking")
plt.ylabel("Payments")
plt.title("Top 3 Customers by Payments for Each Year")
plt.xticks(range(1, 4), ["1st", "2nd", "3rd"])
plt.legend(title="Year")
plt.show()

print("------------------------------------------------------------------------------------------------")
