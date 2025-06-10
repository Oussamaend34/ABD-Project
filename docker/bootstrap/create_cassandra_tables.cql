CREATE TABLE IF NOT EXISTS telecom.raw_usage_records (
    uuid text,
    record_type text,
    timestamp timestamp,
    msisdn text,
    counterparty_msisdn text,
    duration_sec int,
    data_volume_mb double,
    cell_id text,
    technology text,
    status text,
    PRIMARY KEY ((msisdn), timestamp, uuid)
) WITH CLUSTERING ORDER BY (timestamp DESC);

CREATE TABLE IF NOT EXISTS telecom.daily_usage_summary (
    customer_id bigint,
    msisdn text,
    record_type text,
    count bigint,
    total_duration bigint,
    total_data_volume double,
    usage_date date,
    PRIMARY KEY ((customer_id), usage_date, record_type)
) WITH CLUSTERING ORDER BY (usage_date DESC, record_type ASC);

CREATE TABLE IF NOT EXISTS telecom.monthly_billing_result (
    customer_id BIGINT,
    billing_month DATE,
    msisdn TEXT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    activation_date DATE,
    status TEXT,
    record_type TEXT,
    count BIGINT,
    total_duration BIGINT,
    total_data_volume DOUBLE,
    base_cost DOUBLE,
    PRIMARY KEY ((customer_id, billing_month), record_type)
);
