"""
Test cases for Session model
"""
import pytest
from datetime import datetime
from decimal import Decimal
from models.session import Session


class TestSession:
    """Test Session model"""

    def test_session_creation_with_required_fields(self):
        """Test creating a session with only required fields"""
        start_time = datetime(2025, 1, 15, 10, 0, 0)

        session = Session(
            session_id="S001",
            player_id="P001",
            session_start=start_time
        )

        assert session.session_id == "S001"
        assert session.player_id == "P001"
        assert session.session_start == start_time
        assert session.session_end is None
        assert session.device_type == 'desktop'
        assert session.platform == 'web'
        assert session.starting_balance == Decimal('0.00')
        assert session.total_bets == 0
        assert session.session_status == 'active'

    def test_session_device_types(self):
        """Test different device types"""
        device_types = ['desktop', 'mobile', 'tablet']

        for device_type in device_types:
            session = Session(
                session_id=f"S_{device_type}",
                player_id="P001",
                session_start=datetime.now(),
                device_type=device_type
            )
            assert session.device_type == device_type

    def test_session_platforms(self):
        """Test different platforms"""
        platforms = ['web', 'ios', 'android']

        for platform in platforms:
            session = Session(
                session_id=f"S_{platform}",
                player_id="P001",
                session_start=datetime.now(),
                platform=platform
            )
            assert session.platform == platform

    def test_session_status_values(self):
        """Test different session status values"""
        statuses = ['active', 'ended', 'timeout', 'forced_logout']

        for status in statuses:
            session = Session(
                session_id=f"S_{status}",
                player_id="P001",
                session_start=datetime.now(),
                session_status=status
            )
            assert session.session_status == status

    def test_session_with_all_fields(self):
        """Test session with all fields populated"""
        start_time = datetime(2025, 1, 15, 10, 0, 0)
        end_time = datetime(2025, 1, 15, 12, 30, 0)

        session = Session(
            session_id="S002",
            player_id="P002",
            session_start=start_time,
            session_end=end_time,
            device_type='mobile',
            platform='ios',
            ip_address='192.168.1.100',
            country='US',
            user_agent='Mozilla/5.0 iPhone',
            starting_balance=Decimal('1000.00'),
            ending_balance=Decimal('1250.00'),
            total_bets=50,
            total_wagered=Decimal('500.00'),
            total_won=Decimal('750.00'),
            total_lost=Decimal('0.00'),
            games_played=5,
            session_status='ended',
            session_duration_seconds=9000
        )

        assert session.session_end == end_time
        assert session.ip_address == '192.168.1.100'
        assert session.country == 'US'
        assert session.starting_balance == Decimal('1000.00')
        assert session.ending_balance == Decimal('1250.00')
        assert session.total_bets == 50
        assert session.total_wagered == Decimal('500.00')
        assert session.total_won == Decimal('750.00')
        assert session.games_played == 5
        assert session.session_duration_seconds == 9000

    def test_session_net_result_won(self):
        """Test net_result calculation for winning session"""
        session = Session(
            session_id="S003",
            player_id="P001",
            session_start=datetime.now(),
            total_wagered=Decimal('100.00'),
            total_won=Decimal('150.00')
        )

        assert session.net_result == Decimal('50.00')

    def test_session_net_result_lost(self):
        """Test net_result calculation for losing session"""
        session = Session(
            session_id="S004",
            player_id="P001",
            session_start=datetime.now(),
            total_wagered=Decimal('200.00'),
            total_won=Decimal('50.00')
        )

        assert session.net_result == Decimal('-150.00')

    def test_session_net_result_break_even(self):
        """Test net_result calculation for break-even session"""
        session = Session(
            session_id="S005",
            player_id="P001",
            session_start=datetime.now(),
            total_wagered=Decimal('100.00'),
            total_won=Decimal('100.00')
        )

        assert session.net_result == Decimal('0.00')

    def test_session_to_dict(self):
        """Test session serialization to dictionary"""
        start_time = datetime(2025, 1, 15, 10, 0, 0)
        end_time = datetime(2025, 1, 15, 11, 0, 0)

        session = Session(
            session_id="S006",
            player_id="P003",
            session_start=start_time,
            session_end=end_time,
            device_type='tablet',
            platform='android',
            ip_address='10.0.0.1',
            country='CA',
            starting_balance=Decimal('500.00'),
            ending_balance=Decimal('450.00'),
            total_bets=20,
            total_wagered=Decimal('100.00'),
            total_won=Decimal('50.00'),
            session_status='ended',
            session_duration_seconds=3600
        )

        session_dict = session.to_dict()

        assert isinstance(session_dict, dict)
        assert session_dict['session_id'] == "S006"
        assert session_dict['player_id'] == "P003"
        assert session_dict['device_type'] == 'tablet'
        assert session_dict['platform'] == 'android'
        assert session_dict['ip_address'] == '10.0.0.1'
        assert session_dict['country'] == 'CA'
        assert session_dict['starting_balance'] == '500.00'
        assert session_dict['ending_balance'] == '450.00'
        assert session_dict['total_bets'] == 20
        assert session_dict['total_wagered'] == '100.00'
        assert session_dict['total_won'] == '50.00'
        assert session_dict['session_status'] == 'ended'
        assert session_dict['session_duration_seconds'] == 3600
        assert isinstance(session_dict['session_start'], str)
        assert isinstance(session_dict['session_end'], str)

    def test_session_to_dict_active_session(self):
        """Test serialization of active session without end time"""
        session = Session(
            session_id="S007",
            player_id="P001",
            session_start=datetime.now(),
            session_status='active'
        )

        session_dict = session.to_dict()

        assert session_dict['session_end'] is None
        assert session_dict['ending_balance'] is None
        assert session_dict['session_status'] == 'active'

    def test_session_ip_addresses(self):
        """Test various IP address formats"""
        ip_addresses = ['192.168.1.1', '10.0.0.1', '172.16.0.1', '8.8.8.8']

        for ip in ip_addresses:
            session = Session(
                session_id=f"S_ip_{ip.replace('.', '_')}",
                player_id="P001",
                session_start=datetime.now(),
                ip_address=ip
            )
            assert session.ip_address == ip

    def test_session_countries(self):
        """Test different country codes"""
        countries = ['US', 'UK', 'CA', 'AU', 'DE', 'FR']

        for country in countries:
            session = Session(
                session_id=f"S_{country}",
                player_id="P001",
                session_start=datetime.now(),
                country=country
            )
            assert session.country == country

    def test_session_duration_calculation(self):
        """Test session duration in seconds"""
        durations = [60, 300, 1800, 3600, 7200]  # 1 min to 2 hours

        for duration in durations:
            session = Session(
                session_id=f"S_dur_{duration}",
                player_id="P001",
                session_start=datetime.now(),
                session_duration_seconds=duration
            )
            assert session.session_duration_seconds == duration

    def test_session_balance_tracking(self):
        """Test balance tracking during session"""
        session = Session(
            session_id="S008",
            player_id="P001",
            session_start=datetime.now(),
            starting_balance=Decimal('1000.00'),
            ending_balance=Decimal('1500.00')
        )

        balance_change = session.ending_balance - session.starting_balance
        assert balance_change == Decimal('500.00')

    def test_session_multiple_games(self):
        """Test session with multiple games played"""
        session = Session(
            session_id="S009",
            player_id="P001",
            session_start=datetime.now(),
            games_played=10,
            total_bets=100
        )

        assert session.games_played == 10
        assert session.total_bets == 100
        assert session.total_bets >= session.games_played