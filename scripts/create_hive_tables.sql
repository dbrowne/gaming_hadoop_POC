-- Create Hive database and tables for gambling data
-- Run this in Hue or beeline

CREATE DATABASE IF NOT EXISTS gambling;
USE gambling;

-- Drop existing tables if needed
DROP TABLE IF EXISTS bets;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS transactions;

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
    jackpot_amount DECIMAL(10,2),
    bonus_used STRING,
    bet_timestamp TIMESTAMP,
    settled_timestamp TIMESTAMP
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION '/gambling/bets/';

-- Create Players table
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
    total_won DECIMAL(10,2)
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
    max_bet DECIMAL(10,2),
    status STRING,
    reels INT,
    lines INT
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION '/gambling/games/';

-- Create Sessions table
CREATE EXTERNAL TABLE sessions (
    session_id STRING,
    player_id STRING,
    session_start TIMESTAMP,
    session_end TIMESTAMP,
    device_type STRING,
    platform STRING,
    ip_address STRING,
    country STRING,
    starting_balance DECIMAL(10,2),
    ending_balance DECIMAL(10,2),
    total_bets INT,
    total_wagered DECIMAL(10,2),
    total_won DECIMAL(10,2),
    session_status STRING,
    session_duration_seconds INT
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION '/gambling/sessions/';

-- Create Transactions table
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
    fee DECIMAL(10,2),
    transaction_timestamp TIMESTAMP
)
ROW FORMAT SERDE 'org.apache.hive.hcatalog.data.JsonSerDe'
LOCATION '/gambling/transactions/';

-- Verify tables created
SHOW TABLES;

-- Test queries
SELECT COUNT(*) as total_bets FROM bets;
SELECT COUNT(*) as total_players FROM players;
SELECT COUNT(*) as total_games FROM games;