# Online Gambling Platform - Hadoop & Kafka  POC

A proof-of-concept implementation of an online gambling platform's data infrastructure using Hadoop ecosystem.

## Project Overview

This POC demonstrates how to store, process, and analyze gambling platform data using:
- **Python** for data modeling
- **Hadoop HDFS** for distributed storage
- **Hive** for SQL analytics
- **Spark** for data processing
- **Kafka** for real-time event streaming
- **Docker** for easy deployment

## Project Structure

```
gaming_hadoop_poc/
├── models/                      # Python data models
│   ├── __init__.py
│   ├── player.py               # Player accounts and profiles
│   ├── game.py                 # Game catalog and metadata
│   ├── bet.py                  # Bets/wagers with outcomes
│   ├── session.py              # Gaming sessions tracking
│   ├── transaction.py          # Financial transactions
│   └── event.py                # Event logging and analytics
│
├── scripts/                     # Utility and operational scripts
│   ├── check_docker.sh         # Docker daemon status check
│   ├── create_hive_tables.sql  # Hive DDL statements
│   ├── hadoop_loader.py        # Load data to HDFS
│   ├── kafka_producer.py       # Real-time event producer
│   ├── kafka_consumer.py       # Real-time event consumer
│   ├── query_hive.py           # Query Hive via Beeline
│   ├── query_with_spark.py     # Spark-based data analysis
│   ├── run_tests.sh            # Test suite runner
│   ├── setup_hive_tables.sh    # Automated Hive setup
│   ├── start_hadoop.sh         # Start Hadoop cluster
│   ├── stop_hadoop.sh          # Stop Hadoop cluster
│   ├── test_hive_connection.py # Hive connectivity test
│   └── view_data.py            # Local data viewer
│
├── tests/                       # Test suite (153 tests)
│   ├── conftest.py             # Pytest fixtures and config
│   ├── test_player.py          # Player model tests (11)
│   ├── test_game.py            # Game model tests (15)
│   ├── test_bet.py             # Bet model tests (19)
│   ├── test_session.py         # Session model tests (15)
│   ├── test_transaction.py     # Transaction model tests (18)
│   ├── test_event.py           # Event model tests (20)
│   ├── test_integration.py     # Integration tests (8)
│   ├── test_kafka_producer.py  # Kafka producer tests (26)
│   └── test_kafka_consumer.py  # Kafka consumer tests (21)
│
├── data/                        # Generated data files (gitignored)
│   ├── players.json
│   ├── games.json
│   ├── bets.json
│   ├── sessions.json
│   ├── transactions.json
│   └── events.json
│
├── docs/                        # Documentation
│   ├── HADOOP_SETUP.md         # Hadoop setup guide
│   ├── DATA_GENERATION.md      # Data generation docs
│   ├── HIVE_TROUBLESHOOTING.md # Hive debugging guide
│   ├── QUICK_START.md          # Quick start guide
│   └── START_HERE.md           # Project introduction
│
├── .gitignore                   # Git ignore patterns
├── docker-compose.yml           # Multi-container orchestration
├── hadoop.env                   # Hadoop environment variables
├── hue.ini                      # Hue web UI configuration
├── main.py                      # Batch data generator
├── pytest.ini                   # Pytest configuration
├── README.md                    # This file
└── requirements.txt             # Python dependencies
```

## Data Models

### Core Entities

1. **Player** - Player accounts with balance, KYC status, and statistics
2. **Game** - Game catalog with RTP, volatility, and betting limits
3. **Bet** - Individual wagers with outcomes and payouts
4. **Session** - Player gaming sessions with device and location data
5. **Transaction** - Financial transactions (deposits, withdrawals, etc.)
6. **Event** - Analytics and audit event logging

All models include:
- Serialization to JSON for Hadoop storage
- Decimal precision for financial accuracy
- Comprehensive timestamps
- Domain-specific attributes

## Quick Start

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+

### 1. Install Python Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Generate Sample Data

```bash
python main.py
```

This generates realistic gambling data:
- 200 players
- 100 games
- 1,000 sessions
- 5,000 bets
- ~645 transactions
- ~1,700 events

Data is saved to `./data/*.json` files in JSONL format.

### 2a. Run Test Suite

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=models --cov-report=term-missing

