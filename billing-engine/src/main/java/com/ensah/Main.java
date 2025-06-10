package com.ensah;


import org.apache.spark.SparkConf;
import org.apache.spark.sql.*;
import org.apache.spark.sql.api.java.UDF2;
import org.apache.spark.sql.types.DataTypes;

import java.io.IOException;
import java.io.InputStream;
import java.time.LocalDate;
import java.sql.Date;
import java.time.format.DateTimeFormatter;
import java.util.Properties;

import static org.apache.spark.sql.functions.*;


public class Main {

    public static UDF2<Integer, Integer, byte[]> intToBinaryUDF = (value, byteSize) -> {
        if (value == null || byteSize == null) return null;

        int max = (int) Math.pow(2, byteSize * 8) - 1;
        if (value > max) throw new IllegalArgumentException("Value doesn't fit in the byte size");

        byte[] result = new byte[byteSize];
        for (int i = byteSize - 1; i >= 0; i--) {
            result[i] = (byte) (value & 0xFF);
            value >>= 8;
        }
        return result;
    };

    public static void main(String[] args) throws Exception {
        Properties properties = getProperties();
        String url = properties.getProperty("url");
        String customersTable = properties.getProperty("customers.table");
        String productRatesTable = properties.getProperty("product.rates.table");
        String productsTable = properties.getProperty("products.table");
        String rateTiersTable = properties.getProperty("rate.tiers.table");
        String host = properties.getProperty("cassandra.connection.host");
        String port = properties.getProperty("cassandra.connection.port");
        String keyspace = properties.getProperty("cassandra.keyspace");
        String dailyUsageTable = properties.getProperty("cassandra.daily.usage.table");
        String monthlyBillingResultTable = properties.getProperty("cassandra.monthly.billing.result.table");


        SparkConf conf = new SparkConf()
                .setAppName("Telecom Data Aggregator")
                .set("spark.cassandra.connection.host", host)
                .set("spark.cassandra.connection.port", port);

        SparkSession spark = SparkSession.builder().config(conf).getOrCreate();

        spark.udf().register("int_to_binary_udf", intToBinaryUDF, DataTypes.BinaryType);

        Dataset<Row> customersDf = spark.read()
                .jdbc(url, customersTable, properties);
        Dataset<Row> productRatesDf = spark.read()
                .jdbc(url, productRatesTable, properties);
        Dataset<Row> productsDf = spark.read()
                .jdbc(url, productsTable, properties);
        Dataset<Row> rateTiersDf = spark.read()
                .jdbc(url, rateTiersTable, properties);

        Dataset<Row> daily_usage_summary = spark.read()
                .format("org.apache.spark.sql.cassandra")
                .option("keyspace", keyspace)
                .option("table", dailyUsageTable)
                .load();

        Date firstDayOfMonth = Date.valueOf(LocalDate.now().withDayOfMonth(1));
        Date lastDayOfMonth = Date.valueOf(LocalDate.now().plusMonths(1).withDayOfMonth(1));
        String billingMonth = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyy-MM"));
        System.out.println("firstDayOfMonth = " + firstDayOfMonth);
        System.out.println("lastDayOfMonth = " + lastDayOfMonth);
        Dataset<Row> daily_usage_summary_month = daily_usage_summary.filter(daily_usage_summary.col("usage_date").between(firstDayOfMonth, lastDayOfMonth));


        Dataset<Row> monthlyUsage = daily_usage_summary_month.groupBy(col("customer_id"), col("record_type"))
                .agg(
                        functions.sum(col("count")).alias("count"),
                        functions.sum(col("total_duration")).alias("total_duration"),
                        functions.sum(col("total_data_volume")).alias("total_data_volume")
                );
        Dataset<Row> usageWithCustomer = monthlyUsage
                .join(customersDf, monthlyUsage.col("customer_id").equalTo(customersDf.col("id")))
                .filter(col("status").equalTo("active").and(col("subscription_type").equalTo("postpaid")));

        productsDf = productsDf.select(col("id").alias("product_id"), col("service"));
        productRatesDf = productRatesDf.withColumnRenamed("id", "product_rate_id");
        Dataset<Row> ratesWithServices = productRatesDf.join(productsDf, productRatesDf.col("product_id").equalTo(productsDf.col("product_id")));
        Dataset<Row> enriched = usageWithCustomer.join(ratesWithServices, usageWithCustomer.col("rate_plan_id").equalTo(ratesWithServices.col("rate_plan_id"))
                .and(usageWithCustomer.col("record_type").equalTo(ratesWithServices.col("service"))));

        Dataset<Row> withCost = enriched.withColumn(
                "base_cost",
                when(col("rate_type").equalTo("flat_rate"), col("count").multiply(col("unit_price")))
                        .when(col("rate_type").equalTo("per_unit").and(col("record_type").equalTo("voice")), col("total_duration").multiply(col("unit_price")))
                        .when(col("rate_type").equalTo("per_unit").and(col("record_type").equalTo("data")), col("total_data_volume").multiply(col("unit_price")))
                        .otherwise(lit(null)));
        withCost = withCost.filter(col("rate_type").notEqual("tiered"));
        Dataset<Row> tieredOnly = enriched.filter(col("rate_type").equalTo("tiered"));
        tieredOnly = tieredOnly.join(rateTiersDf, tieredOnly.col("product_rate_id").equalTo(rateTiersDf.col("product_rate_id")));
        tieredOnly = tieredOnly.withColumn(
                "tier_cost",
                when(
                        col("record_type").equalTo("voice").and(col("max_units").isNull()).and(col("total_duration").gt(col("min_units"))),
                        col("total_duration").minus(col("min_units")).multiply(col("tier_unit_price"))
                ).otherwise(lit(0)));
        tieredOnly = tieredOnly.withColumn(
                "tier_cost",
                when(
                        col("record_type").equalTo("voice").and(col("total_duration").between(col("min_units"), col("max_units"))),
                        col("total_duration").minus(col("min_units")).multiply(col("tier_unit_price"))
                ).otherwise(col("tier_cost")));
        tieredOnly = tieredOnly.withColumn(
                "tier_cost",
                when(
                        col("record_type").equalTo("voice").and(col("total_duration").gt(col("max_units"))),
                        col("max_units").minus(col("min_units")).multiply(col("tier_unit_price"))
                ).otherwise(col("tier_cost")));
        tieredOnly = tieredOnly.withColumn(
                "tier_cost",
                when(
                        col("record_type").equalTo("voice").and(col("total_duration").lt(col("min_units"))),
                        0
                ).otherwise(col("tier_cost")));
        tieredOnly = tieredOnly.withColumn(
                "tier_cost",
                when(
                        col("record_type").equalTo("data").and(col("max_units").isNull()).and(col("total_data_volume").gt(col("min_units"))),
                        col("total_data_volume").minus(col("min_units")).multiply(col("tier_unit_price"))
                        ).otherwise(col("tier_cost")));
        tieredOnly = tieredOnly.withColumn(
                "tier_cost",
                when(
                        col("record_type").equalTo("data").and(col("total_data_volume").between(col("min_units"), col("max_units"))),
                        col("total_data_volume").minus(col("min_units")).multiply(col("tier_unit_price"))
                ).otherwise(lit(col("tier_cost"))));
        tieredOnly = tieredOnly.withColumn(
                "tier_cost",
                when(
                        col("record_type").equalTo("data").and(col("total_data_volume").gt(col("max_units"))),
                        col("max_units").minus(col("min_units")).multiply(col("tier_unit_price"))
                ).otherwise(col("tier_cost")));
        tieredOnly = tieredOnly.withColumn(
                "tier_cost",
                when(
                        col("record_type").equalTo("data").and(col("total_data_volume").lt(col("min_units"))),
                        0
                ).otherwise(col("tier_cost")));

        Dataset<Row> tieredOnlyWithCost = tieredOnly.groupBy(col("customer_id"), col("record_type")).agg(
                functions.sum(col("tier_cost")).alias("base_cost")
        ).as("tiered_only_with_cost").join(enriched.as("enriched"), col("tiered_only_with_cost.customer_id").equalTo(col("enriched.customer_id"))
                .and(col("tiered_only_with_cost.record_type").equalTo(col("enriched.record_type"))));

        withCost = withCost.select(
                col("customer_id"),
                col("record_type"),
                col("count"),
                col("total_duration"),
                col("total_data_volume"),
                col("msisdn"),
                col("first_name"),
                col("last_name"),
                col("email"),
                col("activation_date"),
                col("status"),
                col("subscription_type"),
                col("base_cost")
        );

        tieredOnlyWithCost = tieredOnlyWithCost.select(
                col("enriched.customer_id").as("customer_id"),
                col("enriched.record_type").as("record_type"),
                col("count"),
                col("total_duration"),
                col("total_data_volume"),
                col("msisdn"),
                col("first_name"),
                col("last_name"),
                col("email"),
                col("activation_date"),
                col("status"),
                col("subscription_type"),
                col("base_cost")
        );
        Dataset<Row> finalDf = withCost.unionByName(tieredOnlyWithCost).withColumn("billing_month", lit(billingMonth));
        finalDf.write()
                .format("org.apache.spark.sql.cassandra")
                .option("keyspace", keyspace)
                .option("table", monthlyBillingResultTable)
                .mode(SaveMode.Append)
                .save();
    }


    public static Properties getProperties() throws IOException {
        final Properties props = new Properties();
        try(InputStream fis = Main.class.getClassLoader().getResourceAsStream("application.properties")) {
            if (fis != null) {
                props.load(fis);
            } else {
                throw new IOException("Properties file not found");
            }
        }
        return props;
    }
}