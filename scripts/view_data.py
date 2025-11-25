#!/usr/bin/env python
"""
Simple data viewer for gambling platform data
"""
import json
import sys
from pathlib import Path


def load_data(filename):
    """Load JSONL data file"""
    data = []
    with open(filename) as f:
        for line in f:
            data.append(json.loads(line))
    return data


def show_sample(data, count=5):
    """Show sample records"""
    for i, record in enumerate(data[:count], 1):
        print(f"\nRecord {i}:")
        print(json.dumps(record, indent=2, default=str))


def show_summary(data, name):
    """Show data summary"""
    print(f"\n{name} Summary:")
    print(f"  Total records: {len(data)}")
    if data:
        print(f"  Sample fields: {list(data[0].keys())[:10]}")


def show_bets_analysis(bets):
    """Analyze bets data"""
    print("\n" + "=" * 60)
    print("  Bets Analysis")
    print("=" * 60)

    total = len(bets)
    won = sum(1 for b in bets if b['bet_status'] == 'won')
    lost = sum(1 for b in bets if b['bet_status'] == 'lost')
    pending = sum(1 for b in bets if b['bet_status'] == 'pending')

    total_wagered = sum(float(b['bet_amount']) for b in bets)
    total_payout = sum(float(b['payout_amount']) for b in bets)

    jackpots = [b for b in bets if b['is_jackpot']]

    print(f"\nTotal Bets: {total:,}")
    print(f"  Won: {won:,} ({won/total*100:.1f}%)")
    print(f"  Lost: {lost:,} ({lost/total*100:.1f}%)")
    print(f"  Pending: {pending:,} ({pending/total*100:.1f}%)")

    print(f"\nFinancials:")
    print(f"  Total Wagered: ${total_wagered:,.2f}")
    print(f"  Total Payout: ${total_payout:,.2f}")
    print(f"  House Edge: ${total_wagered - total_payout:,.2f}")

    print(f"\nJackpots: {len(jackpots)}")
    if jackpots:
        for jp in jackpots:
            print(f"  - Bet {jp['bet_id']}: ${float(jp['jackpot_amount']):,.2f}")


def show_players_analysis(players):
    """Analyze players data"""
    print("\n" + "=" * 60)
    print("  Players Analysis")
    print("=" * 60)

    print(f"\nTotal Players: {len(players):,}")

    # VIP tiers
    from collections import Counter
    tiers = Counter(p['vip_tier'] for p in players)
    print(f"\nVIP Tiers:")
    for tier, count in sorted(tiers.items()):
        print(f"  {tier}: {count} ({count/len(players)*100:.1f}%)")

    # Status
    statuses = Counter(p['status'] for p in players)
    print(f"\nStatus:")
    for status, count in sorted(statuses.items()):
        print(f"  {status}: {count}")

    # Countries
    countries = Counter(p['country'] for p in players)
    print(f"\nTop Countries:")
    for country, count in countries.most_common(5):
        print(f"  {country}: {count}")


def show_games_analysis(games):
    """Analyze games data"""
    print("\n" + "=" * 60)
    print("  Games Analysis")
    print("=" * 60)

    print(f"\nTotal Games: {len(games):,}")

    # Game types
    from collections import Counter
    types = Counter(g['game_type'] for g in games)
    print(f"\nGame Types:")
    for game_type, count in sorted(types.items()):
        print(f"  {game_type}: {count}")

    # Providers
    providers = Counter(g['provider'] for g in games)
    print(f"\nTop Providers:")
    for provider, count in providers.most_common(5):
        print(f"  {provider}: {count}")


def main():
    """Main viewer"""
    data_dir = Path("./data")

    if not data_dir.exists():
        print("Error: ./data directory not found")
        print("Run: python main.py  to generate data")
        sys.exit(1)

    print("=" * 60)
    print("  Gambling Platform Data Viewer")
    print("=" * 60)

    # Load all data
    print("\nLoading data...")
    bets = load_data(data_dir / "bets.json")
    players = load_data(data_dir / "players.json")
    games = load_data(data_dir / "games.json")
    sessions = load_data(data_dir / "sessions.json")
    transactions = load_data(data_dir / "transactions.json")
    events = load_data(data_dir / "events.json")

    # Show summaries
    show_summary(players, "Players")
    show_summary(games, "Games")
    show_summary(bets, "Bets")
    show_summary(sessions, "Sessions")
    show_summary(transactions, "Transactions")
    show_summary(events, "Events")

    # Detailed analysis
    show_bets_analysis(bets)
    show_players_analysis(players)
    show_games_analysis(games)

    # Show samples
    print("\n" + "=" * 60)
    print("  Sample Records")
    print("=" * 60)

    print("\n--- Sample Bets ---")
    show_sample(bets, 3)

    print("\n--- Sample Players ---")
    show_sample(players, 2)

    print("\n" + "=" * 60)
    print("\nFor more analysis, run:")
    print("  python scripts/query_with_spark.py")
    print("\nFor interactive queries, run:")
    print("  python scripts/query_with_spark.py -i")
    print("=" * 60)


if __name__ == '__main__':
    main()