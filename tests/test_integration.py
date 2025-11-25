"""
Integration tests for gaming platform models
Tests interactions between different models
"""
import pytest
from datetime import datetime
from decimal import Decimal
from models import Player, Game, Bet, Session, Transaction, Event


class TestModelIntegration:
    """Test integration between different models"""

    def test_complete_player_session_flow(self):
        """Test a complete flow from player creation to session and betting"""
        # Create player
        player = Player(
            player_id="P001",
            username="integration_test",
            email="integration@example.com",
            registration_date=datetime.now(),
            country="US",
            balance=Decimal('1000.00')
        )

        # Create game
        game = Game(
            game_id="G001",
            game_name="Integration Slot",
            game_type="slot",
            provider="TestProvider",
            rtp=Decimal('96.5'),
            volatility="medium",
            min_bet=Decimal('1.00'),
            max_bet=Decimal('100.00')
        )

        # Create session
        session = Session(
            session_id="S001",
            player_id=player.player_id,
            session_start=datetime.now(),
            starting_balance=player.balance
        )

        # Create bet
        bet = Bet(
            bet_id="B001",
            player_id=player.player_id,
            game_id=game.game_id,
            session_id=session.session_id,
            bet_amount=Decimal('10.00'),
            bet_status='won',
            payout_amount=Decimal('50.00')
        )

        # Verify relationships
        assert bet.player_id == player.player_id
        assert bet.game_id == game.game_id
        assert bet.session_id == session.session_id
        assert session.player_id == player.player_id
        assert bet.bet_amount <= game.max_bet
        assert bet.bet_amount >= game.min_bet
        assert bet.net_profit == Decimal('40.00')

    def test_transaction_affects_player_balance(self):
        """Test that transactions properly track balance changes"""
        player = Player(
            player_id="P002",
            username="balance_test",
            email="balance@example.com",
            registration_date=datetime.now(),
            country="US",
            balance=Decimal('100.00')
        )

        # Deposit transaction
        deposit = Transaction(
            transaction_id="T001",
            player_id=player.player_id,
            transaction_type="deposit",
            amount=Decimal('500.00'),
            balance_before=player.balance,
            balance_after=player.balance + Decimal('500.00'),
            status='completed'
        )

        # Verify balance tracking
        assert deposit.balance_after - deposit.balance_before == deposit.amount

        # Withdrawal transaction
        withdrawal = Transaction(
            transaction_id="T002",
            player_id=player.player_id,
            transaction_type="withdrawal",
            amount=Decimal('200.00'),
            balance_before=Decimal('600.00'),
            balance_after=Decimal('400.00'),
            status='completed'
        )

        assert withdrawal.balance_before - withdrawal.balance_after == withdrawal.amount

    def test_event_tracking_for_player_actions(self):
        """Test that events properly track player actions"""
        player = Player(
            player_id="P003",
            username="event_test",
            email="event@example.com",
            registration_date=datetime.now(),
            country="US"
        )

        session = Session(
            session_id="S002",
            player_id=player.player_id,
            session_start=datetime.now()
        )

        # Login event
        login_event = Event(
            event_id="E001",
            event_type="login",
            event_category="player",
            player_id=player.player_id,
            session_id=session.session_id
        )

        # Bet event
        bet = Bet(
            bet_id="B002",
            player_id=player.player_id,
            game_id="G001",
            session_id=session.session_id,
            bet_amount=Decimal('10.00')
        )

        bet_event = Event(
            event_id="E002",
            event_type="bet_placed",
            event_category="game",
            player_id=player.player_id,
            session_id=session.session_id,
            bet_id=bet.bet_id
        )

        # Verify event relationships
        assert login_event.player_id == player.player_id
        assert login_event.session_id == session.session_id
        assert bet_event.player_id == player.player_id
        assert bet_event.bet_id == bet.bet_id

    def test_session_aggregates_bets(self):
        """Test that session can track multiple bets"""
        session = Session(
            session_id="S003",
            player_id="P004",
            session_start=datetime.now(),
            starting_balance=Decimal('1000.00')
        )

        bets = [
            Bet(
                bet_id=f"B{i:03d}",
                player_id="P004",
                game_id="G001",
                session_id=session.session_id,
                bet_amount=Decimal('10.00'),
                payout_amount=Decimal('20.00') if i % 2 == 0 else Decimal('0.00')
            )
            for i in range(1, 11)
        ]

        # Calculate session totals
        total_bets = len(bets)
        total_wagered = sum(bet.bet_amount for bet in bets)
        total_won = sum(bet.payout_amount for bet in bets)

        # Update session
        session.total_bets = total_bets
        session.total_wagered = total_wagered
        session.total_won = total_won

        assert session.total_bets == 10
        assert session.total_wagered == Decimal('100.00')
        assert session.total_won == Decimal('100.00')  # 5 wins * 20.00
        assert session.net_result == Decimal('0.00')

    def test_game_statistics_from_bets(self):
        """Test that game statistics can be derived from bets"""
        game = Game(
            game_id="G002",
            game_name="Statistics Test",
            game_type="slot",
            provider="Provider",
            rtp=Decimal('96.0'),
            volatility="medium",
            min_bet=Decimal('1.00'),
            max_bet=Decimal('100.00')
        )

        bets = [
            Bet(
                bet_id=f"B{i:03d}",
                player_id="P001",
                game_id=game.game_id,
                session_id="S001",
                bet_amount=Decimal('5.00'),
                payout_amount=Decimal('10.00') if i % 3 == 0 else Decimal('0.00')
            )
            for i in range(1, 101)
        ]

        # Calculate game statistics
        total_plays = len(bets)
        total_wagered = sum(bet.bet_amount for bet in bets)
        total_paid = sum(bet.payout_amount for bet in bets)

        # Update game
        game.total_plays = total_plays
        game.total_wagered = total_wagered
        game.total_paid = total_paid

        assert game.total_plays == 100
        assert game.total_wagered == Decimal('500.00')
        # 33 wins (every 3rd bet) * 10.00 = 330.00
        assert game.total_paid > Decimal('0.00')

    def test_serialization_round_trip(self):
        """Test that all models can be serialized and data preserved"""
        player = Player(
            player_id="P005",
            username="serialize_test",
            email="serialize@example.com",
            registration_date=datetime(2025, 1, 1),
            country="US",
            balance=Decimal('1000.00')
        )

        player_dict = player.to_dict()

        # Verify critical fields are preserved
        assert player_dict['player_id'] == player.player_id
        assert player_dict['username'] == player.username
        assert player_dict['email'] == player.email
        assert player_dict['balance'] == str(player.balance)
        assert player_dict['country'] == player.country

    def test_bet_within_game_limits(self):
        """Test that bets respect game betting limits"""
        game = Game(
            game_id="G003",
            game_name="Limit Test",
            game_type="slot",
            provider="Provider",
            rtp=Decimal('96.0'),
            volatility="medium",
            min_bet=Decimal('5.00'),
            max_bet=Decimal('50.00')
        )

        valid_bet = Bet(
            bet_id="B_VALID",
            player_id="P001",
            game_id=game.game_id,
            session_id="S001",
            bet_amount=Decimal('25.00')
        )

        assert valid_bet.bet_amount >= game.min_bet
        assert valid_bet.bet_amount <= game.max_bet

    def test_player_vip_tier_progression(self):
        """Test player VIP tier based on wagering"""
        players = [
            Player(
                player_id=f"P{i:03d}",
                username=f"player_{i}",
                email=f"player{i}@example.com",
                registration_date=datetime.now(),
                country="US",
                total_wagered=Decimal(str(i * 10000)),
                vip_tier='basic' if i < 5 else 'silver' if i < 10 else 'gold'
            )
            for i in range(1, 11)
        ]

        # Verify VIP tiers based on wagering
        for player in players:
            if player.total_wagered < Decimal('50000'):
                assert player.vip_tier == 'basic'
            elif player.total_wagered < Decimal('100000'):
                assert player.vip_tier == 'silver'
            else:
                assert player.vip_tier == 'gold'