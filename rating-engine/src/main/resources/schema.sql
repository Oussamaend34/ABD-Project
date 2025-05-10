CREATE TABLE customers(
    id BIGSERIAL PRIMARY KEY,
    msisdn VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    rate_plan_id BIGSERIAL NOT NULL,
    activation_date DATE NOT NULL,
    status VARCHAR(255) NOT NULL CHECK( status in  ('active', 'suspended', 'terminated')),
    region VARCHAR(255) NOT NULL
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
    rate_plan_id BIGSERIAL NOT NULL,
    product_id BIGSERIAL NOT NULL,
    rate_type VARCHAR(255) NOT NULL CHECK ( rate_type in ('per_unit', 'tiered', 'flat_rate')),
    unit_price DECIMAL
);

CREATE TABLE rate_tiers(
    id BIGSERIAL PRIMARY KEY,
    product_rate_id BIGSERIAL NOT NULL,
    tier INT NOT NULL,
    min_units BIGINT NOT NULL,
    max_units BIGINT NOT NULL
);

ALTER TABLE customers ADD CONSTRAINT customers_email_unique UNIQUE (email);

ALTER TABLE customers ADD CONSTRAINT customers_msisdn_unique UNIQUE (msisdn);

ALTER TABLE products ADD CONSTRAINT products_name_unique UNIQUE (name);

ALTER TABLE rate_plans ADD CONSTRAINT rate_plans_name_unique UNIQUE (name);

ALTER TABLE product_rates ADD CONSTRAINT product_rates_rate_plan_id_product_id_unique UNIQUE (rate_plan_id,product_id);

ALTER TABLE customers ADD CONSTRAINT customers_rate_plan_id_fk FOREIGN KEY (rate_plan_id) REFERENCES rate_plans (id);

ALTER TABLE product_rates ADD CONSTRAINT product_rate_rate_plan_id_fk FOREIGN KEY (rate_plan_id) REFERENCES rate_plans (id);

ALTER TABLE product_rates ADD CONSTRAINT product_rate_product_id_fk FOREIGN KEY (product_id) REFERENCES products (id);

ALTER TABLE rate_tiers ADD CONSTRAINT rate_tiers_product_rate_id_fk FOREIGN KEY (product_rate_id) REFERENCES product_rates (id);

ALTER TABLE customers ADD COLUMN subscription_type VARCHAR(255) NOT NULL DEFAULT 'postpaid' CHECK ( subscription_type in ('postpaid', 'prepaid'));

