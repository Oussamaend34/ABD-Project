package com.ensah;


import org.apache.spark.SparkConf;
import org.apache.spark.sql.*;

import java.io.IOException;
import java.io.InputStream;
import java.sql.Timestamp;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.Properties;

import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.count;


public class Main {
    public static void main(String[] args) throws IOException {

        Properties properties = getProperties();

        String url = properties.getProperty("url");
        String customersTable = properties.getProperty("customers.table");
        String host = properties.getProperty("cassandra.connection.host");
        String port = properties.getProperty("cassandra.connection.port");
        String keyspace = properties.getProperty("cassandra.keyspace");
        String rawUsagesTable = properties.getProperty("cassandra.raw.data.table");
        String dailyUsageTable = properties.getProperty("cassandra.daily.usage.table");

        SparkConf conf = new SparkConf()
                .setAppName("Telecom Data Aggregator")
                .setMaster("local[*]")
                .set("spark.cassandra.connection.host", host)
                .set("spark.cassandra.connection.port", port);

        SparkSession spark = SparkSession.builder().config(conf).getOrCreate();

        Dataset<Row> customersDf = spark.read()
                .jdbc(url, customersTable, properties);

        Dataset<Row> raw_usage = spark.read()
                .format("org.apache.spark.sql.cassandra")
                .option("keyspace", keyspace)
                .option("table", rawUsagesTable)
                .load();

        LocalDate today = LocalDate.now().minusDays(1);
        LocalDateTime startOfDay = today.atStartOfDay();
        LocalDateTime endOfDay = startOfDay.plusDays(1).minusNanos(1);
        Timestamp from = Timestamp.from(startOfDay.toInstant(ZoneOffset.UTC));
        Timestamp to = Timestamp.from(endOfDay.toInstant(ZoneOffset.UTC));

        Dataset<Row> filteredDf = raw_usage.filter(raw_usage.col("timestamp").between(from, to)).withColumn("usage_date", functions.to_date(col("timestamp")));
        Dataset<Row> aggregatedDf = filteredDf.groupBy(col("msisdn"), col("record_type"), col("usage_date"))
                .agg(
                        count("*").alias("count"),
                        functions.sum(col("duration_sec")).alias("total_duration"),
                        functions.sum(col("data_volume_mb")).alias("total_data_volume")
                );

        Dataset<Row> enrichedDf = aggregatedDf.as("aggregated").join(customersDf.as("customers"), col("aggregated.msisdn").equalTo(col("customers.msisdn")))
                        .select(
                                col("customers.id").as("customer_id"),
                                col("customers.status").as("customer_status"),
                                col("customers.subscription_type").as("customer_subscription_type"),
                                col("aggregated.msisdn"),
                                col("aggregated.record_type"),
                                col("aggregated.count"),
                                col("aggregated.total_duration").as("total_duration"),
                                col("aggregated.total_data_volume").as("total_data_volume"),
                                col("aggregated.usage_date")
                        );

        Dataset<Row> ratableDf = enrichedDf.filter(enrichedDf.col("customer_status")
                .equalTo("active")
                .and(enrichedDf.col("customer_subscription_type").equalTo("postpaid")))
                .select(
                        col("customer_id"),
                        col("msisdn"),
                        col("record_type"),
                        col("count"),
                        col("total_duration"),
                        col("total_data_volume"),
                        col("usage_date")
                );
        Dataset<Row> nonRatableDf = enrichedDf.filter(
                enrichedDf.col("customer_status")
                        .notEqual("active")
                        .or(enrichedDf.col("customer_subscription_type").notEqual("postpaid"))
        );
        System.out.println("Ratable Records Count: " + ratableDf.count());
        System.out.println("Non-Ratable Records Count: " + nonRatableDf.count());
        ratableDf.printSchema();

        ratableDf.write()
                .format("org.apache.spark.sql.cassandra")
                .option("keyspace", keyspace)
                .option("table", dailyUsageTable)
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