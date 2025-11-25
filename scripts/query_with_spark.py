#!/usr/bin/env python
"""
Query gambling data using Spark (bypasses Hive connection issues)
Works directly with JSON files in HDFS
"""
import os
import sys

# Suppress Spark warnings
os.environ['PYSPARK_PYTHON'] = sys.executable

def create_spark_session():
    """Create a Spark session"""
    try:
        from pyspark.sql import SparkSession

        spark = SparkSession.builder \
            .appName("GamblingDataAnalysis") \
            .master("local[*]") \
            .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
            .getOrCreate()

        # Reduce logging
        spark.sparkContext.setLogLevel("ERROR")

        return spark
    except ImportError:
        print("Error: PySpark not installed")
        print("Install with: pip install pyspark")
        sys.exit(1)


def query_local_data():
    """Query local JSON data files"""
    print("=" * 60)
    print("  Gambling Data Analysis with Spark (Local)")
    print("=" * 60)

    spark = create_spark_session()

    # Read local JSON files
    data_dir = "./data"

    if not os.path.exists(data_dir):
        print(f"Error: {data_dir} directory not found")
        print("Run: python main.py  to generate data")
        sys.exit(1)

    print("\nLoading data files...")

    # Load all datasets
    players = spark.read.json(f"{data_dir}/players.json")
    games = spark.read.json(f"{data_dir}/games.json")
    bets = spark.read.json(f"{data_dir}/bets.json")
    sessions = spark.read.json(f"{data_dir}/sessions.json")
    transactions = spark.read.json(f"{data_dir}/transactions.json")
    events = spark.read.json(f"{data_dir}/events.json")

    # Create temporary views for SQL queries
    players.createOrReplaceTempView("players")
    games.createOrReplaceTempView("games")
    bets.createOrReplaceTempView("bets")
    sessions.createOrReplaceTempView("sessions")
    transactions.createOrReplaceTempView("transactions")
    events.createOrReplaceTempView("events")

    print("✓ Data loaded successfully\n")

    # Run analytics queries
    run_analytics(spark)

    spark.stop()


