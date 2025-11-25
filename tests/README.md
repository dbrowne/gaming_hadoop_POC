# Test Suite for Gaming Platform Data Models

Comprehensive test coverage for all data models in the online gambling platform POC.

## Test Statistics

- **Total Tests**: 106
- **Test Files**: 7
- **Models Covered**: 6 (Player, Game, Bet, Session, Transaction, Event)
- **Coverage**: Unit tests + Integration tests

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Shared fixtures and test configuration
├── test_player.py              # Player model tests (11 tests)
├── test_game.py                # Game model tests (15 tests)
├── test_bet.py                 # Bet model tests (19 tests)
├── test_session.py             # Session model tests (15 tests)
├── test_transaction.py         # Transaction model tests (18 tests)
├── test_event.py               # Event model tests (20 tests)
├── test_integration.py         # Integration tests (8 tests)
└── README.md                   # This file
```

## Running Tests

### Run All Tests

```bash
# Using pytest directly
pytest tests/ -v

# Using the test runner script
./scripts/run_tests.sh

# Run specific test file
pytest tests/test_player.py -v

# Run specific test class
pytest tests/test_player.py::TestPlayer -v

# Run specific test
pytest tests/test_player.py::TestPlayer::test_player_creation_with_required_fields -v
```

### Run Tests with Coverage

```bash
# Generate coverage report
pytest tests/ --cov=models --cov-report=term-missing

# Generate HTML coverage report
pytest tests/ --cov=models --cov-report=html

# Then open htmlcov/index.html in browser
```

### Run Tests by Category

```bash
# Run unit tests only
pytest tests/ -m unit -v

# Run integration tests only
pytest tests/ -m integration -v

# Run fast tests (exclude slow tests)
pytest tests/ -m "not slow" -v
```

## Test Coverage by Model

### Player Model (test_player.py)

Tests cover:
- Creation with required and optional fields
- Player status values (active, suspended, banned, closed)
- VIP tiers (basic, silver, gold, platinum)
- Currency handling
- Country codes
- Balance and financial tracking
- Serialization to dictionary
- Timestamp auto-generation
- Decimal precision for financial values

**Key Tests:**
- `test_player_creation_with_required_fields`
- `test_player_vip_tiers`
- `test_player_to_dict`
- `test_player_decimal_precision`

### Game Model (test_game.py)

Tests cover:
- Game types (slot, poker, roulette, blackjack, etc.)
- Volatility levels (low, medium, high)
- Game status (active, inactive, maintenance)
- RTP percentage precision
- Betting limits (min/max)
- Slot-specific fields (reels, lines)
- Features and tags
- Game providers
- Statistics tracking

**Key Tests:**
- `test_game_creation_with_required_fields`
- `test_game_types`
- `test_game_rtp_precision`
- `test_game_betting_limits`

### Bet Model (test_bet.py)

Tests cover:
- Bet types (standard, bonus, free_spin, jackpot)
- Bet statuses (pending, won, lost, cancelled, void)
- Payout calculations
- Net profit calculation (property)
- Win multipliers
- Jackpot bets
- Bonus bets
- Game-specific bet details
- Round IDs for multi-round games
- Outcome tracking

**Key Tests:**
- `test_bet_net_profit_won`
- `test_bet_net_profit_lost`
- `test_bet_jackpot`
- `test_bet_win_multipliers`

### Session Model (test_session.py)

Tests cover:
- Device types (desktop, mobile, tablet)
- Platforms (web, ios, android)
- Session statuses (active, ended, timeout, forced_logout)
- Net result calculation (property)
- Balance tracking (starting/ending)
- Betting statistics (total bets, wagered, won)
- Session duration
- IP addresses and countries
- Multi-game sessions

**Key Tests:**
- `test_session_net_result_won`
- `test_session_net_result_lost`
- `test_session_balance_tracking`
- `test_session_multiple_games`

### Transaction Model (test_transaction.py)

Tests cover:
- Transaction types (deposit, withdrawal, bet, payout, bonus, refund, adjustment)
- Transaction statuses (pending, completed, failed, cancelled, processing)
- Payment methods (credit_card, bank_transfer, ewallet, crypto)
- Transaction fees
- Balance tracking (before/after)
- Provider transaction IDs
- Failed transactions with error details
- Processing time tracking
- Metadata support

**Key Tests:**
- `test_transaction_deposit`
- `test_transaction_withdrawal`
- `test_transaction_with_fee`
- `test_transaction_failed_with_error`

### Event Model (test_event.py)

Tests cover:
- Event types (login, logout, game_start, bet_placed, etc.)
- Event categories (player, game, transaction, system, security)
- Severity levels (debug, info, warning, error, critical)
- Event sources (system, player, admin, api)
- Event data storage
- Security events
- System errors
- KYC updates
- Bonus claims

**Key Tests:**
- `test_event_player_login`
- `test_event_security_warning`
- `test_event_system_error`
- `test_event_with_data`

### Integration Tests (test_integration.py)

Tests cover:
- Complete player session flow
- Transaction affecting player balance
- Event tracking for player actions
- Session aggregating multiple bets
- Game statistics from bets
- Serialization round-trip
- Bet limits validation
- VIP tier progression

**Key Tests:**
- `test_complete_player_session_flow`
- `test_transaction_affects_player_balance`
- `test_session_aggregates_bets`
- `test_player_vip_tier_progression`

## Test Fixtures

The `conftest.py` file provides shared fixtures for common test scenarios:

### Individual Model Fixtures
- `sample_player` - Standard player instance
- `sample_game` - Standard game instance
- `sample_bet` - Standard bet instance
- `sample_session` - Standard session instance
- `sample_transaction` - Standard transaction instance
- `sample_event` - Standard event instance

### Collection Fixtures
- `multiple_players` - List of 5 players
- `multiple_games` - List of 5 games
- `multiple_bets` - List of 5 bets

### Specialized Fixtures
- `winning_bet` - Pre-configured winning bet
- `losing_bet` - Pre-configured losing bet
- `jackpot_bet` - Jackpot winning bet
- `active_session` - Currently active session
- `ended_session` - Completed session
- `deposit_transaction` - Deposit transaction
- `withdrawal_transaction` - Withdrawal transaction
- `failed_transaction` - Failed transaction

### Using Fixtures

```python
def test_with_fixture(sample_player):
    """Example test using a fixture"""
    assert sample_player.player_id == "P001"
    assert sample_player.balance == Decimal('1000.00')
