import psycopg
import csv

# Database connection config
conn = psycopg.connect(
    host="localhost",
    dbname="mydb",
    user="postgres",
    password="password",
    port=6400
)

output_file = 'utils/customer_data.csv'

with conn.cursor() as cur:
    # Fetch required customer data
    cur.execute("""
        SELECT c.msisdn, ci.name AS city_name, r.name AS region_name
        FROM customers c
        JOIN cities ci ON c.city_id = ci.id
        JOIN regions r ON c.region_id = r.id
    """)

    rows = cur.fetchall()

    # Write to CSV
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['msisdn', 'home_city_name', 'home_region_name'])  # header
        writer.writerows(rows)

conn.close()
print(f"✅ Exported {len(rows)} customers to {output_file}")
