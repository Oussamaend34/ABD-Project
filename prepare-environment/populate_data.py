import psycopg
from faker import Faker
import random
import json
import csv


def load_customers_from_csv(path):
    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def _generate_msisdn() -> str:
    prefix = random.choice(["2126", "2127"])
    number = random.randint(10000000, 99999999)
    return f"{prefix}{number}"


def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)


def populate_database_from_csv_and_json(
    db_config=None,
    regions_json_path="regions.json",
    cities_json_path="cities.json",
    customers_csv_path="customer_data.csv",
):
    if db_config is None:
        db_config = {
            "host": "localhost",
            "dbname": "mydb",
            "user": "postgres",
            "password": "password",
            "port": 6400,
        }

    conn = psycopg.connect(**db_config)
    faker = Faker()

    regions_data = load_json(regions_json_path)
    cities_data = load_json(cities_json_path)

    with conn.transaction():
        with conn.cursor() as cur:
            # Insert Regions
            region_id_map = {}
            for key, value in regions_data.items():
                cur.execute(
                    "INSERT INTO regions (name) VALUES (%s) RETURNING id",
                    (value["name"],),
                )
                region_id_map[key] = cur.fetchone()[0]

            # Insert Cities
            city_id_map = {}
            for key, value in cities_data.items():
                region_db_id = region_id_map[value["region_id"]]
                cur.execute(
                    "INSERT INTO cities (name, pretty_name, region_id) VALUES (%s, %s, %s) RETURNING id",
                    (value["name"], value["pretty_name"], region_db_id),
                )
                city_id_map[key] = {
                    "id": cur.fetchone()[0],
                    "max_cell_id": int(value["max_cell_id"]),
                    "pretty_name": value["pretty_name"],
                }

            # Insert Cells
            for city_key, city_info in city_id_map.items():
                for i in range(1, city_info["max_cell_id"] + 1):
                    cell_name = f"{city_info['pretty_name']}_{i}"
                    lat = round(faker.latitude(), 6)
                    lon = round(faker.longitude(), 6)
                    cur.execute(
                        "INSERT INTO cells (name, city_id, latitude, longitude) VALUES (%s, %s, %s, %s)",
                        (cell_name, city_info["id"], lat, lon),
                    )

            # Insert Rate Plans
            rate_plan_names = ["Basic", "Standard", "Premium", "Enterprise"]
            rate_plan_ids = []
            for name in rate_plan_names:
                description = f"{name} plan suitable for different usage profiles."
                cur.execute(
                    "INSERT INTO rate_plans (name, description) VALUES (%s, %s) RETURNING id",
                    (name, description),
                )
                rate_plan_ids.append(cur.fetchone()[0])

            # Define Products (voice, sms, data)
            products = [
                ("Voice Call", "Voice call service", "voice"),
                ("SMS", "Text messaging service", "sms"),
                ("Data Usage", "Mobile data service", "data"),
            ]
            product_ids = {}
            for name, description, service in products:
                cur.execute(
                    "INSERT INTO products (name, description, service) VALUES (%s, %s, %s) RETURNING id",
                    (name, description, service),
                )
                product_ids[service] = cur.fetchone()[0]

            # Insert Product Rates
            for rate_plan_id in rate_plan_ids:
                for service, product_id in product_ids.items():
                    if service == "sms":
                        rate_type = "flat_rate"
                        unit_price = round(random.uniform(0.01, 0.05), 2)
                        cur.execute(
                            """INSERT INTO product_rates (rate_plan_id, product_id, rate_type, unit_price)
                               VALUES (%s, %s, %s, %s) RETURNING id""",
                            (rate_plan_id, product_id, rate_type, unit_price),
                        )
                    else:
                        rate_type = random.choice(["per_unit", "tiered"])
                        unit_price = round(random.uniform(0.05, 0.5), 2) if rate_type == "per_unit" else None
                        cur.execute(
                            """INSERT INTO product_rates (rate_plan_id, product_id, rate_type, unit_price)
                               VALUES (%s, %s, %s, %s) RETURNING id""",
                            (rate_plan_id, product_id, rate_type, unit_price),
                        )
                        product_rate_id = cur.fetchone()[0]

                        if rate_type == "tiered":
                            num_tiers = random.randint(2, 4)
                            for tier in range(1, num_tiers + 1):
                                min_units = (tier - 1) * 100
                                max_units = tier * 100 if tier != num_tiers else None
                                tier_price = round(random.uniform(0.02, 0.4), 2)
                                cur.execute(
                                    """INSERT INTO rate_tiers (product_rate_id, tier, tier_unit_price, min_units, max_units)
                                       VALUES (%s, %s, %s, %s, %s)""",
                                    (product_rate_id, tier, tier_price, min_units, max_units),
                                )

            # Insert Customers
            customers_data = load_customers_from_csv(customers_csv_path)
            cur.execute("SELECT id, name FROM regions")
            region_map = {name.lower(): id for id, name in cur.fetchall()}
            cur.execute("SELECT id, name, region_id FROM cities")
            city_map = {
                (name.lower(), region_id): id for id, name, region_id in cur.fetchall()
            }

            subscription_type_weights = {"prepaid": 0.1, "postpaid": 0.9}
            status_weights = {"active": 0.8, "suspended": 0.15, "terminated": 0.05}
            inserted_count = 0

            for customer in customers_data:
                msisdn = customer["msisdn"]
                city_name = customer["home_city_name"].strip().lower()
                region_name = customer["home_region_name"].strip().lower()

                region_id = region_map.get(region_name)
                if not region_id:
                    print(f"Region not found: {region_name}")
                    continue

                city_id = city_map.get((city_name, region_id))
                if not city_id:
                    print(f"City not found for {city_name} in region {region_name}")
                    continue

                first_name = faker.first_name()
                last_name = faker.last_name()
                email = faker.unique.email()
                rate_plan_id = random.choice(rate_plan_ids)
                activation_date = faker.date_between(start_date="-2y", end_date="today")
                subscription_type = random.choices(
                    population=list(subscription_type_weights.keys()),
                    weights=list(subscription_type_weights.values()),
                    k=1,
                )[0]
                status = random.choices(
                    population=list(status_weights.keys()),
                    weights=list(status_weights.values()),
                    k=1,
                )[0]

                cur.execute(
                    """INSERT INTO customers (msisdn, first_name, last_name, email, rate_plan_id,
                        activation_date, subscription_type, status, region_id, city_id)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (
                        msisdn,
                        first_name,
                        last_name,
                        email,
                        rate_plan_id,
                        activation_date,
                        subscription_type,
                        status,
                        region_id,
                        city_id,
                    ),
                )
                inserted_count += 1

            print(f"✅ Inserted {inserted_count} customers from CSV.")

    conn.close()
    print("✅ Database populated successfully.")


# Run directly
if __name__ == "__main__":
    populate_database_from_csv_and_json()
