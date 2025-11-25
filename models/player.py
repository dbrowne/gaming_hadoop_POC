"""
Player data model for online gambling platform
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from decimal import Decimal


@dataclass
class Player:
    player_id: str
    username: str
    email: str
    registration_date: datetime
    country: str
    balance: Decimal = Decimal('0.00')
    currency: str = 'USD'
    status: str = 'active'  # active, suspended, banned, closed
    kyc_verified: bool = False
    last_login: Optional[datetime] = None
    vip_tier: str = 'basic'  # basic, silver, gold, platinum
    total_deposits: Decimal = Decimal('0.00')
    total_withdrawals: Decimal = Decimal('0.00')
    total_wagered: Decimal = Decimal('0.00')
    total_won: Decimal = Decimal('0.00')
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for Hadoop storage"""
        return {
            'player_id': self.player_id,
            'username': self.username,
            'email': self.email,
            'registration_date': self.registration_date.isoformat(),
            'country': self.country,
            'balance': str(self.balance),
            'currency': self.currency,
            'status': self.status,
            'kyc_verified': self.kyc_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'vip_tier': self.vip_tier,
            'total_deposits': str(self.total_deposits),
            'total_withdrawals': str(self.total_withdrawals),
            'total_wagered': str(self.total_wagered),
            'total_won': str(self.total_won),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }