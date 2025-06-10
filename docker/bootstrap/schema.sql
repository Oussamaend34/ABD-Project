CREATE TABLE customers (
    id BIGSERIAL PRIMARY KEY,
    msisdn VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    rate_plan_id BIGINT NOT NULL,
    activation_date DATE NOT NULL,
    subscription_type VARCHAR(255) NOT NULL DEFAULT 'postpaid' CHECK (subscription_type in ('postpaid', 'prepaid')),
    status VARCHAR(255) NOT NULL CHECK (status in ('active', 'suspended', 'terminated')),
    region_id BIGINT NOT NULL,
    city_id BIGINT NOT NULL
);

CREATE TABLE regions (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE cities (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    pretty_name VARCHAR(255),
    region_id BIGINT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(id)
);

CREATE TABLE cells (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255),
    city_id BIGINT NOT NULL,
    latitude DECIMAL NOT NULL,
    longitude DECIMAL NOT NULL,
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

CREATE TABLE products(
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    service VARCHAR NOT NULL CHECK ( service IN ('voice', 'sms', 'data'))
);

CREATE TABLE rate_plans(
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL
);

CREATE TABLE product_rates(
    id BIGSERIAL PRIMARY KEY,
    rate_plan_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    rate_type VARCHAR(255) NOT NULL CHECK ( rate_type in ('per_unit', 'tiered', 'flat_rate')),
    unit_price DECIMAL
);

CREATE TABLE rate_tiers(
    id BIGSERIAL PRIMARY KEY,
    product_rate_id BIGINT NOT NULL,
    tier INT NOT NULL,
    tier_unit_price DECIMAL NOT NULL,
    min_units BIGINT NOT NULL,
    max_units BIGINT
);



ALTER TABLE customers ADD CONSTRAINT customers_email_unique UNIQUE (email);

ALTER TABLE customers ADD CONSTRAINT customers_msisdn_unique UNIQUE (msisdn);

ALTER TABLE products ADD CONSTRAINT products_name_unique UNIQUE (name);

ALTER TABLE rate_plans ADD CONSTRAINT rate_plans_name_unique UNIQUE (name);

ALTER TABLE customers ADD CONSTRAINT customers_region_id_fk FOREIGN KEY (region_id) REFERENCES regions (id);

ALTER TABLE customers ADD CONSTRAINT customers_city_id_fk FOREIGN KEY (city_id) REFERENCES cities (id);

ALTER TABLE cells ADD CONSTRAINT cells_city_id_fk FOREIGN KEY (city_id) REFERENCES cities (id);

ALTER TABLE product_rates ADD CONSTRAINT product_rates_rate_plan_id_product_id_unique UNIQUE (rate_plan_id,product_id);

ALTER TABLE customers ADD CONSTRAINT customers_rate_plan_id_fk FOREIGN KEY (rate_plan_id) REFERENCES rate_plans (id);

ALTER TABLE product_rates ADD CONSTRAINT product_rate_rate_plan_id_fk FOREIGN KEY (rate_plan_id) REFERENCES rate_plans (id);

ALTER TABLE product_rates ADD CONSTRAINT product_rate_product_id_fk FOREIGN KEY (product_id) REFERENCES products (id);

ALTER TABLE rate_tiers ADD CONSTRAINT rate_tiers_product_rate_id_fk FOREIGN KEY (product_rate_id) REFERENCES product_rates (id);

