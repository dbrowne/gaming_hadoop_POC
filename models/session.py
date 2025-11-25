"""
Session data model for online gambling platform
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from decimal import Decimal


@dataclass
class Session:
    session_id: str
    player_id: str
    session_start: datetime
    session_end: Optional[datetime] = None
    device_type: str = 'desktop'  # desktop, mobile, tablet
    platform: str = 'web'  # web, ios, android
    ip_address: Optional[str] = None
    country: Optional[str] = None
    user_agent: Optional[str] = None
    starting_balance: Decimal = Decimal('0.00')
    ending_balance: Optional[Decimal] = None
    total_bets: int = 0
    total_wagered: Decimal = Decimal('0.00')
    total_won: Decimal = Decimal('0.00')
    total_lost: Decimal = Decimal('0.00')
    games_played: int = 0
    session_status: str = 'active'  # active, ended, timeout, forced_logout
    session_duration_seconds: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for Hadoop storage"""
        return {
            'session_id': self.session_id,
            'player_id': self.player_id,
            'session_start': self.session_start.isoformat(),
            'session_end': self.session_end.isoformat() if self.session_end else None,
            'device_type': self.device_type,
            'platform': self.platform,
            'ip_address': self.ip_address,
            'country': self.country,
            'user_agent': self.user_agent,
            'starting_balance': str(self.starting_balance),
            'ending_balance': str(self.ending_balance) if self.ending_balance else None,
            'total_bets': self.total_bets,
            'total_wagered': str(self.total_wagered),
            'total_won': str(self.total_won),
            'total_lost': str(self.total_lost),
            'games_played': self.games_played,
            'session_status': self.session_status,
            'session_duration_seconds': self.session_duration_seconds,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @property
    def net_result(self) -> Decimal:
        """Calculate net profit/loss for this session"""
        return self.total_won - self.total_wagered