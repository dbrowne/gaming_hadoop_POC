"""
Test cases for Event model
"""
import pytest
from datetime import datetime
from models.event import Event


class TestEvent:
    """Test Event model"""

    def test_event_creation_with_required_fields(self):
        """Test creating an event with only required fields"""
        event = Event(
            event_id="E001",
            event_type="login",
            event_category="player"
        )

        assert event.event_id == "E001"
        assert event.event_type == "login"
        assert event.event_category == "player"
        assert event.severity == 'info'
        assert event.source == 'system'
        assert event.player_id is None

    def test_event_types(self):
        """Test different event types"""
        event_types = [
            'login', 'logout', 'game_start', 'game_end',
            'bet_placed', 'bonus_claimed', 'kyc_update',
            'password_reset', 'account_created'
        ]

        for event_type in event_types:
            event = Event(
                event_id=f"E_{event_type}",
                event_type=event_type,
                event_category="player"
            )
            assert event.event_type == event_type

    def test_event_categories(self):
        """Test different event categories"""
        categories = ['player', 'game', 'transaction', 'system', 'security']

        for category in categories:
            event = Event(
                event_id=f"E_cat_{category}",
                event_type="action",
                event_category=category
            )
            assert event.event_category == category

    def test_event_severity_levels(self):
        """Test different severity levels"""
        severities = ['debug', 'info', 'warning', 'error', 'critical']

        for severity in severities:
            event = Event(
                event_id=f"E_sev_{severity}",
                event_type="system_event",
                event_category="system",
                severity=severity
            )
            assert event.severity == severity

    def test_event_sources(self):
        """Test different event sources"""
        sources = ['system', 'player', 'admin', 'api']

        for source in sources:
            event = Event(
                event_id=f"E_src_{source}",
                event_type="action",
                event_category="system",
                source=source
            )
            assert event.source == source

    def test_event_player_login(self):
        """Test player login event"""
        event = Event(
            event_id="E002",
            event_type="login",
            event_category="player",
            player_id="P001",
            session_id="S001",
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0",
            device_type="mobile",
            country="US",
            severity="info"
        )

        assert event.event_type == "login"
        assert event.player_id == "P001"
        assert event.session_id == "S001"
        assert event.ip_address == "192.168.1.100"
        assert event.device_type == "mobile"
        assert event.country == "US"

    def test_event_bet_placed(self):
        """Test bet placed event"""
        event = Event(
            event_id="E003",
            event_type="bet_placed",
            event_category="game",
            player_id="P001",
            session_id="S001",
            game_id="G001",
            bet_id="B001",
            severity="info"
        )

        assert event.event_type == "bet_placed"
        assert event.player_id == "P001"
        assert event.game_id == "G001"
        assert event.bet_id == "B001"

    def test_event_transaction_completed(self):
        """Test transaction completed event"""
        event = Event(
            event_id="E004",
            event_type="transaction_completed",
            event_category="transaction",
            player_id="P001",
            transaction_id="T001",
            severity="info"
        )

        assert event.event_type == "transaction_completed"
        assert event.transaction_id == "T001"

    def test_event_with_data(self):
        """Test event with event_data"""
        event_data = {
            'amount': '100.00',
            'method': 'credit_card',
            'status': 'success'
        }

        event = Event(
            event_id="E005",
            event_type="deposit",
            event_category="transaction",
            player_id="P001",
            event_data=event_data
        )

        assert event.event_data == event_data
        assert event.event_data['amount'] == '100.00'
        assert event.event_data['method'] == 'credit_card'

    def test_event_security_warning(self):
        """Test security warning event"""
        event = Event(
            event_id="E006",
            event_type="multiple_failed_logins",
            event_category="security",
            player_id="P001",
            ip_address="192.168.1.200",
            severity="warning",
            event_data={'attempts': 5, 'timeframe': '5 minutes'}
        )

        assert event.event_category == "security"
        assert event.severity == "warning"
        assert event.event_data['attempts'] == 5

    def test_event_system_error(self):
        """Test system error event"""
        event = Event(
            event_id="E007",
            event_type="database_connection_failed",
            event_category="system",
            severity="critical",
            event_data={'error': 'Connection timeout', 'retry_count': 3}
        )

        assert event.event_category == "system"
        assert event.severity == "critical"
        assert event.event_data['error'] == 'Connection timeout'

    def test_event_game_session(self):
        """Test game session event"""
        event = Event(
            event_id="E008",
            event_type="game_start",
            event_category="game",
            player_id="P001",
            session_id="S001",
            game_id="G001",
            device_type="desktop",
            severity="info"
        )

        assert event.event_type == "game_start"
        assert event.game_id == "G001"
        assert event.device_type == "desktop"

    def test_event_kyc_update(self):
        """Test KYC update event"""
        event = Event(
            event_id="E009",
            event_type="kyc_verified",
            event_category="player",
            player_id="P001",
            severity="info",
            source="admin",
            event_data={'verified_by': 'admin001', 'documents': ['passport', 'utility_bill']}
        )

        assert event.event_type == "kyc_verified"
        assert event.source == "admin"
        assert event.event_data['verified_by'] == 'admin001'

    def test_event_bonus_claimed(self):
        """Test bonus claimed event"""
        event = Event(
            event_id="E010",
            event_type="bonus_claimed",
            event_category="player",
            player_id="P001",
            severity="info",
            event_data={'bonus_id': 'WELCOME100', 'amount': '100.00'}
        )

        assert event.event_type == "bonus_claimed"
        assert event.event_data['bonus_id'] == 'WELCOME100'

    def test_event_timestamps(self):
        """Test event timestamps"""
        event_time = datetime(2025, 1, 15, 10, 30, 0)

        event = Event(
            event_id="E011",
            event_type="login",
            event_category="player",
            player_id="P001",
            event_timestamp=event_time
        )

        assert event.event_timestamp == event_time
        assert event.created_at is not None

    def test_event_to_dict(self):
        """Test event serialization to dictionary"""
        event_time = datetime(2025, 1, 15, 10, 0, 0)
        event_data = {'action': 'login', 'success': True}

        event = Event(
            event_id="E012",
            event_type="login",
            event_category="player",
            player_id="P002",
            session_id="S010",
            event_data=event_data,
            severity="info",
            source="player",
            ip_address="10.0.0.1",
            user_agent="Chrome/90.0",
            device_type="mobile",
            country="CA",
            event_timestamp=event_time
        )

        event_dict = event.to_dict()

        assert isinstance(event_dict, dict)
        assert event_dict['event_id'] == "E012"
        assert event_dict['event_type'] == "login"
        assert event_dict['event_category'] == "player"
        assert event_dict['player_id'] == "P002"
        assert event_dict['session_id'] == "S010"
        assert event_dict['event_data'] == event_data
        assert event_dict['severity'] == "info"
        assert event_dict['source'] == "player"
        assert event_dict['ip_address'] == "10.0.0.1"
        assert event_dict['user_agent'] == "Chrome/90.0"
        assert event_dict['device_type'] == "mobile"
        assert event_dict['country'] == "CA"
        assert isinstance(event_dict['event_timestamp'], str)
        assert isinstance(event_dict['created_at'], str)

    def test_event_to_dict_with_optional_fields_none(self):
        """Test serialization with optional fields as None"""
        event = Event(
            event_id="E013",
            event_type="system_startup",
            event_category="system"
        )

        event_dict = event.to_dict()

        assert event_dict['player_id'] is None
        assert event_dict['session_id'] is None
        assert event_dict['game_id'] is None
        assert event_dict['bet_id'] is None
        assert event_dict['transaction_id'] is None
        assert event_dict['event_data'] is None
        assert event_dict['ip_address'] is None
        assert event_dict['user_agent'] is None
        assert event_dict['device_type'] is None
        assert event_dict['country'] is None

    def test_event_device_types(self):
        """Test events from different device types"""
        device_types = ['desktop', 'mobile', 'tablet']

        for device_type in device_types:
            event = Event(
                event_id=f"E_dev_{device_type}",
                event_type="login",
                event_category="player",
                device_type=device_type
            )
            assert event.device_type == device_type

    def test_event_countries(self):
        """Test events from different countries"""
        countries = ['US', 'UK', 'CA', 'AU', 'DE']

        for country in countries:
            event = Event(
                event_id=f"E_country_{country}",
                event_type="login",
                event_category="player",
                country=country
            )
            assert event.country == country

    def test_event_with_all_ids(self):
        """Test event with all ID fields populated"""
        event = Event(
            event_id="E014",
            event_type="comprehensive_event",
            event_category="game",
            player_id="P001",
            session_id="S001",
            game_id="G001",
            bet_id="B001",
            transaction_id="T001"
        )

        assert event.player_id == "P001"
        assert event.session_id == "S001"
        assert event.game_id == "G001"
        assert event.bet_id == "B001"
        assert event.transaction_id == "T001"