def run_analytics(spark):
    """Run various analytics queries"""

    print("\n" + "=" * 60)
    print("  Analytics Results")
    print("=" * 60)

    # Query 1: Betting summary
    print("\n1. Betting Summary:")
    print("-" * 60)
    query = """
        SELECT
            bet_status,
            COUNT(*) as count,
            ROUND(SUM(CAST(bet_amount AS DECIMAL(10,2))), 2) as total_wagered,
            ROUND(SUM(CAST(payout_amount AS DECIMAL(10,2))), 2) as total_payout
        FROM bets
        GROUP BY bet_status
        ORDER BY count DESC
    """
    spark.sql(query).show(truncate=False)

    # Query 2: Top 10 players by wagering
    print("\n2. Top 10 Players by Total Wagered:")
    print("-" * 60)
    query = """
        SELECT
            b.player_id,
            p.username,
            p.vip_tier,
            COUNT(*) as total_bets,
            ROUND(SUM(CAST(b.bet_amount AS DECIMAL(10,2))), 2) as total_wagered
        FROM bets b
        JOIN players p ON b.player_id = p.player_id
        GROUP BY b.player_id, p.username, p.vip_tier
        ORDER BY total_wagered DESC
        LIMIT 10
    """
    spark.sql(query).show(truncate=False)

    # Query 3: Game performance
    print("\n3. Top Games by Revenue:")
    print("-" * 60)
    query = """
        SELECT
            g.game_name,
            g.game_type,
            COUNT(*) as plays,
            ROUND(SUM(CAST(b.bet_amount AS DECIMAL(10,2))), 2) as wagered,
            ROUND(SUM(CAST(b.payout_amount AS DECIMAL(10,2))), 2) as paid_out,
            ROUND(SUM(CAST(b.bet_amount AS DECIMAL(10,2))) -
                  SUM(CAST(b.payout_amount AS DECIMAL(10,2))), 2) as revenue
        FROM bets b
        JOIN games g ON b.game_id = g.game_id
        GROUP BY g.game_name, g.game_type
        ORDER BY revenue DESC
        LIMIT 10
    """
    spark.sql(query).show(truncate=False)

    # Query 4: VIP tier analysis
    print("\n4. Player Analysis by VIP Tier:")
    print("-" * 60)
    query = """
        SELECT
            p.vip_tier,
            COUNT(DISTINCT p.player_id) as player_count,
            COUNT(b.bet_id) as total_bets,
            ROUND(AVG(CAST(b.bet_amount AS DECIMAL(10,2))), 2) as avg_bet,
            ROUND(SUM(CAST(b.bet_amount AS DECIMAL(10,2))), 2) as total_wagered
        FROM players p
        LEFT JOIN bets b ON p.player_id = b.player_id
        GROUP BY p.vip_tier
        ORDER BY
            CASE p.vip_tier
                WHEN 'platinum' THEN 1
                WHEN 'gold' THEN 2
                WHEN 'silver' THEN 3
                WHEN 'basic' THEN 4
            END
    """
    spark.sql(query).show(truncate=False)

    # Query 5: Device/Platform usage
    print("\n5. Session Analysis by Device:")
    print("-" * 60)
    query = """
        SELECT
            device_type,
            platform,
            COUNT(*) as session_count,
            ROUND(AVG(total_bets), 2) as avg_bets_per_session,
            ROUND(AVG(CAST(total_wagered AS DECIMAL(10,2))), 2) as avg_wagered
        FROM sessions
        WHERE session_status = 'ended'
        GROUP BY device_type, platform
        ORDER BY session_count DESC
    """
    spark.sql(query).show(truncate=False)

    # Query 6: Jackpot wins
    print("\n6. Jackpot Wins:")
    print("-" * 60)
    query = """
        SELECT
            b.bet_id,
            b.player_id,
            p.username,
            g.game_name,
            ROUND(CAST(b.bet_amount AS DECIMAL(10,2)), 2) as bet_amount,
            ROUND(CAST(b.jackpot_amount AS DECIMAL(10,2)), 2) as jackpot_won,
            b.bet_timestamp
        FROM bets b
        JOIN players p ON b.player_id = p.player_id
        JOIN games g ON b.game_id = g.game_id
        WHERE b.is_jackpot = true
        ORDER BY jackpot_won DESC
    """
    result = spark.sql(query)
    if result.count() > 0:
        result.show(truncate=False)
    else:
        print("No jackpot wins in this dataset")

    # Query 7: Transaction summary
    print("\n7. Transaction Summary:")
    print("-" * 60)
    query = """
        SELECT
            transaction_type,
            status,
            COUNT(*) as count,
            ROUND(SUM(CAST(amount AS DECIMAL(10,2))), 2) as total_amount
        FROM transactions
        GROUP BY transaction_type, status
        ORDER BY transaction_type, count DESC
    """
    spark.sql(query).show(truncate=False)


def interactive_query_mode():
    """Interactive mode for custom queries"""
    print("\n" + "=" * 60)
    print("  Interactive Query Mode")
    print("=" * 60)
    print("\nAvailable tables: players, games, bets, sessions, transactions, events")
    print("Type 'exit' to quit\n")

    spark = create_spark_session()

    # Load data
    data_dir = "./data"
    spark.read.json(f"{data_dir}/players.json").createOrReplaceTempView("players")
    spark.read.json(f"{data_dir}/games.json").createOrReplaceTempView("games")
    spark.read.json(f"{data_dir}/bets.json").createOrReplaceTempView("bets")
    spark.read.json(f"{data_dir}/sessions.json").createOrReplaceTempView("sessions")
    spark.read.json(f"{data_dir}/transactions.json").createOrReplaceTempView("transactions")
    spark.read.json(f"{data_dir}/events.json").createOrReplaceTempView("events")

    while True:
        try:
            query = input("\nSQL> ").strip()

            if query.lower() in ['exit', 'quit', 'q']:
                break

            if not query:
                continue

            result = spark.sql(query)
            result.show(truncate=False)

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

    spark.stop()


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description='Query gambling data with Spark')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Start interactive query mode')
    args = parser.parse_args()

    if args.interactive:
        interactive_query_mode()
    else:
        query_local_data()


if __name__ == '__main__':
    main()