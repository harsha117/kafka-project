
# Scalable and Resilient Event-Based Message Exchange for Real-Time Product Information Updates

## Overview
This project implements a scalable and resilient event-based message exchange system for real-time product information updates. It simulates a multi-hybrid cloud environment with Kafka as the message broker, FastAPI applications for message production and consumption, and a WebSocket-powered dashboard for real-time updates visualization.

---

## Architecture Design

### Components
1. **Producer Service**:
   - Built with FastAPI to handle incoming HTTP requests.
   - Publishes events (e.g., price updates, discounts, country updates) to Kafka topics.

2. **Kafka**:
   - Acts as the message broker for reliable event delivery.
   - Topics are defined for each type of event.

3. **Consumer Service**:
   - Consumes messages from Kafka topics.
   - Forwards the events to the WebSocket server for real-time visualization.

4. **Dashboard**:
   - Built with FastAPI and WebSocket to provide a real-time UI.
   - Displays incoming events in a structured format.

5. **Monitoring Stack**:
   - **Prometheus** for scraping metrics from services.
   - **Grafana** for visualizing metrics and setting up alerts.

### Architecture Diagram
```plaintext
+--------------------+          +--------------------+          +--------------------+
|  Producer Service  |   HTTP   |       Kafka        |   Kafka  |  Consumer Service  |
| (FastAPI)          +--------->+  (Message Broker)  +--------->+  (FastAPI + WS)    |
+--------------------+          +--------------------+          +--------------------+
                                                             |
                                                             |
                                                     WebSocket|
                                                             v
                                                     +--------------------+
                                                     |      Dashboard     |
                                                     |   (Real-Time UI)   |
                                                     +--------------------+

+--------------------+          +--------------------+
|     Prometheus     |<---------|      Services      |
+--------------------+          +--------------------+
         |
         v
+--------------------+
|      Grafana       |
+--------------------+
```

---

## Features
- **Event Handling:** Supports product price updates, country updates, and specific product discount updates.
- **Geographical Distribution:** Simulates message exchange between on-premises and cloud environments.
- **Dashboard:** Real-time visualization of product updates.
- **Observability:** Prometheus and Grafana integration for metrics and monitoring.
- **Scalability:** Kafka-based message broker ensures scalability and resilience.

---

## Prerequisites
1. Python 3.9 or above
2. Java (JDK 8 or above)
3. Apache Kafka
4. Prometheus and Grafana

---

## Installation

### For Linux

#### Install Java
```bash
sudo apt update
sudo apt install -y openjdk-11-jdk
java -version
```

#### Install Python
```bash
sudo apt install -y python3 python3-pip python3-venv
python3 --version
pip3 --version
```

#### Install Kafka
1. Download Kafka:
   ```bash
   wget https://downloads.apache.org/kafka/3.5.0/kafka_2.13-3.5.0.tgz
   ```
2. Extract and set up Kafka:
   ```bash
   tar -xvzf kafka_2.13-3.5.0.tgz
   cd kafka_2.13-3.5.0
   ```
3. Start Zookeeper:
   ```bash
   bin/zookeeper-server-start.sh config/zookeeper.properties
   ```
4. Start Kafka server:
   ```bash
   bin/kafka-server-start.sh config/server.properties
   ```

### For Windows

#### Install Java
1. Download JDK from [Oracle JDK](https://www.oracle.com/java/technologies/javase-downloads.html).
2. Install and configure the `JAVA_HOME` environment variable.
   ```
   setx JAVA_HOME "C:\Program Files\Java\jdk-11.0.x"
   setx PATH "%JAVA_HOME%\bin;%PATH%"
   ```
3. Verify installation:
   ```
   java -version
   ```

#### Install Python
1. Download Python from [Python.org](https://www.python.org/downloads/).
2. During installation, enable the option to add Python to the system PATH.
3. Verify installation:
   ```
   python --version
   pip --version
   ```

#### Install Kafka
1. Download Kafka from [Apache Kafka](https://kafka.apache.org/downloads).
2. Extract Kafka to a preferred directory (e.g., `C:\kafka`).
3. Start Zookeeper:
   ```cmd
   cd C:\kafka\bin\windows
   zookeeper-server-start.bat ..\..\config\zookeeper.properties
   ```
4. Start Kafka server:
   ```cmd
   kafka-server-start.bat ..\..\config\server.properties
   ```

---

## Setting Up the Python Environment

### For Both Linux and Windows
1. Clone the repository:
   ```bash
   git clone https://github.com/harsha117/kafka-project.git
   cd kafka-project
   ```
2. Create a Python virtual environment:
   ```bash
   python3 -m venv venv  # Use `python` on Windows
   source venv/bin/activate  # Use `venv\Scripts\activate` on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Applications

### Producer
Start the `producer.py` service:
```bash
uvicorn producer:app --reload --port 8000
```

### Consumer
Run the `consumer.py` script:
```bash
python consumer.py
```

### Dashboard
Start the `dashboard.py` service:
```bash
uvicorn dashboard:app --reload --port 3000
```

---

## Kafka Topics Created
The following Kafka topics are created to handle various event types:
1. **`product-price-update`**: Handles product price update events.
2. **`product-discount-update`**: Handles product discount update events.
3. **`product-country-update`**: Handles product country update events.

---

## Example CURL Commands

### Product Price Update Event
```bash
curl -X POST "http://localhost:8000/publish-event" -H "Content-Type: application/json" -d '{"event_type": "product-price-update", "data": {"product_id": 123, "price": 10.00}}'
```

### Product Discount Update Event
```bash
curl -X POST "http://localhost:8000/publish-event" -H "Content-Type: application/json" -d '{"event_type": "product-discount-update", "data": {"product_id": 123, "discount": 10.00}}'
```

### Product Country Update Event
```bash
curl -X POST "http://localhost:8000/publish-event" -H "Content-Type: application/json" -d '{"event_type": "product-country-update", "data": {"product_id": 123, "country": "US"}}'
```

---

## Monitoring Setup

### Prometheus
1. Ensure Prometheus is running:
   ```bash
   ./prometheus --config.file=prometheus.yml
   ```
2. Verify at `http://localhost:9090`.

### Kafka Exporter
1. Ensure Kafka Exporter is running.
2. Verify metrics are exposed at `http://localhost:9308/metrics`.

### Grafana
1. Access Grafana at `http://localhost:3001`.
2. Configure Prometheus as a data source and import dashboards.

---

## File Structure
```
├── producer.py       # Event producer API
├── consumer.py       # Kafka consumer
├── dashboard.py      # Real-time dashboard
├── html/dashboard.html  # Frontend for the dashboard
├── prometheus.yml   # Prometheus configuration
├── requirements.txt  # Python dependencies
```

---

## Assumptions
1. All services are running on `localhost` for simplicity.
2. WebSocket communication is simulated between consumer and dashboard.
3. Prometheus is configured with default settings for local monitoring.

---

## Future Improvements
1. **Cloud Deployment:** Migrate services to cloud platforms like AWS, Azure, or GCP.
2. **High Availability:** Configure Kafka brokers for redundancy.
3. **Enhanced Monitoring:** Add distributed tracing with tools like Jaeger.
4. **Authentication:** Secure APIs and WebSocket endpoints with tokens.

---

## Troubleshooting
1. Ensure Kafka and Zookeeper are running before starting services.
2. Use the browser console to debug WebSocket connections.
3. Check Prometheus logs for metric scraping errors.

---

## References
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
