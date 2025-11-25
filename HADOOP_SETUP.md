# Hadoop Environment Setup - Gaming POC

## Overview

This Docker Compose setup provides a complete Hadoop ecosystem for the online gambling platform POC, including:

- **HDFS**: Distributed file system for storing gambling data
- **YARN**: Resource management and job scheduling
- **Hive**: SQL-like queries on gambling datasets
- **Spark**: Fast data processing for analytics
- **Hue**: Web UI for data exploration and queries

## Architecture Components

### Core Services

1. **NameNode** (Port 9870, 9000)
   - HDFS master node
   - Manages file system namespace
   - Web UI: http://localhost:9870

2. **DataNode**
   - Stores actual data blocks
   - Works with NameNode

3. **ResourceManager** (Port 8088)
   - YARN master for job scheduling
   - Web UI: http://localhost:8088

4. **NodeManager** (Port 8042)
   - Runs containers and monitors resources
   - Web UI: http://localhost:8042

5. **HistoryServer** (Port 8188)
   - MapReduce job history
   - Web UI: http://localhost:8188

### Data Processing

6. **Hive Server** (Port 10000)
   - SQL queries on HDFS data
   - Stores player, game, bet data

7. **Hive Metastore** (Port 9083)
   - Stores metadata for Hive tables
   - Uses PostgreSQL backend

8. **Spark Master** (Port 8080, 7077)
   - Spark cluster master
   - Web UI: http://localhost:8080

9. **Spark Worker** (Port 8081)
   - Executes Spark jobs

### Web Interface

10. **Hue** (Port 8888)
    - Web-based data exploration
    - Query editor for Hive/Spark
    - HDFS browser
    - Access: http://localhost:8888

## Quick Start

### 1. Start Hadoop Cluster

```bash
docker-compose up -d
```

### 2. Check Service Status

```bash
docker-compose ps
```

All services should be in "Up" state.

### 3. Access Web Interfaces

- **HDFS NameNode**: http://localhost:9870
- **YARN ResourceManager**: http://localhost:8088
- **Spark Master**: http://localhost:8080
- **Hue**: http://localhost:8888

### 4. Create Data Directory in HDFS

```bash
# Access namenode container
docker exec -it namenode bash

# Create directories for gambling data
hdfs dfs -mkdir -p /gambling/players
hdfs dfs -mkdir -p /gambling/games
hdfs dfs -mkdir -p /gambling/bets
hdfs dfs -mkdir -p /gambling/sessions
hdfs dfs -mkdir -p /gambling/transactions
hdfs dfs -mkdir -p /gambling/events

# Set permissions
hdfs dfs -chmod -R 777 /gambling
```

## Working with Gaming Data

### Upload Sample Data

```bash
# From your local machine, create sample JSON data
python main.py > sample_data.json

# Copy to namenode container
docker cp sample_data.json namenode:/tmp/

# Upload to HDFS
docker exec -it namenode bash
hdfs dfs -put /tmp/sample_data.json /gambling/events/
```

### Create Hive Tables

```bash
# Access Hive
docker exec -it hive-server bash
beeline -u jdbc:hive2://localhost:10000

# Create database
CREATE DATABASE IF NOT EXISTS gambling;
USE gambling;

# Create Players table
CREATE EXTERNAL TABLE players (
    player_id STRING,
    username STRING,
    email STRING,
    registration_date TIMESTAMP,
    country STRING,
    balance DECIMAL(10,2),
    currency STRING,
    status STRING,
    kyc_verified BOOLEAN,
    vip_tier STRING,
    total_deposits DECIMAL(10,2),
    total_withdrawals DECIMAL(10,2),
    total_wagered DECIMAL(10,2),
    total_won DECIMAL(10,2),
    created_at TIMESTAMP
)
STORED AS PARQUET
LOCATION '/gambling/players';

# Create Bets table
CREATE EXTERNAL TABLE bets (
    bet_id STRING,
    player_id STRING,
    game_id STRING,
    session_id STRING,
    bet_amount DECIMAL(10,2),
    currency STRING,
    bet_type STRING,
    bet_status STRING,
    payout_amount DECIMAL(10,2),
    win_multiplier DECIMAL(5,2),
    is_jackpot BOOLEAN,
    bet_timestamp TIMESTAMP,
    settled_timestamp TIMESTAMP
)
PARTITIONED BY (bet_date STRING)
STORED AS PARQUET
LOCATION '/gambling/bets';

# Create Games table
CREATE EXTERNAL TABLE games (
    game_id STRING,
    game_name STRING,
    game_type STRING,
    provider STRING,
    rtp DECIMAL(5,2),
    volatility STRING,
    min_bet DECIMAL(10,2),
    max_bet DECIMAL(10,2),
    total_plays INT,
    total_wagered DECIMAL(15,2),
    total_paid DECIMAL(15,2)
)
STORED AS PARQUET
LOCATION '/gambling/games';

# Create Sessions table
CREATE EXTERNAL TABLE sessions (
    session_id STRING,
    player_id STRING,
    session_start TIMESTAMP,
    session_end TIMESTAMP,
    device_type STRING,
    platform STRING,
    country STRING,
    total_bets INT,
    total_wagered DECIMAL(10,2),
    total_won DECIMAL(10,2),
    session_duration_seconds INT
)
PARTITIONED BY (session_date STRING)
STORED AS PARQUET
LOCATION '/gambling/sessions';

# Create Transactions table
CREATE EXTERNAL TABLE transactions (
    transaction_id STRING,
    player_id STRING,
    transaction_type STRING,
    amount DECIMAL(10,2),
    currency STRING,
    status STRING,
    payment_method STRING,
    payment_provider STRING,
    balance_before DECIMAL(10,2),
    balance_after DECIMAL(10,2),
    transaction_timestamp TIMESTAMP
)
PARTITIONED BY (transaction_date STRING)
STORED AS PARQUET
LOCATION '/gambling/transactions';
```

