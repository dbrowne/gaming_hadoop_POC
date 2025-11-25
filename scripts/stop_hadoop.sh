#!/bin/bash

# Stop Hadoop Cluster

echo "=== Stopping Hadoop Cluster ==="
echo ""

# Stop all services
docker-compose down

echo ""
echo "Hadoop cluster stopped successfully."
echo ""
echo "To remove all data volumes as well, run:"
echo "  docker-compose down -v"
echo ""