"""
Test cases for Kafka Producer
"""
import pytest
import json
from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import after path setup
from scripts.kafka_producer import (
    json_serializer,
    generate_bet_event,
    generate_transaction_event,
    generate_player_event,
    create_producer
)


class TestJsonSerializer:
    """Test JSON serialization helper"""

    def test_serialize_decimal(self):
        """Test Decimal serialization"""
        result = json_serializer(Decimal('123.45'))
        assert result == 123.45
        assert isinstance(result, float)

    def test_serialize_datetime(self):
        """Test datetime serialization"""
        dt = datetime(2024, 1, 15, 10, 30, 0)
        result = json_serializer(dt)
        assert result == '2024-01-15T10:30:00'
        assert isinstance(result, str)

    def test_serialize_unsupported_type(self):
        """Test that unsupported types raise TypeError"""
        with pytest.raises(TypeError):
            json_serializer(set([1, 2, 3]))


class TestGenerateBetEvent:
    """Test bet event generation"""

    def test_generate_bet_event_structure(self):
        """Test that bet event has correct structure"""
        event = generate_bet_event()

        assert 'event_type' in event
        assert 'timestamp' in event
        assert 'data' in event
        assert event['event_type'] == 'bet'
        assert isinstance(event['timestamp'], datetime)
        assert isinstance(event['data'], dict)

    def test_bet_event_data_fields(self):
        """Test that bet event data has required fields"""
        event = generate_bet_event()
        data = event['data']

        required_fields = [
            'bet_id', 'player_id', 'game_id', 'session_id',
            'bet_amount', 'bet_status', 'payout_amount', 'is_jackpot'
        ]

        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_bet_id_format(self):
        """Test bet ID format"""
        event = generate_bet_event()
        bet_id = event['data']['bet_id']

        assert bet_id.startswith('BK')
        assert len(bet_id) == 10  # BK + 8 digits

    def test_bet_status_values(self):
        """Test bet status is either won or lost"""
        # Generate multiple events to test randomness
        statuses = set()
        for _ in range(50):
            event = generate_bet_event()
            statuses.add(event['data']['bet_status'])

        assert statuses.issubset({'won', 'lost'})

    def test_won_bet_has_payout(self):
        """Test that won bets have positive payout"""
        # Generate until we get a won bet
        for _ in range(100):
            event = generate_bet_event()
            if event['data']['bet_status'] == 'won':
                payout = float(event['data']['payout_amount'])
                bet_amount = float(event['data']['bet_amount'])
                assert payout > 0
                assert payout >= bet_amount
                break
        else:
            pytest.skip("No won bets generated in 100 attempts")

    def test_lost_bet_has_zero_payout(self):
        """Test that lost bets have zero payout"""
        # Generate until we get a lost bet
        for _ in range(100):
            event = generate_bet_event()
            if event['data']['bet_status'] == 'lost':
                payout = float(event['data']['payout_amount'])
                assert payout == 0.0
                break
        else:
            pytest.skip("No lost bets generated in 100 attempts")


class TestGenerateTransactionEvent:
    """Test transaction event generation"""

    def test_generate_transaction_event_structure(self):
        """Test that transaction event has correct structure"""
        event = generate_transaction_event()

        assert 'event_type' in event
        assert 'timestamp' in event
        assert 'data' in event
        assert event['event_type'] == 'transaction'
        assert isinstance(event['timestamp'], datetime)

    def test_transaction_event_data_fields(self):
        """Test that transaction event data has required fields"""
        event = generate_transaction_event()
        data = event['data']

        required_fields = [
            'transaction_id', 'player_id', 'transaction_type',
            'amount', 'currency', 'status', 'payment_method'
        ]

        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_transaction_id_format(self):
        """Test transaction ID format"""
        event = generate_transaction_event()
        transaction_id = event['data']['transaction_id']

        assert transaction_id.startswith('TK')
        assert len(transaction_id) == 10  # TK + 8 digits

    def test_transaction_types(self):
        """Test transaction types are valid"""
        valid_types = {'deposit', 'withdrawal', 'bonus', 'refund'}
        types_found = set()

        for _ in range(50):
            event = generate_transaction_event()
            types_found.add(event['data']['transaction_type'])

        assert types_found.issubset(valid_types)

    def test_transaction_amount_positive(self):
        """Test transaction amount is positive"""
        event = generate_transaction_event()
        amount = float(event['data']['amount'])
        assert amount > 0

    def test_transaction_status_values(self):
        """Test transaction status values are valid"""
        valid_statuses = {'completed', 'pending', 'failed'}
        statuses_found = set()

        for _ in range(50):
            event = generate_transaction_event()
            statuses_found.add(event['data']['status'])

        assert statuses_found.issubset(valid_statuses)


