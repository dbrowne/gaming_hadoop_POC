"""
Game data model for online gambling platform
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal


@dataclass
class Game:
    game_id: str
    game_name: str
    game_type: str  # slot, poker, roulette, blackjack, sports_betting, live_dealer, etc.
    provider: str
    rtp: Decimal  # Return to Player percentage
    volatility: str  # low, medium, high
    min_bet: Decimal
    max_bet: Decimal
    currency: str = 'USD'
    status: str = 'active'  # active, inactive, maintenance
    features: Optional[Dict[str, Any]] = None  # bonus rounds, multipliers, etc.
    max_win: Optional[Decimal] = None
    lines: Optional[int] = None  # for slots
    reels: Optional[int] = None  # for slots
    tags: Optional[list] = None  # popular, new, jackpot, etc.
    release_date: Optional[datetime] = None
    total_plays: int = 0
    total_wagered: Decimal = Decimal('0.00')
    total_paid: Decimal = Decimal('0.00')
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for Hadoop storage"""
        return {
            'game_id': self.game_id,
            'game_name': self.game_name,
            'game_type': self.game_type,
            'provider': self.provider,
            'rtp': str(self.rtp),
            'volatility': self.volatility,
            'min_bet': str(self.min_bet),
            'max_bet': str(self.max_bet),
            'currency': self.currency,
            'status': self.status,
            'features': self.features,
            'max_win': str(self.max_win) if self.max_win else None,
            'lines': self.lines,
            'reels': self.reels,
            'tags': self.tags,
            'release_date': self.release_date.isoformat() if self.release_date else None,
            'total_plays': self.total_plays,
            'total_wagered': str(self.total_wagered),
            'total_paid': str(self.total_paid),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }