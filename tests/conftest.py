"""
Pytest configuration and shared fixtures for model tests
"""
import pytest
from datetime import datetime, timedelta
from decimal import Decimal
from models import Player, Game, Bet, Session, Transaction, Event


@pytest.fixture
def sample_player():
    """Create a sample player for testing"""
    return Player(
        player_id="P001",
        username="test_player",
        email="test@example.com",
        registration_date=datetime(2025, 1, 1),
        country="US",
        balance=Decimal('1000.00'),
        currency='USD',
        kyc_verified=True,
        vip_tier='gold'
    )


@pytest.fixture
def sample_game():
    """Create a sample game for testing"""
    return Game(
        game_id="G001",
        game_name="Test Slot Machine",
        game_type="slot",
        provider="TestProvider",
        rtp=Decimal('96.5'),
        volatility="medium",
        min_bet=Decimal('0.10'),
        max_bet=Decimal('100.00'),
        reels=5,
        lines=20,
        tags=['popular', 'jackpot']
    )


@pytest.fixture
def sample_bet():
    """Create a sample bet for testing"""
    return Bet(
        bet_id="B001",
        player_id="P001",
        game_id="G001",
        session_id="S001",
        bet_amount=Decimal('10.00'),
        bet_type='standard',
        bet_status='won',
        payout_amount=Decimal('50.00'),
        win_multiplier=Decimal('5.0')
    )


@pytest.fixture
def sample_session():
    """Create a sample session for testing"""
    return Session(
        session_id="S001",
        player_id="P001",
        session_start=datetime(2025, 1, 15, 10, 0, 0),
        device_type='mobile',
        platform='ios',
        ip_address='192.168.1.1',
        country='US',
        starting_balance=Decimal('1000.00')
    )


@pytest.fixture
def sample_transaction():
    """Create a sample transaction for testing"""
    return Transaction(
        transaction_id="T001",
        player_id="P001",
        transaction_type="deposit",
        amount=Decimal('500.00'),
        currency='USD',
        status='completed',
        payment_method='credit_card',
        payment_provider='Stripe',
        balance_before=Decimal('500.00'),
        balance_after=Decimal('1000.00')
    )


@pytest.fixture
def sample_event():
    """Create a sample event for testing"""
    return Event(
        event_id="E001",
        event_type="login",
        event_category="player",
        player_id="P001",
        session_id="S001",
        severity="info",
        ip_address="192.168.1.1",
        device_type="mobile"
    )


@pytest.fixture
def multiple_players():
    """Create multiple players for testing"""
    return [
        Player(
            player_id=f"P{i:03d}",
            username=f"player_{i}",
            email=f"player{i}@example.com",
            registration_date=datetime.now() - timedelta(days=i),
            country="US",
            balance=Decimal(str(i * 100))
        )
        for i in range(1, 6)
    ]


@pytest.fixture
def multiple_games():
    """Create multiple games for testing"""
    game_types = ['slot', 'poker', 'roulette', 'blackjack', 'baccarat']
    return [
        Game(
            game_id=f"G{i:03d}",
            game_name=f"Game {i}",
            game_type=game_types[i-1],
            provider="TestProvider",
            rtp=Decimal('96.0'),
            volatility="medium",
            min_bet=Decimal('1.00'),
            max_bet=Decimal('100.00')
        )
        for i in range(1, 6)
    ]


@pytest.fixture
def multiple_bets():
    """Create multiple bets for testing"""
    return [
        Bet(
            bet_id=f"B{i:03d}",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal(str(i * 10)),
            bet_status='won' if i % 2 == 0 else 'lost',
            payout_amount=Decimal(str(i * 20)) if i % 2 == 0 else Decimal('0.00')
        )
        for i in range(1, 6)
    ]


@pytest.fixture
def winning_bet():
    """Create a winning bet"""
    return Bet(
        bet_id="B_WIN",
        player_id="P001",
        game_id="G001",
        session_id="S001",
        bet_amount=Decimal('10.00'),
        bet_status='won',
        payout_amount=Decimal('100.00'),
        win_multiplier=Decimal('10.0')
    )


@pytest.fixture
def losing_bet():
    """Create a losing bet"""
    return Bet(
        bet_id="B_LOSE",
        player_id="P001",
        game_id="G001",
        session_id="S001",
        bet_amount=Decimal('10.00'),
        bet_status='lost',
        payout_amount=Decimal('0.00')
    )


@pytest.fixture
def jackpot_bet():
    """Create a jackpot winning bet"""
    return Bet(
        bet_id="B_JACKPOT",
        player_id="P001",
        game_id="G001",
        session_id="S001",
        bet_amount=Decimal('5.00'),
        bet_status='won',
        payout_amount=Decimal('100000.00'),
        is_jackpot=True,
        jackpot_amount=Decimal('100000.00')
    )


@pytest.fixture
def active_session():
    """Create an active session"""
    return Session(
        session_id="S_ACTIVE",
        player_id="P001",
        session_start=datetime.now(),
        session_status='active',
        starting_balance=Decimal('1000.00')
    )


@pytest.fixture
def ended_session():
    """Create an ended session"""
    start = datetime.now() - timedelta(hours=2)
    end = datetime.now()
    return Session(
        session_id="S_ENDED",
        player_id="P001",
        session_start=start,
        session_end=end,
        session_status='ended',
        starting_balance=Decimal('1000.00'),
        ending_balance=Decimal('1200.00'),
        total_bets=50,
        total_wagered=Decimal('500.00'),
        total_won=Decimal('700.00'),
        session_duration_seconds=7200
    )


@pytest.fixture
def deposit_transaction():
    """Create a deposit transaction"""
    return Transaction(
        transaction_id="T_DEPOSIT",
        player_id="P001",
        transaction_type="deposit",
        amount=Decimal('1000.00'),
        status='completed',
        payment_method='credit_card',
        balance_before=Decimal('0.00'),
        balance_after=Decimal('1000.00')
    )


@pytest.fixture
def withdrawal_transaction():
    """Create a withdrawal transaction"""
    return Transaction(
        transaction_id="T_WITHDRAW",
        player_id="P001",
        transaction_type="withdrawal",
        amount=Decimal('500.00'),
        status='completed',
        payment_method='bank_transfer',
        balance_before=Decimal('1000.00'),
        balance_after=Decimal('500.00'),
        fee=Decimal('10.00')
    )


@pytest.fixture
def failed_transaction():
    """Create a failed transaction"""
    return Transaction(
        transaction_id="T_FAILED",
        player_id="P001",
        transaction_type="deposit",
        amount=Decimal('500.00'),
        status='failed',
        error_code='CARD_DECLINED',
        error_message='Card was declined by issuer'
    )