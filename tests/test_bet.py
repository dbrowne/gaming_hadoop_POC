"""
Test cases for Bet model
"""
import pytest
from datetime import datetime
from decimal import Decimal
from models.bet import Bet


class TestBet:
    """Test Bet model"""

    def test_bet_creation_with_required_fields(self):
        """Test creating a bet with only required fields"""
        bet = Bet(
            bet_id="B001",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('10.00')
        )

        assert bet.bet_id == "B001"
        assert bet.player_id == "P001"
        assert bet.game_id == "G001"
        assert bet.session_id == "S001"
        assert bet.bet_amount == Decimal('10.00')
        assert bet.currency == 'USD'
        assert bet.bet_type == 'standard'
        assert bet.bet_status == 'pending'
        assert bet.payout_amount == Decimal('0.00')

    def test_bet_types(self):
        """Test different bet types"""
        bet_types = ['standard', 'bonus', 'free_spin', 'jackpot']

        for bet_type in bet_types:
            bet = Bet(
                bet_id=f"B_{bet_type}",
                player_id="P001",
                game_id="G001",
                session_id="S001",
                bet_amount=Decimal('10.00'),
                bet_type=bet_type
            )
            assert bet.bet_type == bet_type

    def test_bet_statuses(self):
        """Test different bet statuses"""
        statuses = ['pending', 'won', 'lost', 'cancelled', 'void']

        for status in statuses:
            bet = Bet(
                bet_id=f"B_{status}",
                player_id="P001",
                game_id="G001",
                session_id="S001",
                bet_amount=Decimal('10.00'),
                bet_status=status
            )
            assert bet.bet_status == status

    def test_bet_won_with_payout(self):
        """Test a winning bet with payout"""
        bet = Bet(
            bet_id="B002",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('10.00'),
            bet_status='won',
            payout_amount=Decimal('50.00'),
            win_multiplier=Decimal('5.0')
        )

        assert bet.bet_status == 'won'
        assert bet.payout_amount == Decimal('50.00')
        assert bet.win_multiplier == Decimal('5.0')

    def test_bet_lost_no_payout(self):
        """Test a losing bet with no payout"""
        bet = Bet(
            bet_id="B003",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('20.00'),
            bet_status='lost',
            payout_amount=Decimal('0.00')
        )

        assert bet.bet_status == 'lost'
        assert bet.payout_amount == Decimal('0.00')

    def test_bet_net_profit_won(self):
        """Test net_profit calculation for winning bet"""
        bet = Bet(
            bet_id="B004",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('10.00'),
            payout_amount=Decimal('50.00')
        )

        assert bet.net_profit == Decimal('40.00')

    def test_bet_net_profit_lost(self):
        """Test net_profit calculation for losing bet"""
        bet = Bet(
            bet_id="B005",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('25.00'),
            payout_amount=Decimal('0.00')
        )

        assert bet.net_profit == Decimal('-25.00')

    def test_bet_net_profit_break_even(self):
        """Test net_profit calculation for break-even bet"""
        bet = Bet(
            bet_id="B006",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('15.00'),
            payout_amount=Decimal('15.00')
        )

        assert bet.net_profit == Decimal('0.00')

    def test_bet_jackpot(self):
        """Test jackpot bet"""
        bet = Bet(
            bet_id="B007",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('5.00'),
            bet_status='won',
            payout_amount=Decimal('100000.00'),
            is_jackpot=True,
            jackpot_amount=Decimal('100000.00')
        )

        assert bet.is_jackpot is True
        assert bet.jackpot_amount == Decimal('100000.00')

    def test_bet_with_bonus(self):
        """Test bet using bonus"""
        bet = Bet(
            bet_id="B008",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('10.00'),
            bet_type='bonus',
            bonus_used='WELCOME100'
        )

        assert bet.bet_type == 'bonus'
        assert bet.bonus_used == 'WELCOME100'

    def test_bet_with_details(self):
        """Test bet with game-specific details"""
        bet_details = {
            'numbers': [7, 14, 21, 35, 42],
            'bet_type': 'straight_up',
            'table_id': 'T001'
        }

        bet = Bet(
            bet_id="B009",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('10.00'),
            bet_details=bet_details
        )

        assert bet.bet_details == bet_details
        assert bet.bet_details['table_id'] == 'T001'

    def test_bet_with_outcome(self):
        """Test bet with outcome details"""
        outcome = {
            'result': 'win',
            'symbols': ['cherry', 'cherry', 'cherry'],
            'win_line': 5
        }

        bet = Bet(
            bet_id="B010",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('2.00'),
            bet_status='won',
            payout_amount=Decimal('10.00'),
            outcome=outcome
        )

        assert bet.outcome == outcome
        assert bet.outcome['result'] == 'win'

    def test_bet_with_round_id(self):
        """Test bet with round_id for multi-round games"""
        bet = Bet(
            bet_id="B011",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('25.00'),
            round_id="R001"
        )

        assert bet.round_id == "R001"

    def test_bet_timestamps(self):
        """Test bet timestamps"""
        bet_time = datetime(2025, 1, 15, 14, 30, 0)
        settled_time = datetime(2025, 1, 15, 14, 30, 5)

        bet = Bet(
            bet_id="B012",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('10.00'),
            bet_timestamp=bet_time,
            settled_timestamp=settled_time
        )

        assert bet.bet_timestamp == bet_time
        assert bet.settled_timestamp == settled_time

    def test_bet_to_dict(self):
        """Test bet serialization to dictionary"""
        bet = Bet(
            bet_id="B013",
            player_id="P002",
            game_id="G005",
            session_id="S010",
            bet_amount=Decimal('15.50'),
            currency='EUR',
            bet_type='standard',
            bet_status='won',
            payout_amount=Decimal('77.50'),
            win_multiplier=Decimal('5.0'),
            settled_timestamp=datetime(2025, 1, 15, 10, 0, 0)
        )

        bet_dict = bet.to_dict()

        assert isinstance(bet_dict, dict)
        assert bet_dict['bet_id'] == "B013"
        assert bet_dict['player_id'] == "P002"
        assert bet_dict['game_id'] == "G005"
        assert bet_dict['session_id'] == "S010"
        assert bet_dict['bet_amount'] == '15.50'
        assert bet_dict['currency'] == 'EUR'
        assert bet_dict['bet_type'] == 'standard'
        assert bet_dict['bet_status'] == 'won'
        assert bet_dict['payout_amount'] == '77.50'
        assert bet_dict['win_multiplier'] == '5.0'
        assert bet_dict['is_jackpot'] is False
        assert isinstance(bet_dict['bet_timestamp'], str)
        assert isinstance(bet_dict['settled_timestamp'], str)

    def test_bet_to_dict_with_optional_fields_none(self):
        """Test serialization with optional fields as None"""
        bet = Bet(
            bet_id="B014",
            player_id="P001",
            game_id="G001",
            session_id="S001",
            bet_amount=Decimal('10.00')
        )

        bet_dict = bet.to_dict()

        assert bet_dict['win_multiplier'] is None
        assert bet_dict['bet_details'] is None
        assert bet_dict['jackpot_amount'] is None
        assert bet_dict['bonus_used'] is None
        assert bet_dict['settled_timestamp'] is None
        assert bet_dict['round_id'] is None
        assert bet_dict['outcome'] is None

    def test_bet_various_amounts(self):
        """Test bets with various amounts"""
        amounts = [
            Decimal('0.10'),
            Decimal('1.00'),
            Decimal('10.00'),
            Decimal('100.00'),
            Decimal('1000.00')
        ]

        for amount in amounts:
            bet = Bet(
                bet_id=f"B_amt_{amount}",
                player_id="P001",
                game_id="G001",
                session_id="S001",
                bet_amount=amount
            )
            assert bet.bet_amount == amount

    def test_bet_win_multipliers(self):
        """Test various win multipliers"""
        multipliers = [
            Decimal('1.5'),
            Decimal('2.0'),
            Decimal('5.0'),
            Decimal('10.0'),
            Decimal('100.0')
        ]

        for multiplier in multipliers:
            bet_amount = Decimal('10.00')
            payout = bet_amount * multiplier

            bet = Bet(
                bet_id=f"B_mult_{multiplier}",
                player_id="P001",
                game_id="G001",
                session_id="S001",
                bet_amount=bet_amount,
                payout_amount=payout,
                win_multiplier=multiplier
            )
            assert bet.win_multiplier == multiplier
            assert bet.payout_amount == payout

    def test_bet_currencies(self):
        """Test bets with different currencies"""
        currencies = ['USD', 'EUR', 'GBP', 'CAD']

        for currency in currencies:
            bet = Bet(
                bet_id=f"B_{currency}",
                player_id="P001",
                game_id="G001",
                session_id="S001",
                bet_amount=Decimal('10.00'),
                currency=currency
            )
            assert bet.currency == currency