package com.ensah;


import org.apache.spark.SparkContext;
import org.apache.spark.sql.*;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.Metadata;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.count;


public class Main {
    public static void main(String[] args) throws IOException {
        SparkSession spark = SparkSession.builder()
                .appName("Telecom Data Aggregator")
                .master("local[*]")
                .getOrCreate();
        Properties properties = getProperties();
        StructType schema = new StructType(new StructField[]{
                new StructField("uuid", DataTypes.StringType, false, Metadata.empty()),
                new StructField("record_type", DataTypes.StringType, false, Metadata.empty()),
                new StructField("timestamp", DataTypes.TimestampType, false, Metadata.empty()),
                new StructField("msisdn", DataTypes.StringType, false, Metadata.empty()),
                new StructField("counter_party_msisdn", DataTypes.StringType, true, Metadata.empty()),
                new StructField("duration_sec", DataTypes.IntegerType, true, Metadata.empty()),
                new StructField("data_volume_mb", DataTypes.DoubleType, true, Metadata.empty()),
                new StructField("cell_id", DataTypes.StringType, true, Metadata.empty()),
                new StructField("technology", DataTypes.StringType, true, Metadata.empty()),
                new StructField("status", DataTypes.StringType, false, Metadata.empty()),
        });

        String url = properties.getProperty("url");
        String table = properties.getProperty("dbtable");

        Dataset<Row> df = spark.read()
                .jdbc(url, table, properties);
        df = spark.createDataFrame(df.rdd(), schema);
        Dataset<Row> aggregatedDf = df.groupBy(col("msisdn"), col("record_type"))
                .agg(
                        count("*").alias("count"),
                        functions.sum(col("duration_sec")).alias("total_duration"),
                        functions.sum(col("data_volume_mb")).alias("total_data_volume")
                ).orderBy(col("count").desc(), col("total_duration").desc(), col("total_data_volume").desc());
        aggregatedDf.show();
    }

    private static Properties getProperties() throws IOException {
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

