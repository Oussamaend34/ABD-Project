package com.ensah;


import com.ensah.telecom.events.NormalizedCDR;
import com.ensah.telecom.events.NormalizedErrorCDR;
import io.confluent.kafka.serializers.AbstractKafkaSchemaSerDeConfig;
import io.confluent.kafka.streams.serdes.avro.GenericAvroSerde;
import io.confluent.kafka.streams.serdes.avro.SpecificAvroSerde;
import org.apache.avro.generic.GenericRecord;
import org.apache.kafka.common.serialization.Serde;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.io.InputStream;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.Collections;
import java.util.Map;
import java.util.Properties;
import java.util.regex.Pattern;

public class Main {
    public static final String INPUT_TOPIC = "cdr.input.topic";
    public static final String OK_OUTPUT_TOPIC = "cdr.ok.topic";
    public static final String ERROR_OUTPUT_TOPIC = "cdr.error.topic";
    public static final String CDR_TYPE = "cdr.type";

    public static final String APPLICATION_ID_CONFIG_ENV = "APPLICATION_ID_CONFIG";
    public static final String BOOTSTRAP_SERVERS_CONFIG_ENV = "BOOTSTRAP_SERVERS_CONFIG";
    public static final String SCHEMA_REGISTRY_URL_CONFIG_ENV = "SCHEMA_REGISTRY_URL_CONFIG";
    public static final String INPUT_TOPIC_ENV = "INPUT_TOPIC";
    public static final String OK_OUTPUT_TOPIC_ENV = "OK_OUTPUT_TOPIC";
    public static final String ERROR_OUTPUT_TOPIC_ENV = "ERROR_OUTPUT_TOPIC";
    public static final String CDR_TYPE_ENV = "CDR_TYPE";


