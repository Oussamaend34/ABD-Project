
spark-submit \
    --class com.ensah.Main \
    --master spark://spark-master:7077 \
    --deploy-mode cluster \
    --jars /home/spark/jars/spark-sql-kafka-0-10_2.12-3.1.3.jar,/home/spark/jars/spark-token-provider-kafka-0-10_2.12-3.1.3.jar,/home/spark/jars/kafka-clients-2.6.0.jar,/home/spark/jars/zstd-jni-1.4.8-1.jar,/home/spark/jars/lz4-java-1.7.1.jar,/home/spark/jars/snappy-java-1.1.8.2.jar,/home/spark/jars/slf4j-api-1.7.30.jar,/home/spark/jars/unused-1.0.0.jar,/home/spark/jars/commons-pool2-2.6.2.jar,/home/spark/jars/mongo-spark-connector_2.12-10.5.0.jar,/home/spark/jars/mongodb-driver-sync-5.1.4.jar,/home/spark/jars/bson-5.1.4.jar,/home/spark/jars/mongodb-driver-core-5.1.4.jar,/home/spark/jars/bson-record-codec-5.1.4.jar,/home/spark/jars/spark-avro_2.12-3.1.3.jar,/home/spark/jars/postgresql-42.7.5.jar,/home/spark/jars/checker-qual-3.48.3.jar \
    /home/spark/jars/daily-rating-engine.jar


spark-submit \
    --class com.ensah.Main \
    --master spark://spark-master:7077 \
    --deploy-mode cluster \
    --jars /home/spark/jars/spark-sql-kafka-0-10_2.12-3.1.3.jar,/home/spark/jars/spark-token-provider-kafka-0-10_2.12-3.1.3.jar,/home/spark/jars/kafka-clients-2.6.0.jar,/home/spark/jars/zstd-jni-1.4.8-1.jar,/home/spark/jars/lz4-java-1.7.1.jar,/home/spark/jars/snappy-java-1.1.8.2.jar,/home/spark/jars/slf4j-api-1.7.30.jar,/home/spark/jars/unused-1.0.0.jar,/home/spark/jars/commons-pool2-2.6.2.jar,/home/spark/jars/mongo-spark-connector_2.12-10.5.0.jar,/home/spark/jars/mongodb-driver-sync-5.1.4.jar,/home/spark/jars/bson-5.1.4.jar,/home/spark/jars/mongodb-driver-core-5.1.4.jar,/home/spark/jars/bson-record-codec-5.1.4.jar,/home/spark/jars/spark-avro_2.12-3.1.3.jar,/home/spark/jars/postgresql-42.7.5.jar,/home/spark/jars/checker-qual-3.48.3.jar \
    /home/spark/jars/monthly-rating-engine.jar

spark-submit \
    --class com.ensah.Main \
    --master spark://spark-master:7077 \
    --deploy-mode cluster \
    --jars /home/spark/jars/spark-sql-kafka-0-10_2.12-3.1.3.jar,/home/spark/jars/spark-token-provider-kafka-0-10_2.12-3.1.3.jar,/home/spark/jars/kafka-clients-2.6.0.jar,/home/spark/jars/zstd-jni-1.4.8-1.jar,/home/spark/jars/lz4-java-1.7.1.jar,/home/spark/jars/snappy-java-1.1.8.2.jar,/home/spark/jars/slf4j-api-1.7.30.jar,/home/spark/jars/unused-1.0.0.jar,/home/spark/jars/commons-pool2-2.6.2.jar,/home/spark/jars/mongo-spark-connector_2.12-10.5.0.jar,/home/spark/jars/mongodb-driver-sync-5.1.4.jar,/home/spark/jars/bson-5.1.4.jar,/home/spark/jars/mongodb-driver-core-5.1.4.jar,/home/spark/jars/bson-record-codec-5.1.4.jar,/home/spark/jars/spark-avro_2.12-3.1.3.jar,/home/spark/jars/postgresql-42.7.5.jar,/home/spark/jars/checker-qual-3.48.3.jar \
    /home/spark/jars/billing-engine-1.0-SNAPSHOT.jar




spark-submit \
    --class com.ensah.Main \
    --master spark://spark-master:7077 \
    --jars /home/spark/jars/spark-sql-kafka-0-10_2.12-3.1.3.jar,/home/spark/jars/spark-token-provider-kafka-0-10_2.12-3.1.3.jar,/home/spark/jars/kafka-clients-2.6.0.jar,/home/spark/jars/zstd-jni-1.4.8-1.jar,/home/spark/jars/lz4-java-1.7.1.jar,/home/spark/jars/snappy-java-1.1.8.2.jar,/home/spark/jars/slf4j-api-1.7.30.jar,/home/spark/jars/unused-1.0.0.jar,/home/spark/jars/commons-pool2-2.6.2.jar,/home/spark/jars/mongo-spark-connector_2.12-10.5.0.jar,/home/spark/jars/mongodb-driver-sync-5.1.4.jar,/home/spark/jars/bson-5.1.4.jar,/home/spark/jars/mongodb-driver-core-5.1.4.jar,/home/spark/jars/bson-record-codec-5.1.4.jar,/home/spark/jars/spark-avro_2.12-3.1.3.jar,/home/spark/jars/postgresql-42.7.5.jar,/home/spark/jars/checker-qual-3.48.3.jar \
    /home/spark/jars/spark-test-1.0-SNAPSHOT.jar

    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.3,org.mongodb.spark:mongo-spark-connector_2.12:10.5.0,org.apache.spark:spark-avro_2.12:3.1.3,org.postgresql:postgresql:42.7.5 \