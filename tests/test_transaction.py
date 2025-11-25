"""
Test cases for Transaction model
"""
import pytest
from datetime import datetime
from decimal import Decimal
from models.transaction import Transaction


class TestTransaction:
    """Test Transaction model"""

    def test_transaction_creation_with_required_fields(self):
        """Test creating a transaction with only required fields"""
        transaction = Transaction(
            transaction_id="T001",
            player_id="P001",
            transaction_type="deposit",
            amount=Decimal('100.00')
        )

        assert transaction.transaction_id == "T001"
        assert transaction.player_id == "P001"
        assert transaction.transaction_type == "deposit"
        assert transaction.amount == Decimal('100.00')
        assert transaction.currency == 'USD'
        assert transaction.status == 'pending'
        assert transaction.balance_before == Decimal('0.00')
        assert transaction.balance_after == Decimal('0.00')
        assert transaction.fee == Decimal('0.00')

    def test_transaction_types(self):
        """Test different transaction types"""
        tx_types = ['deposit', 'withdrawal', 'bet', 'payout', 'bonus', 'refund', 'adjustment']

        for tx_type in tx_types:
            transaction = Transaction(
                transaction_id=f"T_{tx_type}",
                player_id="P001",
                transaction_type=tx_type,
                amount=Decimal('50.00')
            )
            assert transaction.transaction_type == tx_type

    def test_transaction_statuses(self):
        """Test different transaction statuses"""
        statuses = ['pending', 'completed', 'failed', 'cancelled', 'processing']

        for status in statuses:
            transaction = Transaction(
                transaction_id=f"T_{status}",
                player_id="P001",
                transaction_type="deposit",
                amount=Decimal('100.00'),
                status=status
            )
            assert transaction.status == status

    def test_transaction_deposit(self):
        """Test deposit transaction"""
        transaction = Transaction(
            transaction_id="T002",
            player_id="P001",
            transaction_type="deposit",
            amount=Decimal('500.00'),
            currency='USD',
            status='completed',
            payment_method='credit_card',
            payment_provider='Stripe',
            balance_before=Decimal('100.00'),
            balance_after=Decimal('600.00')
        )

        assert transaction.transaction_type == "deposit"
        assert transaction.amount == Decimal('500.00')
        assert transaction.payment_method == 'credit_card'
        assert transaction.payment_provider == 'Stripe'
        assert transaction.balance_after - transaction.balance_before == Decimal('500.00')

    def test_transaction_withdrawal(self):
        """Test withdrawal transaction"""
        transaction = Transaction(
            transaction_id="T003",
            player_id="P001",
            transaction_type="withdrawal",
            amount=Decimal('200.00'),
            status='completed',
            payment_method='bank_transfer',
            balance_before=Decimal('1000.00'),
            balance_after=Decimal('800.00')
        )

        assert transaction.transaction_type == "withdrawal"
        assert transaction.amount == Decimal('200.00')
        assert transaction.balance_before - transaction.balance_after == Decimal('200.00')

    def test_transaction_payment_methods(self):
        """Test different payment methods"""
        payment_methods = ['credit_card', 'bank_transfer', 'ewallet', 'crypto', 'debit_card']

        for method in payment_methods:
            transaction = Transaction(
                transaction_id=f"T_{method}",
                player_id="P001",
                transaction_type="deposit",
                amount=Decimal('100.00'),
                payment_method=method
            )
            assert transaction.payment_method == method

    def test_transaction_with_fee(self):
        """Test transaction with processing fee"""
        transaction = Transaction(
            transaction_id="T004",
            player_id="P001",
            transaction_type="withdrawal",
            amount=Decimal('1000.00'),
            fee=Decimal('25.00'),
            net_amount=Decimal('975.00'),
            status='completed'
        )

        assert transaction.fee == Decimal('25.00')
        assert transaction.net_amount == Decimal('975.00')
        assert transaction.amount - transaction.fee == transaction.net_amount

    def test_transaction_bet_related(self):
        """Test transaction related to a bet"""
        transaction = Transaction(
            transaction_id="T005",
            player_id="P001",
            transaction_type="bet",
            amount=Decimal('10.00'),
            session_id="S001",
            bet_id="B001",
            game_id="G001",
            balance_before=Decimal('100.00'),
            balance_after=Decimal('90.00')
        )

        assert transaction.transaction_type == "bet"
        assert transaction.session_id == "S001"
        assert transaction.bet_id == "B001"
        assert transaction.game_id == "G001"

    def test_transaction_payout_related(self):
        """Test payout transaction"""
        transaction = Transaction(
            transaction_id="T006",
            player_id="P001",
            transaction_type="payout",
            amount=Decimal('50.00'),
            session_id="S001",
            bet_id="B001",
            game_id="G001",
            balance_before=Decimal('90.00'),
            balance_after=Decimal('140.00')
        )

        assert transaction.transaction_type == "payout"
        assert transaction.balance_after - transaction.balance_before == Decimal('50.00')

    def test_transaction_bonus(self):
        """Test bonus transaction"""
        transaction = Transaction(
            transaction_id="T007",
            player_id="P001",
            transaction_type="bonus",
            amount=Decimal('100.00'),
            bonus_id="BONUS001",
            description="Welcome bonus",
            status='completed',
            balance_before=Decimal('0.00'),
            balance_after=Decimal('100.00')
        )

        assert transaction.transaction_type == "bonus"
        assert transaction.bonus_id == "BONUS001"
        assert transaction.description == "Welcome bonus"

    def test_transaction_with_metadata(self):
        """Test transaction with metadata"""
        metadata = {
            'ip_address': '192.168.1.1',
            'device': 'mobile',
            'location': 'US'
        }

        transaction = Transaction(
            transaction_id="T008",
            player_id="P001",
            transaction_type="deposit",
            amount=Decimal('50.00'),
            metadata=metadata
        )

        assert transaction.metadata == metadata
        assert transaction.metadata['device'] == 'mobile'

    def test_transaction_provider_id(self):
        """Test transaction with provider transaction ID"""
        transaction = Transaction(
            transaction_id="T009",
            player_id="P001",
            transaction_type="deposit",
            amount=Decimal('100.00'),
            payment_provider='Stripe',
            provider_transaction_id='ch_1234567890'
        )

        assert transaction.provider_transaction_id == 'ch_1234567890'

    def test_transaction_failed_with_error(self):
        """Test failed transaction with error details"""
        transaction = Transaction(
            transaction_id="T010",
            player_id="P001",
            transaction_type="deposit",
            amount=Decimal('500.00'),
            status='failed',
            error_code='INSUFFICIENT_FUNDS',
            error_message='Card has insufficient funds'
        )

        assert transaction.status == 'failed'
        assert transaction.error_code == 'INSUFFICIENT_FUNDS'
        assert transaction.error_message == 'Card has insufficient funds'

    def test_transaction_processing_time(self):
        """Test transaction with processing time"""
        transaction = Transaction(
            transaction_id="T011",
            player_id="P001",
            transaction_type="withdrawal",
            amount=Decimal('1000.00'),
            status='completed',
            processing_time_seconds=120
        )

        assert transaction.processing_time_seconds == 120

    def test_transaction_to_dict(self):
        """Test transaction serialization to dictionary"""
        tx_time = datetime(2025, 1, 15, 10, 0, 0)
        completed_time = datetime(2025, 1, 15, 10, 2, 0)

        transaction = Transaction(
            transaction_id="T012",
            player_id="P002",
            transaction_type="deposit",
            amount=Decimal('250.00'),
            currency='EUR',
            status='completed',
            payment_method='ewallet',
            payment_provider='PayPal',
            balance_before=Decimal('100.00'),
            balance_after=Decimal('350.00'),
            fee=Decimal('5.00'),
            net_amount=Decimal('245.00'),
            transaction_timestamp=tx_time,
            completed_timestamp=completed_time,
            processing_time_seconds=120
        )

        tx_dict = transaction.to_dict()

        assert isinstance(tx_dict, dict)
        assert tx_dict['transaction_id'] == "T012"
        assert tx_dict['player_id'] == "P002"
        assert tx_dict['transaction_type'] == "deposit"
        assert tx_dict['amount'] == '250.00'
        assert tx_dict['currency'] == 'EUR'
        assert tx_dict['status'] == 'completed'
        assert tx_dict['payment_method'] == 'ewallet'
        assert tx_dict['payment_provider'] == 'PayPal'
        assert tx_dict['balance_before'] == '100.00'
        assert tx_dict['balance_after'] == '350.00'
        assert tx_dict['fee'] == '5.00'
        assert tx_dict['net_amount'] == '245.00'
        assert tx_dict['processing_time_seconds'] == 120
        assert isinstance(tx_dict['transaction_timestamp'], str)
        assert isinstance(tx_dict['completed_timestamp'], str)

    def test_transaction_to_dict_with_optional_fields_none(self):
        """Test serialization with optional fields as None"""
        transaction = Transaction(
            transaction_id="T013",
            player_id="P001",
            transaction_type="deposit",
            amount=Decimal('100.00')
        )

        tx_dict = transaction.to_dict()

        assert tx_dict['payment_method'] is None
        assert tx_dict['payment_provider'] is None
        assert tx_dict['provider_transaction_id'] is None
        assert tx_dict['session_id'] is None
        assert tx_dict['bet_id'] is None
        assert tx_dict['game_id'] is None
        assert tx_dict['bonus_id'] is None
        assert tx_dict['description'] is None
        assert tx_dict['metadata'] is None
        assert tx_dict['net_amount'] is None
        assert tx_dict['processing_time_seconds'] is None
        assert tx_dict['error_code'] is None
        assert tx_dict['error_message'] is None
        assert tx_dict['completed_timestamp'] is None

    def test_transaction_currencies(self):
        """Test transactions with different currencies"""
        currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD']

        for currency in currencies:
            transaction = Transaction(
                transaction_id=f"T_{currency}",
                player_id="P001",
                transaction_type="deposit",
                amount=Decimal('100.00'),
                currency=currency
            )
            assert transaction.currency == currency

    def test_transaction_various_amounts(self):
        """Test transactions with various amounts"""
        amounts = [
            Decimal('10.00'),
            Decimal('100.00'),
            Decimal('1000.00'),
            Decimal('10000.00')
        ]

        for amount in amounts:
            transaction = Transaction(
                transaction_id=f"T_amt_{amount}",
                player_id="P001",
                transaction_type="deposit",
                amount=amount
            )
            assert transaction.amount == amount