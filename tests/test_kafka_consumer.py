"""
Test cases for Kafka Consumer
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import after path setup
from scripts.kafka_consumer import (
    process_bet_event,
    process_transaction_event,
    process_player_activity_event,
    create_consumer,
    GracefulKiller
)


class TestProcessBetEvent:
    """Test bet event processing"""

    def test_process_bet_event_basic(self):
        """Test basic bet event processing"""
        event = {
            'event_type': 'bet',
            'data': {
                'bet_id': 'BK00000001',
                'player_id': 'P000001',
                'game_id': 'G000001',
                'bet_amount': '10.00',
                'bet_status': 'won',
                'payout_amount': '20.00'
            }
        }

        result = process_bet_event(event)

        assert result['type'] == 'BET'
        assert result['id'] == 'BK00000001'
        assert result['player'] == 'P000001'
        assert result['amount'] == '10.00'
        assert result['status'] == 'won'
        assert result['game'] == 'G000001'

    def test_process_bet_event_all_fields(self):
        """Test that all required fields are extracted"""
        event = {
            'data': {
                'bet_id': 'BK12345678',
                'player_id': 'P123456',
                'game_id': 'G999999',
                'bet_amount': '50.50',
                'bet_status': 'lost',
                'payout_amount': '0.00'
            }
        }

        result = process_bet_event(event)

        assert 'type' in result
        assert 'id' in result
        assert 'player' in result
        assert 'amount' in result
        assert 'status' in result
        assert 'game' in result

    def test_process_bet_event_missing_fields(self):
        """Test handling of missing fields"""
        event = {
            'data': {
                'bet_id': 'BK00000001',
                # Missing other fields
            }
        }

        with pytest.raises(KeyError):
            process_bet_event(event)


class TestProcessTransactionEvent:
    """Test transaction event processing"""

    def test_process_transaction_event_basic(self):
        """Test basic transaction event processing"""
        event = {
            'event_type': 'transaction',
            'data': {
                'transaction_id': 'TK00000001',
                'player_id': 'P000001',
                'transaction_type': 'deposit',
                'amount': '100.00',
                'status': 'completed'
            }
        }

        result = process_transaction_event(event)

        assert result['type'] == 'TRANSACTION'
        assert result['id'] == 'TK00000001'
        assert result['player'] == 'P000001'
        assert result['type_detail'] == 'deposit'
        assert result['amount'] == '100.00'
        assert result['status'] == 'completed'

    def test_process_transaction_event_all_types(self):
        """Test processing different transaction types"""
        transaction_types = ['deposit', 'withdrawal', 'bonus', 'refund']

        for tx_type in transaction_types:
            event = {
                'data': {
                    'transaction_id': 'TK00000001',
                    'player_id': 'P000001',
                    'transaction_type': tx_type,
                    'amount': '50.00',
                    'status': 'completed'
                }
            }

            result = process_transaction_event(event)
            assert result['type_detail'] == tx_type

    def test_process_transaction_event_statuses(self):
        """Test processing different transaction statuses"""
        statuses = ['completed', 'pending', 'failed']

        for status in statuses:
            event = {
                'data': {
                    'transaction_id': 'TK00000001',
                    'player_id': 'P000001',
                    'transaction_type': 'deposit',
                    'amount': '50.00',
                    'status': status
                }
            }

            result = process_transaction_event(event)
            assert result['status'] == status


class TestProcessPlayerActivityEvent:
    """Test player activity event processing"""

    def test_process_player_activity_event_basic(self):
        """Test basic player activity event processing"""
        event = {
            'event_type': 'player_activity',
            'data': {
                'event_id': 'EK00000001',
                'player_id': 'P000001',
                'event_type': 'login',
                'event_category': 'authentication'
            }
        }

        result = process_player_activity_event(event)

        assert result['type'] == 'ACTIVITY'
        assert result['id'] == 'EK00000001'
        assert result['player'] == 'P000001'
        assert result['action'] == 'login'
        assert result['category'] == 'authentication'

    def test_process_player_activity_event_types(self):
        """Test processing different event types"""
        event_types = ['login', 'logout', 'game_start', 'game_end', 'bonus_claimed', 'level_up']

        for evt_type in event_types:
            event = {
                'data': {
                    'event_id': 'EK00000001',
                    'player_id': 'P000001',
                    'event_type': evt_type,
                    'event_category': 'gameplay'
                }
            }

            result = process_player_activity_event(event)
            assert result['action'] == evt_type

    def test_process_player_activity_event_categories(self):
        """Test processing different event categories"""
        categories = ['authentication', 'gameplay', 'promotion', 'progression']

        for category in categories:
            event = {
                'data': {
                    'event_id': 'EK00000001',
                    'player_id': 'P000001',
                    'event_type': 'login',
                    'event_category': category
                }
            }

            result = process_player_activity_event(event)
            assert result['category'] == category


class TestCreateConsumer:
    """Test Kafka consumer creation"""

    @patch('scripts.kafka_consumer.Consumer')
    def test_create_consumer_success(self, mock_consumer):
        """Test successful consumer creation"""
        mock_instance = MagicMock()
        mock_consumer.return_value = mock_instance

        topics = ['gambling-bets', 'gambling-transactions']
        consumer = create_consumer(topics, 'localhost:9093', 'test-group')

        assert consumer is not None
        mock_consumer.assert_called_once()

        # Check configuration
        call_args = mock_consumer.call_args
        config = call_args[0][0]
        assert config['bootstrap.servers'] == 'localhost:9093'
        assert config['group.id'] == 'test-group'
        assert config['auto.offset.reset'] == 'earliest'
        assert config['enable.auto.commit'] is True

        # Check subscription
        mock_instance.subscribe.assert_called_once_with(topics)

    @patch('scripts.kafka_consumer.Consumer')
    def test_create_consumer_default_params(self, mock_consumer):
        """Test consumer creation with default parameters"""
        mock_instance = MagicMock()
        mock_consumer.return_value = mock_instance

        topics = ['test-topic']
        consumer = create_consumer(topics)

        assert consumer is not None

        # Check default configuration
        call_args = mock_consumer.call_args
        config = call_args[0][0]
        assert config['bootstrap.servers'] == 'localhost:9093'
        assert config['group.id'] == 'gambling-consumer'

    @patch('scripts.kafka_consumer.Consumer')
    def test_create_consumer_failure(self, mock_consumer):
        """Test consumer creation failure"""
        from confluent_kafka import KafkaException
        mock_consumer.side_effect = KafkaException('Connection failed')

        topics = ['test-topic']
        consumer = create_consumer(topics, 'invalid:9093')

        assert consumer is None

    @patch('scripts.kafka_consumer.Consumer')
    def test_create_consumer_multiple_topics(self, mock_consumer):
        """Test consumer creation with multiple topics"""
        mock_instance = MagicMock()
        mock_consumer.return_value = mock_instance

        topics = ['topic1', 'topic2', 'topic3']
        consumer = create_consumer(topics)

        assert consumer is not None
        mock_instance.subscribe.assert_called_once_with(topics)


class TestGracefulKiller:
    """Test graceful shutdown handler"""

    def test_graceful_killer_initialization(self):
        """Test GracefulKiller initialization"""
        killer = GracefulKiller()
        assert killer.kill_now is False

    @patch('signal.signal')
    def test_graceful_killer_registers_signals(self, mock_signal):
        """Test that signal handlers are registered"""
        import signal as sig
        killer = GracefulKiller()

        # Check that signal handlers were registered
        calls = mock_signal.call_args_list
        signal_types = [call[0][0] for call in calls]

        assert sig.SIGINT in signal_types
        assert sig.SIGTERM in signal_types

    def test_graceful_killer_exit_gracefully(self):
        """Test exit_gracefully method"""
        killer = GracefulKiller()
        assert killer.kill_now is False

        killer.exit_gracefully()
        assert killer.kill_now is True


class TestEventProcessingIntegration:
    """Integration tests for event processing"""

    def test_process_complete_bet_workflow(self):
        """Test processing a complete bet event workflow"""
        # Simulate a bet event from producer
        producer_event = {
            'event_type': 'bet',
            'timestamp': '2024-01-15T10:30:00',
            'data': {
                'bet_id': 'BK00000123',
                'player_id': 'P000045',
                'game_id': 'G000012',
                'session_id': 'S000789',
                'bet_amount': '25.50',
                'currency': 'USD',
                'bet_status': 'won',
                'payout_amount': '51.00',
                'win_multiplier': '2.00',
                'is_jackpot': False
            }
        }

        # Process the event
        result = process_bet_event(producer_event)

        # Verify all expected fields
        assert result['type'] == 'BET'
        assert result['id'] == 'BK00000123'
        assert result['player'] == 'P000045'
        assert result['amount'] == '25.50'
        assert result['status'] == 'won'
        assert result['game'] == 'G000012'

    def test_process_complete_transaction_workflow(self):
        """Test processing a complete transaction event workflow"""
        producer_event = {
            'event_type': 'transaction',
            'timestamp': '2024-01-15T10:30:00',
            'data': {
                'transaction_id': 'TK00000456',
                'player_id': 'P000045',
                'transaction_type': 'deposit',
                'amount': '100.00',
                'currency': 'USD',
                'status': 'completed',
                'payment_method': 'credit_card'
            }
        }

        result = process_transaction_event(producer_event)

        assert result['type'] == 'TRANSACTION'
        assert result['id'] == 'TK00000456'
        assert result['player'] == 'P000045'
        assert result['type_detail'] == 'deposit'
        assert result['amount'] == '100.00'
        assert result['status'] == 'completed'

    def test_process_complete_player_activity_workflow(self):
        """Test processing a complete player activity event workflow"""
        producer_event = {
            'event_type': 'player_activity',
            'timestamp': '2024-01-15T10:30:00',
            'data': {
                'event_id': 'EK00000789',
                'player_id': 'P000045',
                'event_type': 'login',
                'event_category': 'authentication',
                'event_timestamp': '2024-01-15T10:30:00'
            }
        }

        result = process_player_activity_event(producer_event)

        assert result['type'] == 'ACTIVITY'
        assert result['id'] == 'EK00000789'
        assert result['player'] == 'P000045'
        assert result['action'] == 'login'
        assert result['category'] == 'authentication'


class TestErrorHandling:
    """Test error handling in consumer"""

    def test_process_bet_event_with_extra_fields(self):
        """Test that extra fields don't break processing"""
        event = {
            'event_type': 'bet',
            'data': {
                'bet_id': 'BK00000001',
                'player_id': 'P000001',
                'game_id': 'G000001',
                'bet_amount': '10.00',
                'bet_status': 'won',
                'payout_amount': '20.00',
                'extra_field': 'should_be_ignored',
                'another_field': 123
            }
        }

        result = process_bet_event(event)

        # Should process successfully despite extra fields
        assert result['type'] == 'BET'
        assert result['id'] == 'BK00000001'

    def test_process_transaction_event_with_extra_fields(self):
        """Test transaction processing with extra fields"""
        event = {
            'data': {
                'transaction_id': 'TK00000001',
                'player_id': 'P000001',
                'transaction_type': 'deposit',
                'amount': '100.00',
                'status': 'completed',
                'metadata': {'ip': '1.2.3.4'}
            }
        }

        result = process_transaction_event(event)

        assert result['type'] == 'TRANSACTION'
        assert result['id'] == 'TK00000001'