# Use test runner script
./scripts/run_tests.sh
```

Test suite includes 153 tests covering all 6 data models and Kafka streaming.

### 3. Start Hadoop Cluster

```bash
# Option 1: Using script (recommended)
./scripts/start_hadoop.sh

# Option 2: Using docker-compose directly
docker-compose up -d
```

Wait 1-2 minutes for all services to initialize.

### 4. Generate Sample Data

```bash
python scripts/hadoop_loader.py
```

This creates 100 players, 50 games, and 1000 bets, saving them to:
- Local: `./data/*.json`
- HDFS: `/gambling/*/*.json`

### 5. Access Web Interfaces

Once the cluster is running:

- **HDFS NameNode**: http://localhost:9870
  - Browse HDFS file system
  - Monitor cluster health

- **YARN ResourceManager**: http://localhost:8088
  - View running jobs
  - Monitor resource usage

- **Spark Master**: http://localhost:8080
  - Spark cluster status
  - Active applications

- **Hue**: http://localhost:8888
  - SQL query editor
  - HDFS file browser
  - Data visualization

## Usage Examples

### Query Data with Hive

1. Access Hue at http://localhost:8888
2. Use the SQL editor to run queries
3. Example queries are in `HADOOP_SETUP.md`

### Process Data with Spark

```bash
# Access Spark master container
docker exec -it spark-master bash

# Start PySpark
pyspark --master spark://spark-master:7077

# Run analysis
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("GamblingAnalytics").getOrCreate()
bets_df = spark.read.json("hdfs://namenode:9000/gambling/bets/bets.json")
bets_df.show()
```

### Upload Custom Data

```bash
# Copy file to namenode
docker cp mydata.json namenode:/tmp/

# Upload to HDFS
docker exec namenode hdfs dfs -put /tmp/mydata.json /gambling/events/
```

### Real-Time Event Streaming with Kafka

Stream real-time gambling events to Kafka for immediate processing and analytics.

**Kafka Topics:**
- `gambling-bets` - Real-time betting events (60% of traffic)
- `gambling-transactions` - Financial transactions (20% of traffic)
- `gambling-player-activity` - Player activity events (20% of traffic)

**Start Producing Events:**

```bash
# Stream events at 10 events/second for 60 seconds
python scripts/kafka_producer.py --duration 60 --rate 10

# High-rate streaming (50 events/second)
python scripts/kafka_producer.py --duration 300 --rate 50
```

**Consume Events:**

In a separate terminal:

```bash
# Consume all events from topics
python scripts/kafka_consumer.py

# Consume specific number of messages
python scripts/kafka_consumer.py --max-messages 1000

# Consume from specific topics
python scripts/kafka_consumer.py --topics gambling-bets
```

**Real-Time Demo:**

Terminal 1 - Start consumer first:
```bash
python scripts/kafka_consumer.py
```

Terminal 2 - Start producer:
```bash
python scripts/kafka_producer.py --duration 60 --rate 20
```

Watch events flow in real-time! The consumer displays statistics every 10th message.

**Manage Kafka:**

```bash
# List topics
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092

# View topic details
docker exec kafka kafka-topics --describe --topic gambling-bets --bootstrap-server localhost:9092

# Check consumer groups
docker exec kafka kafka-consumer-groups --list --bootstrap-server localhost:9092
```

## Architecture

### Services

| Service | Port | Description |
|---------|------|-------------|
| NameNode | 9870, 9000 | HDFS master node |
| DataNode | - | HDFS data storage |
| ResourceManager | 8088 | YARN job scheduler |
| NodeManager | 8042 | YARN container manager |
| HistoryServer | 8188 | Job history |
| Hive Server | 10000 | SQL interface |
| Hive Metastore | 9083 | Metadata service |
| Spark Master | 8080, 7077 | Spark cluster master |
| Spark Worker | 8081 | Spark executor |
| Hue | 8888 | Web UI |
| Zookeeper | 2181 | Kafka coordination |
| Kafka | 9092, 9093 | Message broker |

### Data Flow

**Batch Processing:**
```
Python Models → JSON → HDFS → Hive Tables → SQL Queries
                               ↓
                            Spark Jobs → Analytics
```

**Real-Time Streaming:**
```
Kafka Producer → Kafka Topics → Kafka Consumer → Processing/Analytics
                      ↓
                 Spark Streaming (future)