    public static void main(String[] args) throws IOException {
        final Logger log = LoggerFactory.getLogger(Main.class);
        final Properties streamsProps = getProperties();
        final Map<String, String> serdeConfig = Collections.singletonMap(
                AbstractKafkaSchemaSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG,
                streamsProps.getProperty(AbstractKafkaSchemaSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG)
        );

        final Serde<String> keySerde = Serdes.String();

        final Serde<GenericRecord> CDRSerdeInput = new GenericAvroSerde();
        CDRSerdeInput.configure(serdeConfig, false);

        final Serde<NormalizedCDR> normalizedCDRSerde = new SpecificAvroSerde<>();
        normalizedCDRSerde.configure(serdeConfig, false);

        final Serde<NormalizedErrorCDR> normalizedErrorCDRSerde = new SpecificAvroSerde<>();
        normalizedErrorCDRSerde.configure(serdeConfig, false);

        StreamsBuilder builder = new StreamsBuilder();

        final String inputTopic = streamsProps.getProperty(INPUT_TOPIC);
        final String okOutputTopic = streamsProps.getProperty(OK_OUTPUT_TOPIC);
        final String errorOutputTopic = streamsProps.getProperty(ERROR_OUTPUT_TOPIC);
        final String cdrType = streamsProps.getProperty(CDR_TYPE);

        KStream<String, GenericRecord> CDRStream = builder.stream(inputTopic, Consumed.with(keySerde, CDRSerdeInput));
        KStream<String, NormalizedErrorCDR> normalizedCDRStream = CDRStream
                .mapValues(value -> {
                            String record_type = value.get("record_type").toString();
                            String uuid = value.get("uuid").toString();
                            String msisdn = null;
                            String counterpartyMsisdn = null;
                            Integer durationSec = null;
                            Double dataVolumeMb = null;
                            String cellId = value.get("cell_id").toString();
                            String technology = value.get("technology").toString();
                            Instant timestamp = Instant.ofEpochMilli((Long) value.get("timestamp"));
                            if (
                                    timestamp.isBefore(Instant.now().minus(1, ChronoUnit.DAYS)) || timestamp.isAfter(Instant.now().plus(1, ChronoUnit.DAYS))
                            ){
                                timestamp = Instant.now();
                            }
                            if (record_type == null) {
                                record_type = cdrType;
                            }
                            if (record_type.equals("voice")) {
                                msisdn = normalizeMsisdn(value.get("caller_id").toString());
                                counterpartyMsisdn = normalizeMsisdn(value.get("callee_id").toString());
                                durationSec = (Integer) value.get("duration_sec");
                            }
                            if (record_type.equals("sms")) {
                                msisdn = normalizeMsisdn(value.get("sender_id").toString());
                                counterpartyMsisdn = normalizeMsisdn(value.get("receiver_id").toString());
                            }
                            if (record_type.equals("data")) {
                                msisdn = normalizeMsisdn(value.get("user_id").toString());
                                dataVolumeMb = (Double) value.get("data_volume_mb");
                                durationSec = (Integer) value.get("session_duration_sec");
                            }
                            return NormalizedErrorCDR.newBuilder()
                                    .setUuid(uuid)
                                    .setMsisdn(msisdn)
                                    .setCounterpartyMsisdn(counterpartyMsisdn)
                                    .setDurationSec(durationSec)
                                    .setDataVolumeMb(dataVolumeMb)
                                    .setCellId(cellId)
                                    .setTechnology(technology)
                                    .setTimestamp(timestamp)
                                    .setRecordType(record_type)
                                    .setStatus("ok")
                                    .build();
                        }
                );
        final String msisdnPattern = "^212[6-7][0-9]{8}$";
        final String cellIdPattern = "^[a-z][a-z_]*?_[0-9]*$";

        normalizedCDRStream = normalizedCDRStream.mapValues(value -> {
            if (
                    value.getMsisdn() == null || !Pattern.matches(msisdnPattern, value.getMsisdn()) || (value.getUuid() == null && value.getTimestamp() == null)
            ){
                value.setStatus("error");
            } else if (value.getRecordType().equals("voice") && (value.getDurationSec() == null || value.getDurationSec() <=0 || value.getDurationSec() > 9999)) {
                value.setStatus("error");
            } else if (value.getRecordType().equals("data") && (value.getDurationSec() == null || value.getDurationSec() <=0 || value.getDurationSec() > 9999 || value.getDataVolumeMb() == null || value.getDataVolumeMb() <= 0 || value.getDataVolumeMb() > 9999 )) {
                value.setStatus("error");
            } else if (value.getCellId() == null || !Pattern.matches(cellIdPattern, value.getCellId()) || value.getTechnology() == null || value.getUuid() == null || value.getTimestamp() == null) {
                value.setStatus("partial");
            } else {
                value.setStatus("ok");
            }
            return value;
        });
        KStream<String, NormalizedCDR> okStream = normalizedCDRStream
                .filter((key, value) -> value.getStatus().equals("ok") || value.getStatus().equals("partial"))
                .mapValues(value -> NormalizedCDR.newBuilder()
                        .setUuid(value.getUuid())
                        .setMsisdn(value.getMsisdn())
                        .setCounterpartyMsisdn(value.getCounterpartyMsisdn())
                        .setDurationSec(value.getDurationSec())
                        .setDataVolumeMb(value.getDataVolumeMb())
                        .setCellId(value.getCellId())
                        .setTechnology(value.getTechnology())
                        .setTimestamp(value.getTimestamp())
                        .setRecordType(value.getRecordType())
                        .setStatus(value.getStatus())
                        .build());
        KStream<String, NormalizedErrorCDR> errorStream = normalizedCDRStream.filter((key, value) -> value.getStatus().equals("error"));
        okStream.filter((key, value) -> key != null && value != null)
                .peek((key, value) -> log.info("Normalized OK {} : Key: {} Value: {}", value.getRecordType(), key, value))
                .to(okOutputTopic, Produced.with(keySerde, normalizedCDRSerde));
        errorStream.filter((key, value) -> key != null && value != null)
                .peek((key, value) -> log.info("Normalized ERROR {} : Key: {} Value: {}", value.getRecordType(), key, value))
                .to(errorOutputTopic, Produced.with(keySerde, normalizedErrorCDRSerde));
        KafkaStreams streams = new KafkaStreams(builder.build(), streamsProps);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            log.info("Shutting down Kafka Streams application...");
            streams.close();
            log.info("Kafka Streams application shut down complete.");
        }));

        try {
            log.info("Starting Kafka Streams application...");
            streams.start();
            log.info("Kafka Streams application started successfully.");
        } catch (Exception e) {
            log.error("Error starting Kafka Streams application: {}", e.getMessage());
            streams.close();
            throw e;
        }
    }

    public static String normalizeMsisdn(CharSequence msisdn) {
        if (msisdn == null) {
            return null;
        }
        String digits = msisdn.toString().replaceAll("\\D", "");
        if (digits.startsWith("06") || digits.startsWith("07")) {
            digits = "212" + digits.substring(1);
        } else if (digits.startsWith("00212")) {
            digits = digits.substring(2);
        } else if (digits.startsWith("+212")) {
            digits = digits.substring(1);
        } else if (digits.startsWith("212")) {
            return digits.startsWith("212") ? digits : null;
        } else {
            return null;
        }
        return digits.startsWith("212") ? digits : null;
    }

    private static Properties getProperties() throws IOException {
        final Properties streamsProps = new Properties();
        try(InputStream fis = Main.class.getClassLoader().getResourceAsStream("streams.properties")) {
            if (fis != null) {
                streamsProps.load(fis);
            } else {
                throw new IOException("Properties file not found");
            }
        }
        if (streamsProps.getProperty(StreamsConfig.APPLICATION_ID_CONFIG) == null) {
            streamsProps.put(StreamsConfig.APPLICATION_ID_CONFIG, "streaming-mediation-sms-app");
        }
        if (streamsProps.getProperty(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG) == null) {
            streamsProps.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        }
        if (streamsProps.getProperty(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG) == null) {
            streamsProps.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        }
        if (streamsProps.getProperty(AbstractKafkaSchemaSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG) == null) {
            streamsProps.put(AbstractKafkaSchemaSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG, "http://localhost:8081");
        }
        overrideWithEnv(streamsProps, StreamsConfig.APPLICATION_ID_CONFIG, APPLICATION_ID_CONFIG_ENV);
        overrideWithEnv(streamsProps, StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS_CONFIG_ENV);
        overrideWithEnv(streamsProps, AbstractKafkaSchemaSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG, SCHEMA_REGISTRY_URL_CONFIG_ENV);
        overrideWithEnv(streamsProps, INPUT_TOPIC, INPUT_TOPIC_ENV);
        overrideWithEnv(streamsProps, OK_OUTPUT_TOPIC, OK_OUTPUT_TOPIC_ENV);
        overrideWithEnv(streamsProps, ERROR_OUTPUT_TOPIC, ERROR_OUTPUT_TOPIC_ENV);
        overrideWithEnv(streamsProps, CDR_TYPE, CDR_TYPE_ENV);

        assert streamsProps.getProperty(StreamsConfig.APPLICATION_ID_CONFIG) != null : "APPLICATION_ID_CONFIG is not set";
        assert streamsProps.getProperty(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG) != null : "BOOTSTRAP_SERVERS_CONFIG is not set";
        assert streamsProps.getProperty(AbstractKafkaSchemaSerDeConfig.SCHEMA_REGISTRY_URL_CONFIG) != null : "SCHEMA_REGISTRY_URL_CONFIG is not set";
        assert streamsProps.getProperty(INPUT_TOPIC) != null : "INPUT_TOPIC is not set";
        assert streamsProps.getProperty(OK_OUTPUT_TOPIC) != null : "OK_OUTPUT_TOPIC is not set";
        assert streamsProps.getProperty(ERROR_OUTPUT_TOPIC) != null : "ERROR_OUTPUT_TOPIC is not set";
        assert streamsProps.getProperty(CDR_TYPE) != null : "CDR_TYPE is not set";
        assert streamsProps.getProperty(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG) != null : "DEFAULT_KEY_SERDE_CLASS_CONFIG is not set";

        return streamsProps;
    }

    private static void overrideWithEnv(Properties props, String configKey, String envVar) {
        String value = System.getenv(envVar);
        if (value != null && !value.isEmpty()) {
            props.setProperty(configKey, value);
        }
    }
}