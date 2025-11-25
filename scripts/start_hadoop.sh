#!/bin/bash

# Start Hadoop Cluster for Gaming POC

echo "=== Starting Hadoop Cluster for Gaming Platform ==="
echo ""

# Check if docker and docker-compose are installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed"
    exit 1
fi

# Start the cluster
echo "Starting Hadoop services..."
docker-compose up -d

# Wait for services to be ready
echo ""
echo "Waiting for services to initialize (this may take 1-2 minutes)..."
sleep 30

# Check status
echo ""
echo "Service Status:"
docker-compose ps

# Create HDFS directories
echo ""
echo "Creating HDFS directories for gambling data..."
docker exec namenode hdfs dfs -mkdir -p /gambling/players 2>/dev/null
docker exec namenode hdfs dfs -mkdir -p /gambling/games 2>/dev/null
docker exec namenode hdfs dfs -mkdir -p /gambling/bets 2>/dev/null
docker exec namenode hdfs dfs -mkdir -p /gambling/sessions 2>/dev/null
docker exec namenode hdfs dfs -mkdir -p /gambling/transactions 2>/dev/null
docker exec namenode hdfs dfs -mkdir -p /gambling/events 2>/dev/null
docker exec namenode hdfs dfs -chmod -R 777 /gambling 2>/dev/null

echo ""
echo "=== Hadoop Cluster Started Successfully! ==="
echo ""
echo "Access the web interfaces:"
echo "  - HDFS NameNode:        http://localhost:9870"
echo "  - YARN ResourceManager: http://localhost:8088"
echo "  - Spark Master:         http://localhost:8080"
echo "  - Hue (SQL/File UI):    http://localhost:8888"
echo ""
echo "To view logs:    docker-compose logs -f"
echo "To stop cluster: docker-compose down"
echo ""
echo "Next steps:"
echo "  1. Generate sample data:  python scripts/hadoop_loader.py"
echo "  2. Access Hue at http://localhost:8888 to run SQL queries"
echo "  3. Check HADOOP_SETUP.md for detailed usage instructions"
echo ""