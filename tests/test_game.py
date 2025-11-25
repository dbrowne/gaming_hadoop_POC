"""
Test cases for Game model
"""
import pytest
from datetime import datetime
from decimal import Decimal
from models.game import Game


class TestGame:
    """Test Game model"""

    def test_game_creation_with_required_fields(self):
        """Test creating a game with only required fields"""
        game = Game(
            game_id="G001",
            game_name="Test Slot",
            game_type="slot",
            provider="TestProvider",
            rtp=Decimal('96.5'),
            volatility="medium",
            min_bet=Decimal('0.10'),
            max_bet=Decimal('100.00')
        )

        assert game.game_id == "G001"
        assert game.game_name == "Test Slot"
        assert game.game_type == "slot"
        assert game.provider == "TestProvider"
        assert game.rtp == Decimal('96.5')
        assert game.volatility == "medium"
        assert game.min_bet == Decimal('0.10')
        assert game.max_bet == Decimal('100.00')
        assert game.currency == 'USD'
        assert game.status == 'active'

    def test_game_types(self):
        """Test different game types"""
        game_types = ['slot', 'poker', 'roulette', 'blackjack', 'sports_betting', 'live_dealer']

        for game_type in game_types:
            game = Game(
                game_id=f"G_{game_type}",
                game_name=f"Test {game_type}",
                game_type=game_type,
                provider="Provider",
                rtp=Decimal('96.0'),
                volatility="medium",
                min_bet=Decimal('1.00'),
                max_bet=Decimal('100.00')
            )
            assert game.game_type == game_type

    def test_game_volatility_levels(self):
        """Test different volatility levels"""
        volatilities = ['low', 'medium', 'high']

        for volatility in volatilities:
            game = Game(
                game_id=f"G_vol_{volatility}",
                game_name=f"{volatility} Volatility Game",
                game_type="slot",
                provider="Provider",
                rtp=Decimal('95.0'),
                volatility=volatility,
                min_bet=Decimal('1.00'),
                max_bet=Decimal('100.00')
            )
            assert game.volatility == volatility

    def test_game_status_values(self):
        """Test different game status values"""
        statuses = ['active', 'inactive', 'maintenance']

        for status in statuses:
            game = Game(
                game_id=f"G_status_{status}",
                game_name=f"{status} Game",
                game_type="slot",
                provider="Provider",
                rtp=Decimal('96.0'),
                volatility="medium",
                min_bet=Decimal('1.00'),
                max_bet=Decimal('100.00'),
                status=status
            )
            assert game.status == status

    def test_game_with_slot_specific_fields(self):
        """Test game with slot-specific fields (reels and lines)"""
        game = Game(
            game_id="G002",
            game_name="5-Reel Slot",
            game_type="slot",
            provider="NetEnt",
            rtp=Decimal('96.5'),
            volatility="high",
            min_bet=Decimal('0.20'),
            max_bet=Decimal('200.00'),
            reels=5,
            lines=20
        )

        assert game.reels == 5
        assert game.lines == 20

    def test_game_with_features(self):
        """Test game with features dictionary"""
        features = {
            'bonus_rounds': True,
            'multipliers': True,
            'free_spins': 10,
            'wild_symbols': True
        }

        game = Game(
            game_id="G003",
            game_name="Feature Rich Slot",
            game_type="slot",
            provider="Microgaming",
            rtp=Decimal('97.0'),
            volatility="medium",
            min_bet=Decimal('0.10'),
            max_bet=Decimal('100.00'),
            features=features
        )

        assert game.features == features
        assert game.features['bonus_rounds'] is True
        assert game.features['free_spins'] == 10

    def test_game_with_tags(self):
        """Test game with tags"""
        tags = ['popular', 'new', 'jackpot']

        game = Game(
            game_id="G004",
            game_name="Tagged Game",
            game_type="slot",
            provider="Playtech",
            rtp=Decimal('96.0'),
            volatility="high",
            min_bet=Decimal('1.00'),
            max_bet=Decimal('500.00'),
            tags=tags
        )

        assert game.tags == tags
        assert 'popular' in game.tags
        assert len(game.tags) == 3

    def test_game_with_max_win(self):
        """Test game with max_win specified"""
        game = Game(
            game_id="G005",
            game_name="Big Win Slot",
            game_type="slot",
            provider="Provider",
            rtp=Decimal('96.0'),
            volatility="high",
            min_bet=Decimal('0.10'),
            max_bet=Decimal('100.00'),
            max_win=Decimal('50000.00')
        )

        assert game.max_win == Decimal('50000.00')

    def test_game_rtp_precision(self):
        """Test RTP percentage precision"""
        rtps = [Decimal('94.50'), Decimal('96.00'), Decimal('97.25'), Decimal('98.99')]

        for rtp in rtps:
            game = Game(
                game_id=f"G_rtp_{rtp}",
                game_name="RTP Test Game",
                game_type="slot",
                provider="Provider",
                rtp=rtp,
                volatility="medium",
                min_bet=Decimal('1.00'),
                max_bet=Decimal('100.00')
            )
            assert game.rtp == rtp

    def test_game_betting_limits(self):
        """Test various betting limits"""
        game = Game(
            game_id="G006",
            game_name="VIP Slot",
            game_type="slot",
            provider="Evolution",
            rtp=Decimal('96.5'),
            volatility="low",
            min_bet=Decimal('10.00'),
            max_bet=Decimal('5000.00')
        )

        assert game.min_bet == Decimal('10.00')
        assert game.max_bet == Decimal('5000.00')
        assert game.max_bet > game.min_bet

    def test_game_statistics_defaults(self):
        """Test that game statistics default to zero"""
        game = Game(
            game_id="G007",
            game_name="New Game",
            game_type="poker",
            provider="Provider",
            rtp=Decimal('96.0'),
            volatility="medium",
            min_bet=Decimal('1.00'),
            max_bet=Decimal('100.00')
        )

        assert game.total_plays == 0
        assert game.total_wagered == Decimal('0.00')
        assert game.total_paid == Decimal('0.00')

    def test_game_to_dict(self):
        """Test game serialization to dictionary"""
        game = Game(
            game_id="G008",
            game_name="Dict Test Slot",
            game_type="slot",
            provider="NetEnt",
            rtp=Decimal('96.50'),
            volatility="high",
            min_bet=Decimal('0.20'),
            max_bet=Decimal('100.00'),
            reels=5,
            lines=25,
            tags=['popular', 'jackpot'],
            release_date=datetime(2025, 1, 1)
        )

        game_dict = game.to_dict()

        assert isinstance(game_dict, dict)
        assert game_dict['game_id'] == "G008"
        assert game_dict['game_name'] == "Dict Test Slot"
        assert game_dict['game_type'] == "slot"
        assert game_dict['provider'] == "NetEnt"
        assert game_dict['rtp'] == '96.50'
        assert game_dict['volatility'] == "high"
        assert game_dict['min_bet'] == '0.20'
        assert game_dict['max_bet'] == '100.00'
        assert game_dict['reels'] == 5
        assert game_dict['lines'] == 25
        assert game_dict['tags'] == ['popular', 'jackpot']
        assert isinstance(game_dict['created_at'], str)

    def test_game_to_dict_with_optional_fields_none(self):
        """Test serialization with optional fields as None"""
        game = Game(
            game_id="G009",
            game_name="Minimal Game",
            game_type="roulette",
            provider="Provider",
            rtp=Decimal('97.0'),
            volatility="low",
            min_bet=Decimal('1.00'),
            max_bet=Decimal('1000.00')
        )

        game_dict = game.to_dict()

        assert game_dict['features'] is None
        assert game_dict['max_win'] is None
        assert game_dict['lines'] is None
        assert game_dict['reels'] is None
        assert game_dict['tags'] is None
        assert game_dict['release_date'] is None

    def test_game_providers(self):
        """Test different game providers"""
        providers = ['NetEnt', 'Microgaming', 'Playtech', 'Evolution', 'Pragmatic Play']

        for provider in providers:
            game = Game(
                game_id=f"G_{provider.replace(' ', '_')}",
                game_name=f"{provider} Game",
                game_type="slot",
                provider=provider,
                rtp=Decimal('96.0'),
                volatility="medium",
                min_bet=Decimal('1.00'),
                max_bet=Decimal('100.00')
            )
            assert game.provider == provider

    def test_game_with_statistics(self):
        """Test game with updated statistics"""
        game = Game(
            game_id="G010",
            game_name="Popular Game",
            game_type="slot",
            provider="Provider",
            rtp=Decimal('96.0'),
            volatility="medium",
            min_bet=Decimal('1.00'),
            max_bet=Decimal('100.00'),
            total_plays=10000,
            total_wagered=Decimal('250000.00'),
            total_paid=Decimal('240000.00')
        )

        assert game.total_plays == 10000
        assert game.total_wagered == Decimal('250000.00')
        assert game.total_paid == Decimal('240000.00')