class TestGeneratePlayerEvent:
    """Test player activity event generation"""

    def test_generate_player_event_structure(self):
        """Test that player event has correct structure"""
        event = generate_player_event()

        assert 'event_type' in event
        assert 'timestamp' in event
        assert 'data' in event
        assert event['event_type'] == 'player_activity'
        assert isinstance(event['timestamp'], datetime)

    def test_player_event_data_fields(self):
        """Test that player event data has required fields"""
        event = generate_player_event()
        data = event['data']

        required_fields = [
            'event_id', 'player_id', 'event_type',
            'event_category', 'event_timestamp'
        ]

        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_event_id_format(self):
        """Test event ID format"""
        event = generate_player_event()
        event_id = event['data']['event_id']

        assert event_id.startswith('EK')
        assert len(event_id) == 10  # EK + 8 digits

    def test_event_types_valid(self):
        """Test event types are valid"""
        valid_types = {
            'login', 'logout', 'game_start',
            'game_end', 'bonus_claimed', 'level_up'
        }
        types_found = set()

        for _ in range(100):
            event = generate_player_event()
            types_found.add(event['data']['event_type'])

        assert types_found.issubset(valid_types)

    def test_event_categories_valid(self):
        """Test event categories are valid"""
        valid_categories = {
            'authentication', 'gameplay',
            'promotion', 'progression'
        }
        categories_found = set()

        for _ in range(100):
            event = generate_player_event()
            categories_found.add(event['data']['event_category'])

        assert categories_found.issubset(valid_categories)


class TestCreateProducer:
    """Test Kafka producer creation"""

    @patch('scripts.kafka_producer.Producer')
    def test_create_producer_success(self, mock_producer):
        """Test successful producer creation"""
        mock_instance = MagicMock()
        mock_producer.return_value = mock_instance

        producer = create_producer('localhost:9093')

        assert producer is not None
        mock_producer.assert_called_once()

        # Check configuration
        call_args = mock_producer.call_args
        config = call_args[0][0]
        assert config['bootstrap.servers'] == 'localhost:9093'
        assert config['client.id'] == 'gambling-producer'
        assert config['acks'] == 'all'

    @patch('scripts.kafka_producer.Producer')
    def test_create_producer_failure(self, mock_producer):
        """Test producer creation failure"""
        from confluent_kafka import KafkaException
        mock_producer.side_effect = KafkaException('Connection failed')

        producer = create_producer('invalid:9093')

        assert producer is None


class TestEventSerialization:
    """Test that events can be serialized to JSON"""

    def test_bet_event_json_serializable(self):
        """Test bet event can be serialized to JSON"""
        event = generate_bet_event()

        # Should not raise exception
        json_str = json.dumps(event, default=json_serializer)
        assert isinstance(json_str, str)

        # Should be deserializable
        parsed = json.loads(json_str)
        assert parsed['event_type'] == 'bet'

    def test_transaction_event_json_serializable(self):
        """Test transaction event can be serialized to JSON"""
        event = generate_transaction_event()

        json_str = json.dumps(event, default=json_serializer)
        assert isinstance(json_str, str)

        parsed = json.loads(json_str)
        assert parsed['event_type'] == 'transaction'

    def test_player_event_json_serializable(self):
        """Test player event can be serialized to JSON"""
        event = generate_player_event()

        json_str = json.dumps(event, default=json_serializer)
        assert isinstance(json_str, str)

        parsed = json.loads(json_str)
        assert parsed['event_type'] == 'player_activity'


class TestEventDistribution:
    """Test event generation distribution"""

    def test_counter_increments(self):
        """Test that counters increment properly"""
        # Import to reset counters
        import importlib
        import scripts.kafka_producer as kp
        importlib.reload(kp)

        # Generate events
        bet1 = kp.generate_bet_event()
        bet2 = kp.generate_bet_event()

        id1 = bet1['data']['bet_id']
        id2 = bet2['data']['bet_id']

        # Extract numbers
        num1 = int(id1[2:])
        num2 = int(id2[2:])

        assert num2 == num1 + 1