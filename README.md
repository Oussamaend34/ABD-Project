# ABD-Project

<div align="center" style="background: white; padding: 1em; border-radius: 8px;">
  <img src="./Global Architecture.svg" alt="Global Architecture Diagram" width="800"/>
</div>

A modular, end-to-end telecom data processing platform for generating, ingesting, normalizing, rating, and analyzing synthetic Call/Data Records (CDRs/EDRs) using modern streaming and batch technologies.

---

## 🏗️ Architecture Overview

This project simulates a real-world telecom data pipeline, including:

- **Synthetic CDR/EDR Generation** (Python)
- **Streaming Mediation** (Kafka Streams in Java, or Spark Streaming in Python as a variant)
- **Rating Engines** (Java, Spark)
- **Billing Engine** (Java, Spark)
- **Data Storage** (Pinot, MongoDB, PostgreSQL)
- **Visualization** (Apache Superset)
- **Containerized Orchestration** (Docker Compose)

See the architecture diagram above or `Gloabl Architecture.pdf` for more details.

---

## 📦 Main Components

- **1-synthetic_cdr_generator/**  
  Generate realistic synthetic CDR/EDR data and push to Kafka. Includes error injection, Avro schema support, and flexible configuration.

- **2-streaming_mediation_kafka_streams/**  
  Java-based Kafka Streams app for CDR normalization, deduplication, and error handling. 

- **streaming_mediation_spark_streaming/**  
  Python Spark Streaming pipeline for CDR normalization and enrichment. **This is a variant implementation of the mediation logic, providing an alternative to the Kafka Streams approach.**

- **3-daily-rating-engine/**, **4-monthly-rating-engine/**  
  Java Spark jobs for daily and monthly rating of CDRs.

- **5-billing-engine/**  
  Java Spark job for billing and aggregation, producing final billing results.

- **6-prepare-environment/**  
  Scripts for bootstrapping databases, connectors, Pinot tables, and initial data.

- **docker/**  
  Dockerfiles, connector configs, and the main Docker Compose entry point.

---

## ⚡️ Before You Start

To run the application, make sure you:

1. **Enter the `docker` folder**:
   ```bash
   cd docker
   ```
2. **Download the JDBC Connector from Confluent Hub**  
   [JDBC Connector Download & Instructions](https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc)

3. **Download the MongoDB Connector from Confluent Hub**  
   [MongoDB Connector Download & Instructions](https://www.confluent.io/hub/mongodb/kafka-connect-mongodb)

4. **Put the downloaded connectors in the `docker/plugins` folder**

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ABD-Project.git
cd ABD-Project
```

### 2. Prerequisites

- Docker & Docker Compose
- Java 11+ and Maven (for Java modules)
- Python 3.8+ (for Python modules)

### 3. Environment Setup

#### a. Start the Full Stack

The main entry point for running the project is the Docker Compose file located in the `docker/` folder:

```bash
docker compose -f docker/compose.yml up --build
```

#### b. Prepare Databases & Schemas

```bash
cd 6-prepare-environment
pip install -r requirements.txt
python main.py
```

This will:
- Create DB tables (Pinot, MongoDB, PostgreSQL, etc.)
- Register Kafka topics and Avro schemas
- Register Kafka Connect connectors

#### c. Generate Synthetic Data

```bash
cd 1-synthetic_cdr_generator
pip install -r requirements.txt
python main.py
```

Configure generation parameters in `1-synthetic_cdr_generator/config/config.yaml`.

---

## ⚙️ Configuration

- **Kafka, Schema Registry, Connect:**  
  See `docker/` for service configs.

- **Avro Schemas:**  
  Located in `6-prepare-environment/avro/`.

- **Application Properties:**  
  Java modules: `src/main/resources/application.properties`  
  Python modules: `config/config.yaml`

- **Connector Configs:**  
  See `docker/connectors config/` and `6-prepare-environment/`.

---

## 🧑‍💻 Development

- **Java Modules:**  
  Build with Maven:
  ```bash
  mvn clean package
  ```
  Run with:
  ```bash
  java -jar target/your-app.jar
  ```

- **Python Modules:**  
  Use virtualenv or conda, install requirements, and run scripts as needed.

---

## 📊 Visualization

- **Apache Superset** is included for dashboarding.  
  Access at [http://localhost:8088](http://localhost:8088) (default credentials: admin/admin).

---

## 🤝 Contributing

Pull requests are welcome!  
For major changes, please open an issue first to discuss what you would like to change.

---

## 📬 Contact

For questions or support, open an issue or contact [oussama.elalaouielismali@etu.uae.ac.ma].

--- 