```

## Test Categories

Tests can be marked with categories:

```python
@pytest.mark.unit
def test_player_creation():
    """Unit test for player creation"""
    pass

@pytest.mark.integration
def test_player_session_flow():
    """Integration test for complete flow"""
    pass

@pytest.mark.slow
def test_large_dataset():
    """Test that takes significant time"""
    pass
```

## Writing New Tests

### Test File Template

```python
"""
Test cases for [Model] model
"""
import pytest
from datetime import datetime
from decimal import Decimal
from models.[model] import [Model]


class Test[Model]:
    """Test [Model] model"""

    def test_[model]_creation_with_required_fields(self):
        """Test creating a [model] with only required fields"""
        instance = [Model](
            # required fields
        )

        assert instance.field == expected_value

    def test_[model]_to_dict(self):
        """Test [model] serialization to dictionary"""
        instance = [Model](...)
        instance_dict = instance.to_dict()

        assert isinstance(instance_dict, dict)
        assert instance_dict['field'] == 'value'
```

### Best Practices

1. **Descriptive Test Names**: Use clear, descriptive test names that explain what is being tested
2. **Single Assertion Focus**: Each test should focus on one specific behavior
3. **Use Fixtures**: Leverage fixtures for common test data
4. **Test Edge Cases**: Include tests for boundary conditions and edge cases
5. **Decimal Precision**: Always use Decimal for financial values in tests
6. **Datetime Handling**: Use explicit datetime instances, not relative dates
7. **Isolation**: Tests should be independent and not rely on execution order

## Common Test Patterns

### Testing Required vs Optional Fields

```python
def test_with_required_fields_only(self):
    instance = Model(required_field="value")
    assert instance.optional_field is None

def test_with_all_fields(self):
    instance = Model(
        required_field="value",
        optional_field="optional"
    )
    assert instance.optional_field == "optional"
```

### Testing Enumerations

```python
def test_status_values(self):
    statuses = ['active', 'inactive', 'suspended']
    for status in statuses:
        instance = Model(status=status)
        assert instance.status == status
```

### Testing Calculated Properties

```python
def test_calculated_property(self):
    instance = Model(value1=10, value2=5)
    assert instance.calculated == 15
```

### Testing Serialization

```python
def test_to_dict(self):
    instance = Model(field=Decimal('10.00'))
    data = instance.to_dict()

    assert isinstance(data, dict)
    assert data['field'] == '10.00'  # Decimal converted to string
```

## Continuous Integration

To integrate with CI/CD:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ -v --cov=models --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v2
  with:
    file: ./coverage.xml
```

## Troubleshooting

### ImportError: No module named 'models'

Ensure you're running tests from the project root:
```bash
cd /path/to/gaming_hadoop_poc
pytest tests/
```

### Tests Passing Locally but Failing in CI

- Check Python version consistency
- Ensure all dependencies are in requirements.txt
- Verify timezone handling (use UTC)

### Deprecation Warnings

The test suite may show warnings about `datetime.utcnow()`. This is expected and will be addressed in future updates.

## Future Enhancements

- [ ] Add performance tests for large datasets
- [ ] Add tests for data validation
- [ ] Add tests for concurrent access scenarios
- [ ] Increase coverage to 100%
- [ ] Add mutation testing
- [ ] Add property-based testing with Hypothesis

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)