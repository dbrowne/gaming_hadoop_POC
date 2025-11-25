#!/bin/bash

echo "=== Docker Status Check ==="
echo ""

# Check if Docker daemon is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker daemon is NOT running"
    echo ""
    echo "To start Docker:"
    echo "  sudo systemctl start docker"
    echo ""
    echo "To enable Docker to start on boot:"
    echo "  sudo systemctl enable docker"
    exit 1
fi

echo "✓ Docker daemon is running"
echo ""

# Check running containers
RUNNING=$(docker ps --filter "name=namenode" --filter "name=hue" --filter "name=hive-server" --format "{{.Names}}" | wc -l)

if [ "$RUNNING" -eq 0 ]; then
    echo "❌ Hadoop containers are NOT running"
    echo ""
    echo "To start the cluster:"
    echo "  cd /home/djb/GRepository/pythonstuffs/gaming_hadoop_poc"
    echo "  docker-compose up -d"
    echo ""
    echo "Wait 2-3 minutes, then access:"
    echo "  - Hue: http://localhost:8888"
    echo "  - HDFS: http://localhost:9870"
    echo "  - YARN: http://localhost:8088"
    exit 1
fi

echo "✓ Hadoop containers are running"
echo ""
echo "Active services:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "NAME|namenode|hue|hive|resourcemanager|spark"

echo ""
echo "=== Access Points ==="
echo "Hue Web UI:           http://localhost:8888"
echo "HDFS NameNode:        http://localhost:9870"
echo "YARN ResourceManager: http://localhost:8088"
echo "Spark Master:         http://localhost:8080"
echo ""
echo "=== Query Your Data ==="
echo "Python Analytics:     python scripts/query_with_spark.py"
echo "Hive CLI:             docker exec -it hive-server beeline -u jdbc:hive2://localhost:10000"
echo "View Data:            python scripts/view_data.py"
echo ""