```

## Common Operations

### Start Cluster
```bash
./scripts/start_hadoop.sh
```

### Stop Cluster
```bash
./scripts/stop_hadoop.sh
```

### View Logs
```bash
docker-compose logs -f namenode
docker-compose logs -f hive-server
```

### Create HDFS Directory
```bash
docker exec namenode hdfs dfs -mkdir /gambling/custom
docker exec namenode hdfs dfs -chmod 777 /gambling/custom
```

### List HDFS Files
```bash
docker exec namenode hdfs dfs -ls /gambling/
```

### Check Cluster Status
```bash
docker-compose ps
```

## Analytics Use Cases

### Player Analytics
- Player lifetime value calculation
- Churn prediction
- VIP tier analysis
- Geographic distribution

### Game Analytics
- RTP validation
- Game popularity trends
- Revenue by game type
- Provider performance

### Risk & Fraud
- Unusual betting patterns
- Multi-account detection
- Transaction monitoring
- Session anomalies

### Business Intelligence
- Daily/monthly revenue
- Payment method analysis
- Platform usage (mobile vs desktop)
- Retention metrics

## Testing

The project includes a comprehensive test suite with 153 tests:

- **tests/test_player.py** - Player model tests (11 tests)
- **tests/test_game.py** - Game model tests (15 tests)
- **tests/test_bet.py** - Bet model tests (19 tests)
- **tests/test_session.py** - Session model tests (15 tests)
- **tests/test_transaction.py** - Transaction model tests (18 tests)
- **tests/test_event.py** - Event model tests (20 tests)
- **tests/test_integration.py** - Integration tests (8 tests)
- **tests/test_kafka_producer.py** - Kafka producer tests (26 tests)
- **tests/test_kafka_consumer.py** - Kafka consumer tests (21 tests)

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_player.py -v

# Generate coverage report
pytest tests/ --cov=models --cov-report=html
```

See `tests/README.md` for detailed testing documentation.

## Data Analysis

### Quick Analysis with Spark (No Hive Setup Needed!)

```bash
# Run comprehensive analytics
python scripts/query_with_spark.py

# Interactive SQL mode
python scripts/query_with_spark.py -i
```

This analyzes all your data immediately without Hive connection issues!

### Alternative: Using Hive/Beeline

If you need Hive, see **HIVE_TROUBLESHOOTING.md** for connection setup.

## Documentation

- **HADOOP_SETUP.md** - Detailed Hadoop setup and usage guide
- **DATA_GENERATION.md** - Data generation documentation
- **tests/README.md** - Complete testing documentation
- **docker-compose.yml** - Service configuration

## Troubleshooting

### Services won't start
```bash
docker-compose down -v
docker-compose up -d
```

### Out of memory
Reduce resource limits in `hadoop.env`:
```
YARN_CONF_yarn_nodemanager_resource_memory___mb=8192
```

### Can't connect to HDFS
Wait 1-2 minutes after startup, then check:
```bash
docker exec namenode hdfs dfsadmin -report
```

### HDFS in safe mode
```bash
docker exec namenode hdfs dfsadmin -safemode leave
```

## Development

### Add New Data Model

1. Create model in `models/` directory
2. Add `to_dict()` method for serialization
3. Import in `models/__init__.py`
4. Create corresponding Hive table schema

### Customize Configuration

- Hadoop settings: `hadoop.env`
- Docker services: `docker-compose.yml`
- Hue interface: `hue.ini`

## Performance Considerations

- **Partitioning**: Partition large tables by date
- **Compression**: Use Parquet format for storage efficiency
- **Replication**: Set `dfs.replication=3` for production
- **Memory**: Allocate sufficient RAM to containers
- **Network**: Use dedicated network for multi-host clusters

## Production Recommendations

1. Use separate nodes for NameNode/DataNode
2. Enable HDFS high availability (HA)
3. Set up backup/disaster recovery
4. Implement data retention policies
5. Monitor with Prometheus/Grafana
6. Secure with Kerberos authentication
7. Enable encryption at rest and in transit

## Next Steps

- [x] Implement streaming data ingestion with Kafka
- [ ] Add real-time analytics with Spark Streaming
- [ ] Create scheduled ETL jobs
- [ ] Build ML models for player behavior
- [ ] Implement data quality checks
- [ ] Add visualization dashboards

## License

POC for demonstration purposes.

## Support

For detailed Hadoop usage, see `HADOOP_SETUP.md`.