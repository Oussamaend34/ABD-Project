package com.ensah;


import org.apache.spark.SparkConf;
import org.apache.spark.sql.*;
import org.apache.spark.sql.api.java.UDF2;
import org.apache.spark.sql.types.DataTypes;

import java.io.IOException;
import java.io.InputStream;
import java.sql.Timestamp;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.Properties;

import static org.apache.spark.sql.avro.functions.to_avro;
import static org.apache.spark.sql.functions.*;


public class Main {

    public static UDF2<Integer, Integer, byte[]> intToBinaryUDF = (value, byteSize) -> {
        if (value == null || byteSize == null) return null;

        // Check max allowed value
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
        String mongoUri = properties.getProperty("mongodb.uri");
        String mongoDatabase = properties.getProperty("mongodb.database");
        String rawCollection = properties.getProperty("mongodb.raw.collection");
        String dailyUsageSummaryCollection = properties.getProperty("mongodb.dail-usage.collection");
        String schemaRegistryUrl = properties.getProperty("schema.registry.url");
        String cdrUnratableTopic = properties.getProperty("cdr.unratable.topic");
        String cdrUnratableSubject = properties.getProperty("cdr.unratable.subject");
        String bootstrapServers = properties.getProperty("kafka.bootstrap.servers");
        String schema = "{\"type\":\"record\",\"name\":\"UnratableCDR\",\"namespace\":\"com.ensah.telecom.events\",\"fields\":[{\"name\":\"customer_id\",\"type\":\"long\"},{\"name\":\"customer_status\",\"type\":\"string\"},{\"name\":\"customer_subscription_type\",\"type\":\"string\"},{\"name\":\"msisdn\",\"type\":\"string\"},{\"name\":\"record_type\",\"type\":\"string\"},{\"name\":\"count\",\"type\":\"long\"},{\"name\":\"total_duration\",\"type\":[\"null\",\"long\"],\"default\":null},{\"name\":\"total_data_volume\",\"type\":[\"null\",\"double\"],\"default\":null},{\"name\":\"usage_date\",\"type\":{\"type\":\"int\",\"logicalType\":\"date\"}}]}";
        Integer schemaId = 6;


        SparkConf conf = new SparkConf()
                .setAppName("Telecom Data Aggregator")
//                .setMaster("local[*]")
                .set("spark.mongodb.read.connection.uri", mongoUri)
                .set("spark.mongodb.read.database", mongoDatabase)
                .set("spark.mongodb.read.collection", rawCollection);

        SparkSession spark = SparkSession.builder().config(conf).getOrCreate();

        spark.udf().register("int_to_binary_udf", intToBinaryUDF, DataTypes.BinaryType);

        Dataset<Row> customersDf = spark.read()
                .jdbc(url, customersTable, properties);

        Dataset<Row> raw_usage = spark.read()
                .format("mongodb")
                .option("spark.mongodb.read.connection.uri", mongoUri)
                .option("spark.mongodb.read.database", mongoDatabase)
                .option("spark.mongodb.read.collection", rawCollection)
                .load();
        raw_usage = raw_usage.drop(col("_id"));


        LocalDate today = LocalDate.now();
        LocalDateTime startOfDay = today.atStartOfDay();
        LocalDateTime endOfDay = startOfDay.plusDays(1).minusNanos(1);
        Timestamp from = Timestamp.from(startOfDay.toInstant(ZoneOffset.UTC));
        Timestamp to = Timestamp.from(endOfDay.toInstant(ZoneOffset.UTC));
        System.out.println("Total records in raw_usage: " + raw_usage.count());
        Dataset<Row> filteredDf = raw_usage.filter(raw_usage.col("timestamp").between(from, to)).withColumn("usage_date", functions.to_date(col("timestamp")));
        System.out.println("Filtered records count: " + filteredDf.count());
        Dataset<Row> aggregatedDf = filteredDf.groupBy(col("msisdn"), col("record_type"), col("usage_date"))
                .agg(
                        count("*").alias("count"),
                        functions.sum(col("duration_sec")).alias("total_duration"),
                        functions.sum(col("data_volume_mb")).alias("total_data_volume")
                );
        System.out.println("Aggregated records count: " + aggregatedDf.count());
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
        System.out.println("Enriched records count: " + enrichedDf.count());
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
        System.out.println("Ratable records count: " + ratableDf.count());
        Dataset<Row> nonRatableDf = enrichedDf.filter(
                enrichedDf.col("customer_status")
                        .notEqual("active")
                        .or(enrichedDf.col("customer_subscription_type").notEqual("postpaid"))
        );
        System.out.println("Non-ratable records count: " + nonRatableDf.count());
        ratableDf.write()
                .format("mongodb")
                .option("spark.mongodb.write.connection.uri", mongoUri)
                .option("spark.mongodb.write.database", mongoDatabase)
                .option("spark.mongodb.write.collection", dailyUsageSummaryCollection)
                .mode(SaveMode.Append)
                .save();

        nonRatableDf = nonRatableDf.select(
                col("customer_id"),
                col("customer_status"),
                col("customer_subscription_type"),
                col("msisdn"),
                col("record_type"),
                col("count"),
                col("total_duration"),
                col("total_data_volume"),
                col("usage_date")
        );

        nonRatableDf = nonRatableDf
                .select(
                        col("customer_id").cast("string").as("key"),
                        to_avro(struct("*"), schema).as("value")
                );

        Column magicByte = callUDF("int_to_binary_udf", lit(0), lit(1));
        Column schemaIdColumn = callUDF("int_to_binary_udf", lit(schemaId), lit(4));
        nonRatableDf = nonRatableDf.withColumn("value", concat(magicByte, schemaIdColumn, col("value")));
//        nonRatableDf = nonRatableDf.selectExpr("CAST(key AS STRING) AS key", "CAST(value AS BINARY) AS value");
        nonRatableDf.write()
                .format("kafka")
                .option("kafka.bootstrap.servers", bootstrapServers)
                .option("topic", cdrUnratableTopic)
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