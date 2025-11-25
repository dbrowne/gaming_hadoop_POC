"""
Online Gambling Platform - Hadoop POC
Generate and persist random gambling data to Hadoop
"""
import os
import json
import random
from datetime import datetime, timedelta
from decimal import Decimal
from models import Player, Game, Bet, Session, Transaction, Event


class GamblingDataGenerator:
    """Generate realistic gambling platform data"""

    def __init__(self, num_players=200, num_games=100, num_sessions=1000, num_bets=5000):
        self.num_players = num_players
        self.num_games = num_games
        self.num_sessions = num_sessions
        self.num_bets = num_bets

        # Reference data
        self.countries = ['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'ES', 'IT', 'NL', 'SE']
        self.currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD']
        self.game_types = ['slot', 'poker', 'roulette', 'blackjack', 'baccarat', 'live_dealer']
        self.providers = ['NetEnt', 'Microgaming', 'Playtech', 'Evolution', 'Pragmatic Play', 'Red Tiger']
        self.device_types = ['desktop', 'mobile', 'tablet']
        self.platforms = ['web', 'ios', 'android']
        self.payment_methods = ['credit_card', 'bank_transfer', 'ewallet', 'crypto', 'debit_card']

        # Generated data storage
        self.players = []
        self.games = []
        self.sessions = []
        self.bets = []
        self.transactions = []
        self.events = []

    def generate_all_data(self):
        """Generate all gambling data"""
        print("=== Generating Gambling Platform Data ===\n")

        print(f"Generating {self.num_players} players...")
        self.players = self.generate_players()

        print(f"Generating {self.num_games} games...")
        self.games = self.generate_games()

        print(f"Generating {self.num_sessions} sessions...")
        self.sessions = self.generate_sessions()

        print(f"Generating {self.num_bets} bets...")
        self.bets = self.generate_bets()

        print(f"Generating transactions...")
        self.transactions = self.generate_transactions()

        print(f"Generating events...")
        self.events = self.generate_events()

        print("\n=== Data Generation Complete ===\n")
        self.print_statistics()

    def generate_players(self):
        """Generate random players"""
        players = []
        base_date = datetime.now() - timedelta(days=365)

        for i in range(1, self.num_players + 1):
            country = random.choice(self.countries)
            currency = 'USD' if country == 'US' else random.choice(self.currencies)
            registration_date = base_date + timedelta(days=random.randint(0, 365))

            player = Player(
                player_id=f"P{i:06d}",
                username=f"player_{i}",
                email=f"player{i}@example.com",
                registration_date=registration_date,
                country=country,
                balance=Decimal(str(round(random.uniform(0, 10000), 2))),
                currency=currency,
                status=random.choices(
                    ['active', 'suspended', 'closed'],
                    weights=[85, 10, 5]
                )[0],
                kyc_verified=random.random() > 0.3,
                vip_tier=random.choices(
                    ['basic', 'silver', 'gold', 'platinum'],
                    weights=[60, 25, 12, 3]
                )[0],
                total_deposits=Decimal(str(round(random.uniform(100, 50000), 2))),
                total_withdrawals=Decimal(str(round(random.uniform(0, 30000), 2))),
                total_wagered=Decimal(str(round(random.uniform(1000, 100000), 2))),
                total_won=Decimal(str(round(random.uniform(500, 80000), 2)))
            )
            players.append(player)

        return players

    def generate_games(self):
        """Generate random games"""
        games = []

        game_names = [
            "Mega Fortune", "Book of Dead", "Starburst", "Gonzo's Quest", "Mega Moolah",
            "Lightning Roulette", "Blackjack Supreme", "Texas Hold'em", "Dragon Tiger",
            "Baccarat Evolution", "Dream Catcher", "Sweet Bonanza", "Wolf Gold", "Dead or Alive"
        ]

        for i in range(1, self.num_games + 1):
            game_type = random.choice(self.game_types)
            game_name = f"{random.choice(game_names)} {i}" if i <= len(game_names) else f"Game {i}"

            game = Game(
                game_id=f"G{i:04d}",
                game_name=game_name,
                game_type=game_type,
                provider=random.choice(self.providers),
                rtp=Decimal(str(round(random.uniform(94.0, 98.5), 2))),
                volatility=random.choice(['low', 'medium', 'high']),
                min_bet=Decimal(str(round(random.uniform(0.1, 5.0), 2))),
                max_bet=Decimal(str(round(random.uniform(50, 1000), 2))),
                status=random.choices(['active', 'inactive'], weights=[90, 10])[0],
                reels=random.choice([3, 5, 6]) if game_type == 'slot' else None,
                lines=random.choice([10, 20, 25, 30]) if game_type == 'slot' else None,
                tags=['popular'] if random.random() > 0.7 else []
            )
            games.append(game)

        return games

    def generate_sessions(self):
        """Generate random gaming sessions"""
        sessions = []
        base_date = datetime.now() - timedelta(days=90)

        for i in range(1, self.num_sessions + 1):
            player = random.choice(self.players)
            start_time = base_date + timedelta(
                days=random.randint(0, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            duration_seconds = random.randint(60, 7200)
            is_ended = random.random() > 0.2

            starting_balance = Decimal(str(round(random.uniform(50, 5000), 2)))
            total_wagered = Decimal(str(round(random.uniform(10, 1000), 2)))
            total_won = Decimal(str(round(random.uniform(0, float(total_wagered) * 1.5), 2)))

            session = Session(
                session_id=f"S{i:06d}",
                player_id=player.player_id,
                session_start=start_time,
                session_end=start_time + timedelta(seconds=duration_seconds) if is_ended else None,
                device_type=random.choice(self.device_types),
                platform=random.choice(self.platforms),
                ip_address=f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                country=player.country,
                starting_balance=starting_balance,
                ending_balance=starting_balance + total_won - total_wagered if is_ended else None,
                total_bets=random.randint(5, 200) if is_ended else random.randint(1, 50),
                total_wagered=total_wagered if is_ended else Decimal('0.00'),
                total_won=total_won if is_ended else Decimal('0.00'),
                total_lost=total_wagered - total_won if is_ended else Decimal('0.00'),
                games_played=random.randint(1, 10),
                session_status='ended' if is_ended else 'active',
                session_duration_seconds=duration_seconds if is_ended else None
            )
            sessions.append(session)

        return sessions

    def generate_bets(self):
        """Generate random bets"""
        bets = []
        base_date = datetime.now() - timedelta(days=90)

        for i in range(1, self.num_bets + 1):
            session = random.choice(self.sessions)
            game = random.choice(self.games)
            player = next((p for p in self.players if p.player_id == session.player_id), self.players[0])

            bet_amount = Decimal(str(round(random.uniform(
                float(game.min_bet),
                min(float(game.max_bet), 100)
            ), 2)))

            # Determine if bet wins (roughly 45% win rate)
            is_won = random.random() < 0.45
            bet_status = 'won' if is_won else 'lost'

            if is_won:
                multiplier = Decimal(str(round(random.uniform(1.2, 10.0), 2)))
                payout = bet_amount * multiplier
                # Rare jackpot (0.1% chance)
                is_jackpot = random.random() < 0.001
                if is_jackpot:
                    payout = Decimal(str(round(random.uniform(10000, 100000), 2)))
                    multiplier = payout / bet_amount
            else:
                payout = Decimal('0.00')
                multiplier = None
                is_jackpot = False

            bet_time = session.session_start + timedelta(seconds=random.randint(0, 3600))

            bet = Bet(
                bet_id=f"B{i:08d}",
                player_id=player.player_id,
                game_id=game.game_id,
                session_id=session.session_id,
                bet_amount=bet_amount,
                currency=player.currency,
                bet_type=random.choices(
                    ['standard', 'bonus', 'free_spin'],
                    weights=[85, 10, 5]
                )[0],
                bet_status=bet_status,
                payout_amount=payout,
                win_multiplier=multiplier,
                is_jackpot=is_jackpot,
                jackpot_amount=payout if is_jackpot else None,
                bet_timestamp=bet_time,
                settled_timestamp=bet_time + timedelta(seconds=random.randint(1, 10))
            )
            bets.append(bet)

        return bets

    def generate_transactions(self):
        """Generate random transactions"""
        transactions = []
        tx_id = 1

        # Generate deposit transactions for each player
        for player in self.players:
            num_deposits = random.randint(1, 5)
            for _ in range(num_deposits):
                amount = Decimal(str(round(random.uniform(50, 2000), 2)))
                transaction = Transaction(
                    transaction_id=f"T{tx_id:08d}",
                    player_id=player.player_id,
                    transaction_type="deposit",
                    amount=amount,
                    currency=player.currency,
                    status=random.choices(['completed', 'failed'], weights=[95, 5])[0],
                    payment_method=random.choice(self.payment_methods),
                    payment_provider=random.choice(['Stripe', 'PayPal', 'Adyen', 'Coinbase']),
                    balance_before=Decimal(str(round(random.uniform(0, 1000), 2))),
                    balance_after=Decimal(str(round(random.uniform(1000, 3000), 2)))
                )
                transactions.append(transaction)
                tx_id += 1

        # Generate some withdrawal transactions
        num_withdrawals = self.num_players // 3
        for _ in range(num_withdrawals):
            player = random.choice(self.players)
            amount = Decimal(str(round(random.uniform(100, 5000), 2)))
            fee = Decimal(str(round(float(amount) * 0.02, 2)))

            transaction = Transaction(
                transaction_id=f"T{tx_id:08d}",
                player_id=player.player_id,
                transaction_type="withdrawal",
                amount=amount,
                currency=player.currency,
                status=random.choices(['completed', 'processing', 'failed'], weights=[80, 15, 5])[0],
                payment_method=random.choice(self.payment_methods),
                fee=fee,
                net_amount=amount - fee,
                balance_before=Decimal(str(round(random.uniform(1000, 10000), 2))),
                balance_after=Decimal(str(round(random.uniform(100, 5000), 2)))
            )
            transactions.append(transaction)
            tx_id += 1

        return transactions

    def generate_events(self):
        """Generate random events"""
        events = []
        event_id = 1

        # Login events for sessions
        for session in self.sessions[:500]:  # First 500 sessions
            event = Event(
                event_id=f"E{event_id:08d}",
                event_type="login",
                event_category="player",
                player_id=session.player_id,
                session_id=session.session_id,
                severity="info",
                ip_address=session.ip_address,
                device_type=session.device_type,
                country=session.country
            )
            events.append(event)
            event_id += 1

        # Bet placed events for sample of bets
        for bet in random.sample(self.bets, min(1000, len(self.bets))):
            event = Event(
                event_id=f"E{event_id:08d}",
                event_type="bet_placed",
                event_category="game",
                player_id=bet.player_id,
                session_id=bet.session_id,
                game_id=bet.game_id,
                bet_id=bet.bet_id,
                severity="info",
                event_data={'amount': str(bet.bet_amount), 'status': bet.bet_status}
            )
            events.append(event)
            event_id += 1

        # Transaction events
        for transaction in self.transactions[:200]:
            event = Event(
                event_id=f"E{event_id:08d}",
                event_type=f"transaction_{transaction.transaction_type}",
                event_category="transaction",
                player_id=transaction.player_id,
                transaction_id=transaction.transaction_id,
                severity="info",
                event_data={'amount': str(transaction.amount), 'status': transaction.status}
            )
            events.append(event)
            event_id += 1

        return events

    def print_statistics(self):
        """Print statistics about generated data"""
        print("Statistics:")
        print(f"  Players: {len(self.players)}")
        print(f"  Games: {len(self.games)}")
        print(f"  Sessions: {len(self.sessions)}")
        print(f"  Bets: {len(self.bets)}")
        print(f"  Transactions: {len(self.transactions)}")
        print(f"  Events: {len(self.events)}")

        # Calculate some analytics
        total_wagered = sum(bet.bet_amount for bet in self.bets)
        total_payout = sum(bet.payout_amount for bet in self.bets)
        house_edge = total_wagered - total_payout
        jackpots = sum(1 for bet in self.bets if bet.is_jackpot)

        print(f"\nBetting Analytics:")
        print(f"  Total Wagered: ${total_wagered:,.2f}")
        print(f"  Total Payout: ${total_payout:,.2f}")
        print(f"  House Revenue: ${house_edge:,.2f}")
        print(f"  Jackpot Wins: {jackpots}")

    def save_to_json(self, output_dir='./data'):
        """Save all data to JSON files"""
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n=== Saving Data to {output_dir} ===\n")

        datasets = {
            'players': self.players,
            'games': self.games,
            'sessions': self.sessions,
            'bets': self.bets,
            'transactions': self.transactions,
            'events': self.events
        }

        for name, data in datasets.items():
            filename = f"{output_dir}/{name}.json"
            with open(filename, 'w') as f:
                for item in data:
                    f.write(json.dumps(item.to_dict(), default=str) + '\n')
            print(f"  Saved {len(data):,} records to {filename}")

        print("\n=== Data Saved Successfully ===\n")

    def upload_to_hdfs(self, output_dir='./data'):
        """Attempt to upload data to HDFS"""
        try:
            from hdfs import InsecureClient
            client = InsecureClient('http://localhost:9870', user='root')

            print("\n=== Uploading Data to HDFS ===\n")

            datasets = ['players', 'games', 'sessions', 'bets', 'transactions', 'events']

            for dataset in datasets:
                local_path = f"{output_dir}/{dataset}.json"
                hdfs_path = f"/gambling/{dataset}/{dataset}.json"

                # Create directory if needed
                try:
                    client.makedirs(f"/gambling/{dataset}")
                except:
                    pass

                # Upload file
                client.upload(hdfs_path, local_path, overwrite=True)
                print(f"  Uploaded {dataset}.json to HDFS: {hdfs_path}")

            print("\n=== Data Uploaded to HDFS Successfully ===\n")

        except ImportError:
            print("\n=== HDFS Upload Skipped ===")
            print("  Install hdfs library with: pip install hdfs")
            print("  Or upload manually with:")
            for dataset in ['players', 'games', 'sessions', 'bets', 'transactions', 'events']:
                print(f"    docker exec namenode hdfs dfs -put {output_dir}/{dataset}.json /gambling/{dataset}/")
            print()

        except Exception as e:
            print(f"\n=== HDFS Upload Failed ===")
            print(f"  Error: {e}")
            print(f"  Make sure Hadoop cluster is running: ./scripts/start_hadoop.sh")
            print(f"  Or upload manually with:")
            for dataset in ['players', 'games', 'sessions', 'bets', 'transactions', 'events']:
                print(f"    docker exec namenode hdfs dfs -put {output_dir}/{dataset}.json /gambling/{dataset}/")
            print()


def main():
    """Main function to generate and persist gambling data"""
    print("\n" + "=" * 60)
    print("  Online Gambling Platform - Hadoop POC")
    print("  Generating Random Gambling Data")
    print("=" * 60 + "\n")

    # Create generator with desired quantities
    generator = GamblingDataGenerator(
        num_players=200,
        num_games=100,
        num_sessions=1000,
        num_bets=5000
    )

    # Generate all data
    generator.generate_all_data()

    # Save to local JSON files
    generator.save_to_json()

    # Try to upload to HDFS
    generator.upload_to_hdfs()

    print("=" * 60)
    print("  Data generation and persistence complete!")
    print("=" * 60 + "\n")

    print("Next steps:")
    print("  1. Start Hadoop cluster: ./scripts/start_hadoop.sh")
    print("  2. View data in Hue: http://localhost:8888")
    print("  3. Run analytics queries (see HADOOP_SETUP.md)")
    print("  4. Process with Spark for advanced analytics")
    print()


if __name__ == '__main__':
    main()