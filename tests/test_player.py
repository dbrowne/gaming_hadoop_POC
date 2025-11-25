"""
Test cases for Player model
"""
import pytest
from datetime import datetime
from decimal import Decimal
from models.player import Player


class TestPlayer:
    """Test Player model"""

    def test_player_creation_with_required_fields(self):
        """Test creating a player with only required fields"""
        player = Player(
            player_id="P001",
            username="test_player",
            email="test@example.com",
            registration_date=datetime(2025, 1, 1),
            country="US"
        )

        assert player.player_id == "P001"
        assert player.username == "test_player"
        assert player.email == "test@example.com"
        assert player.country == "US"
        assert player.balance == Decimal('0.00')
        assert player.currency == 'USD'
        assert player.status == 'active'
        assert player.kyc_verified is False
        assert player.vip_tier == 'basic'

    def test_player_creation_with_all_fields(self):
        """Test creating a player with all fields"""
        player = Player(
            player_id="P002",
            username="vip_player",
            email="vip@example.com",
            registration_date=datetime(2025, 1, 1),
            country="UK",
            balance=Decimal('5000.00'),
            currency='GBP',
            status='active',
            kyc_verified=True,
            last_login=datetime(2025, 1, 15),
            vip_tier='platinum',
            total_deposits=Decimal('10000.00'),
            total_withdrawals=Decimal('3000.00'),
            total_wagered=Decimal('25000.00'),
            total_won=Decimal('20000.00')
        )

        assert player.balance == Decimal('5000.00')
        assert player.currency == 'GBP'
        assert player.kyc_verified is True
        assert player.vip_tier == 'platinum'
        assert player.total_deposits == Decimal('10000.00')

    def test_player_status_values(self):
        """Test different player status values"""
        statuses = ['active', 'suspended', 'banned', 'closed']

        for status in statuses:
            player = Player(
                player_id=f"P_{status}",
                username=f"player_{status}",
                email=f"{status}@example.com",
                registration_date=datetime.now(),
                country="US",
                status=status
            )
            assert player.status == status

    def test_player_vip_tiers(self):
        """Test different VIP tier values"""
        tiers = ['basic', 'silver', 'gold', 'platinum']

        for tier in tiers:
            player = Player(
                player_id=f"P_{tier}",
                username=f"player_{tier}",
                email=f"{tier}@example.com",
                registration_date=datetime.now(),
                country="US",
                vip_tier=tier
            )
            assert player.vip_tier == tier

    def test_player_to_dict(self):
        """Test player serialization to dictionary"""
        player = Player(
            player_id="P003",
            username="dict_test",
            email="dict@example.com",
            registration_date=datetime(2025, 1, 1, 12, 0, 0),
            country="CA",
            balance=Decimal('1000.50'),
            total_wagered=Decimal('5000.00')
        )

        player_dict = player.to_dict()

        assert isinstance(player_dict, dict)
        assert player_dict['player_id'] == "P003"
        assert player_dict['username'] == "dict_test"
        assert player_dict['email'] == "dict@example.com"
        assert player_dict['country'] == "CA"
        assert player_dict['balance'] == '1000.50'
        assert player_dict['total_wagered'] == '5000.00'
        assert isinstance(player_dict['registration_date'], str)
        assert isinstance(player_dict['created_at'], str)

    def test_player_decimal_precision(self):
        """Test that financial values maintain decimal precision"""
        player = Player(
            player_id="P004",
            username="decimal_test",
            email="decimal@example.com",
            registration_date=datetime.now(),
            country="US",
            balance=Decimal('123.45'),
            total_deposits=Decimal('1000.99'),
            total_withdrawals=Decimal('500.50')
        )

        assert player.balance == Decimal('123.45')
        assert player.total_deposits == Decimal('1000.99')
        assert player.total_withdrawals == Decimal('500.50')

    def test_player_timestamps_auto_generated(self):
        """Test that created_at and updated_at are automatically set"""
        player = Player(
            player_id="P005",
            username="timestamp_test",
            email="timestamp@example.com",
            registration_date=datetime.now(),
            country="US"
        )

        assert player.created_at is not None
        assert player.updated_at is not None
        assert isinstance(player.created_at, datetime)
        assert isinstance(player.updated_at, datetime)

    def test_player_optional_last_login(self):
        """Test that last_login can be None"""
        player = Player(
            player_id="P006",
            username="no_login",
            email="no_login@example.com",
            registration_date=datetime.now(),
            country="US"
        )

        assert player.last_login is None

        player_dict = player.to_dict()
        assert player_dict['last_login'] is None

    def test_player_currencies(self):
        """Test different currency values"""
        currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD']

        for currency in currencies:
            player = Player(
                player_id=f"P_{currency}",
                username=f"player_{currency}",
                email=f"{currency}@example.com",
                registration_date=datetime.now(),
                country="US",
                currency=currency
            )
            assert player.currency == currency

    def test_player_countries(self):
        """Test different country values"""
        countries = ['US', 'UK', 'CA', 'AU', 'DE', 'FR', 'ES', 'IT']

        for country in countries:
            player = Player(
                player_id=f"P_{country}",
                username=f"player_{country}",
                email=f"{country}@example.com",
                registration_date=datetime.now(),
                country=country
            )
            assert player.country == country

    def test_player_to_dict_with_last_login(self):
        """Test serialization with last_login set"""
        last_login = datetime(2025, 1, 15, 10, 30, 0)
        player = Player(
            player_id="P007",
            username="login_test",
            email="login@example.com",
            registration_date=datetime(2025, 1, 1),
            country="US",
            last_login=last_login
        )

        player_dict = player.to_dict()
        assert player_dict['last_login'] is not None
        assert isinstance(player_dict['last_login'], str)
        assert '2025-01-15' in player_dict['last_login']