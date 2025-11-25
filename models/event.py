"""
Event data model for online gambling platform
Used for event tracking, analytics, and audit logs
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Event:
    event_id: str
    event_type: str  # login, logout, game_start, game_end, bet_placed, bonus_claimed, kyc_update, etc.
    event_category: str  # player, game, transaction, system, security
    player_id: Optional[str] = None
    session_id: Optional[str] = None
    game_id: Optional[str] = None
    bet_id: Optional[str] = None
    transaction_id: Optional[str] = None
    event_data: Optional[Dict[str, Any]] = None
    severity: str = 'info'  # debug, info, warning, error, critical
    source: str = 'system'  # system, player, admin, api
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    device_type: Optional[str] = None
    country: Optional[str] = None
    event_timestamp: datetime = field(default_factory=datetime.utcnow)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for Hadoop storage"""
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'event_category': self.event_category,
            'player_id': self.player_id,
            'session_id': self.session_id,
            'game_id': self.game_id,
            'bet_id': self.bet_id,
            'transaction_id': self.transaction_id,
            'event_data': self.event_data,
            'severity': self.severity,
            'source': self.source,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'device_type': self.device_type,
            'country': self.country,
            'event_timestamp': self.event_timestamp.isoformat(),
            'created_at': self.created_at.isoformat()
        }