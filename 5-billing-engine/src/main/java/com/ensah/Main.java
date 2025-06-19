package com.ensah;


import org.apache.spark.SparkConf;
import org.apache.spark.sql.Column;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.api.java.UDF2;
import org.apache.spark.sql.types.DataTypes;
import scala.collection.JavaConverters;
import scala.collection.Seq;

import java.io.IOException;
import java.io.InputStream;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.List;
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

    public static void main(String[] args) throws IOException {
        Properties properties = getProperties();
        String mongoUri = properties.getProperty("mongodb.uri");
        String mongoDatabase = properties.getProperty("mongodb.database");
        String bootstrapServers = properties.getProperty("kafka.bootstrap.servers");
        String invoiceTopic = properties.getProperty("telecom.billing.invoice.topic");
        String monthlyUsageSummaryCollection = properties.getProperty("mongodb.monthly-usage.collection");
        String schema = "{\"type\":\"record\",\"name\":\"MonthlyInvoice\",\"namespace\":\"com.ensah.telecom.events\",\"fields\":[{\"name\":\"customer_id\",\"type\":\"long\"},{\"name\":\"billing_month\",\"type\":\"string\"},{\"name\":\"first_name\",\"type\":\"string\"},{\"name\":\"last_name\",\"type\":\"string\"},{\"name\":\"email\",\"type\":\"string\"},{\"name\":\"msisdn\",\"type\":\"string\"},{\"name\":\"subscription_type\",\"type\":\"string\"},{\"name\":\"status\",\"type\":\"string\"},{\"name\":\"activation_date\",\"type\":{\"type\":\"long\",\"logicalType\":\"timestamp-millis\"}},{\"name\":\"voice_cost\",\"type\":\"double\"},{\"name\":\"sms_cost\",\"type\":\"double\"},{\"name\":\"data_cost\",\"type\":\"double\"},{\"name\":\"total_base_cost\",\"type\":\"double\"},{\"name\":\"full_name\",\"type\":\"string\"}]}";
        Integer schemaId =  7;

        SparkConf conf = new SparkConf()
                .setAppName("Billing Engine")
                .setMaster("local[*]")
                .set("spark.mongodb.read.connection.uri", mongoUri)
                .set("spark.mongodb.read.database", mongoDatabase)
                .set("spark.mongodb.read.collection", monthlyUsageSummaryCollection);

        SparkSession spark = SparkSession.builder().config(conf).getOrCreate();

        spark.udf().register("int_to_binary_udf", intToBinaryUDF, DataTypes.BinaryType);

        Dataset<Row> monthlyUsage = spark.read()
                .format("mongodb")
                .option("spark.mongodb.read.connection.uri", mongoUri)
                .option("spark.mongodb.read.database", mongoDatabase)
                .option("spark.mongodb.read.collection", monthlyUsageSummaryCollection)
                .load();
        monthlyUsage = monthlyUsage.drop("_id");

        LocalDate today = LocalDate.now();
        LocalDate previousMonthDate = today.minusMonths(0); // TODO: Change this to make it work with the last month
        String targetBillingMonth = previousMonthDate.format(DateTimeFormatter.ofPattern("yyyy-MM"));

        monthlyUsage = monthlyUsage.filter(col("billing_month").equalTo(targetBillingMonth));

        Dataset<Row> pivoted = monthlyUsage.groupBy("customer_id", "billing_month")
                .pivot("record_type", Arrays.asList("voice", "sms", "data"))
                .agg(sum("base_cost").alias("cost"));

        pivoted.printSchema();
        pivoted.show();

        Dataset<Row> customerInfo = monthlyUsage.groupBy("customer_id", "billing_month").agg(
                first("first_name").alias("first_name"),
                first("last_name").alias("last_name"),
                first("email").alias("email"),
                first("msisdn").alias("msisdn"),
                first("subscription_type").alias("subscription_type"),
                first("status").alias("status"),
                first("activation_date").alias("activation_date")
        );
        customerInfo.printSchema();
        customerInfo.show();
        List<String> joinCols = Arrays.asList("customer_id", "billing_month");
        Seq<String> joinColumns = JavaConverters.asScalaIteratorConverter(joinCols.iterator()).asScala().toSeq();
        Dataset<Row> invoice = customerInfo.join(pivoted, joinColumns);

        invoice = invoice.na().fill(0.0, new String[]{"voice", "sms", "data"});

        invoice = invoice.withColumn("total_base_cost",
                col("voice").plus(col("sms")).plus(col("data")));

        invoice = invoice.withColumnRenamed("voice", "voice_cost")
                .withColumnRenamed("sms", "sms_cost")
                .withColumnRenamed("data", "data_cost")
                .withColumn("full_name", concat_ws(" ", col("first_name"), col("last_name")));

        invoice.printSchema();
        invoice.show();


        invoice = invoice.select(
                col("customer_id").cast("string").as("key"),
                to_avro(struct("*"), schema).as("value")
        );

        Column magicByte = callUDF("int_to_binary_udf", lit(0), lit(1));
        Column schemaIdColumn = callUDF("int_to_binary_udf", lit(schemaId), lit(4));
        invoice = invoice.withColumn("value", concat(magicByte, schemaIdColumn, col("value")));

        invoice.write()
                .format("kafka")
                .option("kafka.bootstrap.servers", bootstrapServers)
                .option("topic", invoiceTopic)
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