# ABD-Project

A modular, end-to-end telecom data processing platform for generating, ingesting, normalizing, rating, and analyzing synthetic Call/Data Records (CDRs/EDRs) using modern streaming and batch technologies.

---

## 🏗️ Architecture Overview

This project simulates a real-world telecom data pipeline, including:

- **Synthetic CDR/EDR Generation** (Python)
- **Kafka-based Streaming Mediation** (Java, Spark, Kafka Streams, Python)
- **Rating Engines** (Java, Spark)
- **Data Storage** (Cassandra, Pinot, MongoDB, JDBC)
- **Visualization** (Apache Superset)
- **Containerized Orchestration** (Docker Compose)

See `Gloabl Architecture.pdf` for a detailed architecture diagram.

---

## 📦 Main Components

- **1-synthetic_cdr_generator/**  
  Generate realistic synthetic CDR/EDR data and push to Kafka. Includes error injection, Avro schema support, and flexible configuration.

- **streaming_mediation_kafka_streams/**  
  Java-based Kafka Streams app for CDR normalization, deduplication, and error handling.

- **streaming_mediation_spark_streaming/**  
  Python Spark Streaming pipeline for CDR normalization and enrichment.

- **billing-engine/**  
  Java Spark job for real-time/batch rating of CDRs.

- **monthly-rating-engine/**  
  Java Spark job for monthly aggregation and rating.

- **rating-engine/**  
  Java Spark job for rating and storing CDRs.

- **prepare-environment/**  
  Scripts for bootstrapping databases, connectors, and Pinot tables.

- **docker/**  
  Dockerfiles, Avro schemas, connector configs, and the main Docker Compose entry point.

- **compose-files/**  
  Additional Docker Compose files for various deployment modes.

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

Or use a specific mode (see `compose-files/` for options):

```bash
docker compose -f compose-files/compose.spark.cluster.yaml up --build
```

#### b. Prepare Databases & Schemas

```bash
cd prepare-environment
pip install -r requirements.txt
python main.py
```

This will:
- Create DB tables (Cassandra, Pinot, etc.)
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
  See `docker/` and `compose-files/` for service configs.

- **Avro Schemas:**  
  Located in `docker/avro/` and `1-synthetic_cdr_generator/avro/`.

- **Application Properties:**  
  Java modules: `src/main/resources/application.properties`  
  Python modules: `config/config.yaml`

- **Connector Configs:**  
  See `docker/connectors config/` and `prepare-environment/`.

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

- **Testing:**  
  (Add your test instructions here if available.)

---

## 📊 Visualization

- **Apache Superset** is included for dashboarding.  
  Access at [http://localhost:8088](http://localhost:8088) (default credentials: admin/admin).

---

## 🤝 Contributing

Pull requests are welcome!  
For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[MIT](LICENSE) (or your license of choice)

---

## 📬 Contact

For questions or support, open an issue or contact [your-email@example.com].

--- 