#!/usr/bin/env python
"""
Simple Hive query interface using beeline
"""
import subprocess
import sys

def run_hive_query(query):
    """Run a Hive query via beeline"""
    cmd = [
        'docker', 'exec', '-i', 'hive-server',
        'beeline', '-u', 'jdbc:hive2://localhost:10000',
        '-e', query
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr

def main():
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        # Default queries
        queries = [
            "USE gambling",
            "SHOW TABLES",
            "SELECT COUNT(*) as total_bets FROM bets",
            "SELECT bet_status, COUNT(*) as count FROM bets GROUP BY bet_status",
            "SELECT COUNT(*) as total_players FROM players",
            "SELECT vip_tier, COUNT(*) as count FROM players GROUP BY vip_tier",
        ]

        print("=" * 60)
        print("  Gambling Platform - Hive Query Results")
        print("=" * 60)

        for query in queries:
            print(f"\n>>> {query}")
            stdout, stderr = run_hive_query(query)

            # Print only the relevant output (skip warnings)
            for line in stdout.split('\n'):
                if line and not line.startswith('SLF4J') and not line.startswith('Connecting') and not line.startswith('Connected'):
                    print(line)

        print("\n" + "=" * 60)
        print("\nTo run custom queries:")
        print("  python scripts/query_hive.py 'SELECT * FROM bets LIMIT 10'")
        print("=" * 60)
        return

    # Run custom query
    stdout, stderr = run_hive_query(query)
    print(stdout)
    if stderr and 'Error' in stderr:
        print("STDERR:", stderr, file=sys.stderr)

if __name__ == '__main__':
    main()
