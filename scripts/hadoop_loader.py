"""
Hadoop Data Loader for Gaming Platform
Loads Python data models into HDFS and creates Hive tables
"""
import json
import sys
import os
from datetime import datetime
from decimal import Decimal

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Player, Game, Bet, Session, Transaction, Event


class HadoopLoader:
    """Load gaming data into Hadoop/HDFS"""

    def __init__(self, hdfs_url='http://localhost:9870', hdfs_user='root'):
        """
        Initialize Hadoop loader

        Args:
            hdfs_url: URL to HDFS WebHDFS interface
            hdfs_user: HDFS user
        """
        self.hdfs_url = hdfs_url
        self.hdfs_user = hdfs_user
        try:
            from hdfs import InsecureClient
            self.client = InsecureClient(hdfs_url, user=hdfs_user)
        except ImportError:
            print("Warning: hdfs library not installed. Install with: pip install hdfs")
            self.client = None

    def save_to_json(self, data_list, filename):
        """
        Save data models to JSON file

        Args:
            data_list: List of data model instances
            filename: Output filename
        """
        json_data = [item.to_dict() for item in data_list]

        with open(filename, 'w') as f:
            for record in json_data:
                f.write(json.dumps(record, default=str) + '\n')

        print(f"Saved {len(json_data)} records to {filename}")
        return filename

    def upload_to_hdfs(self, local_path, hdfs_path):
        """
        Upload local file to HDFS

        Args:
            local_path: Local file path
            hdfs_path: HDFS destination path
        """
        if not self.client:
            print(f"HDFS client not available. File saved locally at: {local_path}")
            print(f"Upload manually with: hdfs dfs -put {local_path} {hdfs_path}")
            return

        try:
            # Create parent directory if it doesn't exist
            parent_dir = '/'.join(hdfs_path.split('/')[:-1])
            try:
                self.client.makedirs(parent_dir)
            except:
                pass  # Directory might already exist

            # Upload file
            self.client.upload(hdfs_path, local_path, overwrite=True)
            print(f"Uploaded {local_path} to HDFS: {hdfs_path}")

        except Exception as e:
            print(f"Error uploading to HDFS: {e}")
            print(f"File saved locally at: {local_path}")

    def generate_sample_players(self, count=100):
        """Generate sample player data"""
        from random import choice, randint, uniform
        from datetime import timedelta

        players = []
        countries = ['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'ES', 'IT']
        statuses = ['active', 'suspended', 'closed']
        tiers = ['basic', 'silver', 'gold', 'platinum']

        for i in range(1, count + 1):
            player = Player(
                player_id=f"P{i:06d}",
                username=f"player_{i}",
                email=f"player{i}@example.com",
                registration_date=datetime.now() - timedelta(days=randint(1, 365)),
                country=choice(countries),
                balance=Decimal(str(round(uniform(0, 10000), 2))),
                currency='USD',
                status=choice(statuses),
                kyc_verified=choice([True, False]),
                vip_tier=choice(tiers),
                total_deposits=Decimal(str(round(uniform(100, 50000), 2))),
                total_withdrawals=Decimal(str(round(uniform(0, 30000), 2))),
                total_wagered=Decimal(str(round(uniform(1000, 100000), 2))),
                total_won=Decimal(str(round(uniform(500, 80000), 2)))
            )
            players.append(player)

        return players

    def generate_sample_games(self, count=50):
        """Generate sample game data"""
        from random import choice, uniform

        games = []
        game_types = ['slot', 'poker', 'roulette', 'blackjack', 'baccarat']
        providers = ['NetEnt', 'Microgaming', 'Playtech', 'Evolution', 'Pragmatic Play']
        volatilities = ['low', 'medium', 'high']

        for i in range(1, count + 1):
            game = Game(
                game_id=f"G{i:04d}",
                game_name=f"Game {i}",
                game_type=choice(game_types),
                provider=choice(providers),
                rtp=Decimal(str(round(uniform(94, 98), 2))),
                volatility=choice(volatilities),
                min_bet=Decimal(str(round(uniform(0.1, 1), 2))),
                max_bet=Decimal(str(round(uniform(100, 1000), 2))),
                tags=['popular', 'new'] if i % 3 == 0 else ['classic']
            )
            games.append(game)

        return games

    def generate_sample_bets(self, count=1000):
        """Generate sample bet data"""
        from random import choice, randint, uniform

        bets = []
        bet_types = ['standard', 'bonus', 'free_spin']
        bet_statuses = ['won', 'lost', 'pending']

        for i in range(1, count + 1):
            bet_amount = Decimal(str(round(uniform(1, 100), 2)))
            status = choice(bet_statuses)

            if status == 'won':
                payout = bet_amount * Decimal(str(round(uniform(1.5, 10), 2)))
                multiplier = payout / bet_amount
            else:
                payout = Decimal('0.00')
                multiplier = None

            bet = Bet(
                bet_id=f"B{i:08d}",
                player_id=f"P{randint(1, 100):06d}",
                game_id=f"G{randint(1, 50):04d}",
                session_id=f"S{randint(1, 500):06d}",
                bet_amount=bet_amount,
                bet_type=choice(bet_types),
                bet_status=status,
                payout_amount=payout,
                win_multiplier=multiplier
            )
            bets.append(bet)

        return bets

    def load_all_sample_data(self, output_dir='./data'):
        """Generate and load all sample data"""
        os.makedirs(output_dir, exist_ok=True)

        print("Generating sample data...")

        # Generate data
        players = self.generate_sample_players(100)
        games = self.generate_sample_games(50)
        bets = self.generate_sample_bets(1000)

        # Save to JSON
        player_file = self.save_to_json(players, f"{output_dir}/players.json")
        game_file = self.save_to_json(games, f"{output_dir}/games.json")
        bet_file = self.save_to_json(bets, f"{output_dir}/bets.json")

        # Upload to HDFS
        if self.client:
            print("\nUploading to HDFS...")
            self.upload_to_hdfs(player_file, '/gambling/players/players.json')
            self.upload_to_hdfs(game_file, '/gambling/games/games.json')
            self.upload_to_hdfs(bet_file, '/gambling/bets/bets.json')

        print("\nData generation complete!")
        print(f"Players: {len(players)}")
        print(f"Games: {len(games)}")
        print(f"Bets: {len(bets)}")


def main():
    """Main function"""
    print("=== Hadoop Gaming Data Loader ===\n")

    loader = HadoopLoader()
    loader.load_all_sample_data()


if __name__ == '__main__':
    main()