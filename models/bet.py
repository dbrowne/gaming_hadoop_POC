"""
Bet/Wager data model for online gambling platform
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal


@dataclass
class Bet:
    bet_id: str
    player_id: str
    game_id: str
    session_id: str
    bet_amount: Decimal
    currency: str = 'USD'
    bet_type: str = 'standard'  # standard, bonus, free_spin, jackpot
    bet_status: str = 'pending'  # pending, won, lost, cancelled, void
    payout_amount: Decimal = Decimal('0.00')
    win_multiplier: Optional[Decimal] = None
    bet_details: Optional[Dict[str, Any]] = None  # game-specific details
    is_jackpot: bool = False
    jackpot_amount: Optional[Decimal] = None
    bonus_used: Optional[str] = None
    bet_timestamp: datetime = field(default_factory=datetime.utcnow)
    settled_timestamp: Optional[datetime] = None
    round_id: Optional[str] = None  # for multi-round games
    outcome: Optional[Dict[str, Any]] = None  # game outcome details
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for Hadoop storage"""
        return {
            'bet_id': self.bet_id,
            'player_id': self.player_id,
            'game_id': self.game_id,
            'session_id': self.session_id,
            'bet_amount': str(self.bet_amount),
            'currency': self.currency,
            'bet_type': self.bet_type,
            'bet_status': self.bet_status,
            'payout_amount': str(self.payout_amount),
            'win_multiplier': str(self.win_multiplier) if self.win_multiplier else None,
            'bet_details': self.bet_details,
            'is_jackpot': self.is_jackpot,
            'jackpot_amount': str(self.jackpot_amount) if self.jackpot_amount else None,
            'bonus_used': self.bonus_used,
            'bet_timestamp': self.bet_timestamp.isoformat(),
            'settled_timestamp': self.settled_timestamp.isoformat() if self.settled_timestamp else None,
            'round_id': self.round_id,
            'outcome': self.outcome,
            'created_at': self.created_at.isoformat()
        }

    @property
    def net_profit(self) -> Decimal:
        """Calculate net profit/loss for this bet"""
        return self.payout_amount - self.bet_amount