### Example Queries

```sql
-- Top 10 players by total wagered
SELECT player_id, SUM(bet_amount) as total_wagered
FROM bets
WHERE bet_status = 'settled'
GROUP BY player_id
ORDER BY total_wagered DESC
LIMIT 10;

-- Daily revenue by game type
SELECT
    g.game_type,
    DATE(b.bet_timestamp) as bet_date,
    SUM(b.bet_amount - b.payout_amount) as net_revenue
FROM bets b
JOIN games g ON b.game_id = g.game_id
GROUP BY g.game_type, DATE(b.bet_timestamp);

-- Player lifetime value
SELECT
    p.player_id,
    p.username,
    p.total_deposits - p.total_withdrawals as net_deposits,
    p.total_wagered,
    p.total_won,
    p.total_wagered - p.total_won as house_profit
FROM players p
WHERE p.status = 'active';

-- Session analysis
SELECT
    device_type,
    AVG(session_duration_seconds/60) as avg_session_minutes,
    AVG(total_bets) as avg_bets_per_session,
    AVG(total_wagered) as avg_wagered_per_session
FROM sessions
GROUP BY device_type;
```

## Using Spark for Analytics

```bash
# Access Spark master
docker exec -it spark-master bash

# Start PySpark
pyspark --master spark://spark-master:7077

# In PySpark shell:
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("GamblingAnalytics") \
    .getOrCreate()

# Read parquet data
bets_df = spark.read.parquet("hdfs://namenode:9000/gambling/bets")

# Analysis
daily_stats = bets_df.groupBy("bet_date") \
    .agg({
        "bet_amount": "sum",
        "payout_amount": "sum",
        "bet_id": "count"
    })

daily_stats.show()
```

## Data Pipeline Example

Create a script to load Python models into Hadoop:

```python
# hadoop_loader.py
import json
from models import Player, Game, Bet, Session, Transaction, Event
from hdfs import InsecureClient

# Connect to HDFS
client = InsecureClient('http://localhost:9870', user='root')

def upload_to_hdfs(data_list, hdfs_path):
    """Upload list of model instances to HDFS as JSON"""
    json_data = [item.to_dict() for item in data_list]

    with client.write(hdfs_path, encoding='utf-8') as writer:
        for record in json_data:
            writer.write(json.dumps(record) + '\n')

# Usage
players = [player1, player2, player3]
upload_to_hdfs(players, '/gambling/players/players.json')
```

## Monitoring and Maintenance

### View Logs

```bash
# View specific service logs
docker-compose logs -f namenode
docker-compose logs -f hive-server
docker-compose logs -f spark-master

# View all logs
docker-compose logs -f
```

### Stop Cluster

```bash
docker-compose down
```

### Stop and Remove Data

```bash
docker-compose down -v
```

### Restart Single Service

```bash
docker-compose restart namenode
```

## Troubleshooting

### Service Won't Start

Check dependencies:
```bash
docker-compose logs namenode
```

### Out of Memory

Adjust memory settings in `hadoop.env`:
```bash
YARN_CONF_yarn_nodemanager_resource_memory___mb=8192
YARN_CONF_yarn_scheduler_maximum___allocation___mb=8192
```

### HDFS Safe Mode

```bash
docker exec -it namenode bash
hdfs dfsadmin -safemode leave
```

### Reset Everything

```bash
docker-compose down -v
docker system prune -a
docker-compose up -d
```

## Performance Tuning

### For Production

1. Increase replication factor in `hadoop.env`:
   ```
   HDFS_CONF_dfs_replication=3
   ```

2. Add more DataNodes and Spark workers in `docker-compose.yml`

3. Tune YARN memory settings based on your host machine

4. Enable compression for storage efficiency

5. Partition tables by date for better query performance

## Next Steps

1. Set up automated data ingestion pipelines
2. Create scheduled analytics jobs with Spark
3. Implement real-time streaming with Kafka + Spark Streaming
4. Add data quality validation
5. Set up monitoring with Prometheus/Grafana
6. Implement backup strategies for critical data

## Resources

- Hadoop Documentation: https://hadoop.apache.org/docs/
- Hive Documentation: https://hive.apache.org/
- Spark Documentation: https://spark.apache.org/docs/
- Hue Documentation: https://docs.gethue.com/