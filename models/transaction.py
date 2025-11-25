"""
Transaction data model for online gambling platform
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal


@dataclass
class Transaction:
    transaction_id: str
    player_id: str
    transaction_type: str  # deposit, withdrawal, bet, payout, bonus, refund, adjustment
    amount: Decimal
    currency: str = 'USD'
    status: str = 'pending'  # pending, completed, failed, cancelled, processing
    payment_method: Optional[str] = None  # credit_card, bank_transfer, ewallet, crypto, etc.
    payment_provider: Optional[str] = None
    provider_transaction_id: Optional[str] = None
    balance_before: Decimal = Decimal('0.00')
    balance_after: Decimal = Decimal('0.00')
    session_id: Optional[str] = None
    bet_id: Optional[str] = None
    game_id: Optional[str] = None
    bonus_id: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    fee: Decimal = Decimal('0.00')
    net_amount: Optional[Decimal] = None
    processing_time_seconds: Optional[int] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    transaction_timestamp: datetime = field(default_factory=datetime.utcnow)
    completed_timestamp: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for Hadoop storage"""
        return {
            'transaction_id': self.transaction_id,
            'player_id': self.player_id,
            'transaction_type': self.transaction_type,
            'amount': str(self.amount),
            'currency': self.currency,
            'status': self.status,
            'payment_method': self.payment_method,
            'payment_provider': self.payment_provider,
            'provider_transaction_id': self.provider_transaction_id,
            'balance_before': str(self.balance_before),
            'balance_after': str(self.balance_after),
            'session_id': self.session_id,
            'bet_id': self.bet_id,
            'game_id': self.game_id,
            'bonus_id': self.bonus_id,
            'description': self.description,
            'metadata': self.metadata,
            'fee': str(self.fee),
            'net_amount': str(self.net_amount) if self.net_amount else None,
            'processing_time_seconds': self.processing_time_seconds,
            'error_code': self.error_code,
            'error_message': self.error_message,
            'transaction_timestamp': self.transaction_timestamp.isoformat(),
            'completed_timestamp': self.completed_timestamp.isoformat() if self.completed_timestamp else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }