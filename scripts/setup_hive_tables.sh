#!/bin/bash

# Setup Hive tables via beeline

echo "=== Setting up Hive Tables ==="
echo ""

# Run SQL script via beeline
docker exec -i hive-server beeline -u jdbc:hive2://localhost:10000 -f /dev/stdin << 'EOF'

CREATE DATABASE IF NOT EXISTS gambling;
USE gambling;

-- Drop existing tables
DROP TABLE IF EXISTS bets;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS games;

-- Create Bets table
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
    win_multiplier DECIMAL(10,2),
    is_jackpot BOOLEAN,
    jackpot_amount DECIMAL(10,2)
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION '/gambling/bets/';

-- Create Players table
CREATE EXTERNAL TABLE players (
    player_id STRING,
    username STRING,
    email STRING,
    country STRING,
    balance DECIMAL(10,2),
    currency STRING,
    status STRING,
    kyc_verified BOOLEAN,
    vip_tier STRING,
    total_wagered DECIMAL(10,2)
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION '/gambling/players/';

-- Create Games table
CREATE EXTERNAL TABLE games (
    game_id STRING,
    game_name STRING,
    game_type STRING,
    provider STRING,
    rtp DECIMAL(5,2),
    volatility STRING,
    min_bet DECIMAL(10,2),
    max_bet DECIMAL(10,2)
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION '/gambling/games/';

-- Show tables
SHOW TABLES;

-- Test query
SELECT COUNT(*) as total_bets FROM bets;

EOF

echo ""
echo "=== Hive Tables Created! ==="
echo ""
echo "Now you can query in Hue at http://localhost:8888"
echo ""
echo "Example queries:"
echo "  SELECT * FROM gambling.bets LIMIT 10;"
echo "  SELECT bet_status, COUNT(*) FROM gambling.bets GROUP BY bet_status;"
echo ""