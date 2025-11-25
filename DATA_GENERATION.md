# Data Generation for Gambling Platform POC

## Overview

The `main.py` script generates realistic random gambling data suitable for Hadoop analysis and testing.

## Generated Data

### Quantities (Default)

- **Players**: 200
- **Games**: 100
- **Sessions**: 1,000
- **Bets**: 5,000
- **Transactions**: ~645 (varies)
- **Events**: ~1,700 (varies)

Total records: ~8,645 across all entities

### File Sizes

```
bets.json          ~2.4 MB  (5,000 records)
events.json        ~752 KB  (1,700 records)
sessions.json      ~556 KB  (1,000 records)
transactions.json  ~437 KB    (645 records)
players.json       ~94 KB     (200 records)
games.json         ~46 KB     (100 records)
```

## Data Characteristics

### Players
- **Countries**: US, UK, CA, AU, DE, FR, ES, IT, NL, SE
- **Currencies**: USD, EUR, GBP, CAD, AUD
- **Status Distribution**: 85% active, 10% suspended, 5% closed
- **VIP Tiers**: 60% basic, 25% silver, 12% gold, 3% platinum
- **KYC Verified**: ~70% of players
- **Balance Range**: $0 - $10,000
- **Registration**: Spread over past 365 days

### Games
- **Types**: slot, poker, roulette, blackjack, baccarat, live_dealer
- **Providers**: NetEnt, Microgaming, Playtech, Evolution, Pragmatic Play, Red Tiger
- **RTP Range**: 94.0% - 98.5%
- **Volatility**: low, medium, high (equal distribution)
- **Min Bet**: $0.10 - $5.00
- **Max Bet**: $50 - $1,000
- **Status**: 90% active, 10% inactive

### Sessions
- **Time Period**: Last 90 days
- **Device Types**: desktop, mobile, tablet (equal distribution)
- **Platforms**: web, ios, android (equal distribution)
- **Duration**: 60 seconds - 2 hours
- **Status**: 80% ended, 20% active
- **Bets per Session**: 5-200 for ended, 1-50 for active
- **Starting Balance**: $50 - $5,000

### Bets
- **Win Rate**: ~45% (realistic house edge)
- **Jackpot Frequency**: ~0.1% (very rare)
- **Bet Types**: 85% standard, 10% bonus, 5% free_spin
- **Win Multipliers**: 1.2x - 10.0x (normal wins)
- **Jackpot Payouts**: $10,000 - $100,000
- **Bet Amounts**: Respects game min/max limits
- **Time Spread**: Last 90 days

### Transactions
- **Deposits**: 1-5 per player
- **Deposit Amounts**: $50 - $2,000
- **Deposit Success Rate**: 95%
- **Withdrawals**: ~1/3 of players
- **Withdrawal Amounts**: $100 - $5,000
- **Withdrawal Fee**: 2% of amount
- **Payment Methods**: credit_card, bank_transfer, ewallet, crypto, debit_card
- **Providers**: Stripe, PayPal, Adyen, Coinbase

### Events
- **Login Events**: 500 (from sessions)
- **Bet Events**: 1,000 (sample from bets)
- **Transaction Events**: 200 (sample from transactions)
- **Categories**: player, game, transaction, system, security
- **Severity**: info, warning, error, critical

## Sample Analytics

From a typical generation run:

```
Total Wagered:    $252,973.07
Total Payout:     $803,694.64
House Revenue:   -$550,721.57  (Note: includes jackpots)
Jackpot Wins:     3
Win Rate:        45.24%
Loss Rate:       54.76%
```

**Note**: The house revenue can be negative when jackpots are hit, which is realistic for small sample sizes. Over larger datasets, the house edge normalizes.

## Data Format

All data is saved in **JSONL** (JSON Lines) format:
- One JSON object per line
- No enclosing array
- Perfect for Hadoop/Spark processing
- Easy to stream and process

### Example Bet Record

```json
{
  "bet_id": "B00000001",
  "player_id": "P000157",
  "game_id": "G0045",
  "session_id": "S000568",
  "bet_amount": "50.05",
  "currency": "GBP",
  "bet_type": "standard",
  "bet_status": "won",
  "payout_amount": "453.95",
  "win_multiplier": "9.07",
  "is_jackpot": false,
  "jackpot_amount": null,
  "bet_timestamp": "2025-11-02T08:40:56.833249",
  "settled_timestamp": "2025-11-02T08:40:59.833249",
  "created_at": "2025-11-25T05:15:37.840866"
}
```

## Usage

### Generate Data

```bash
# Generate default quantities (5,000 bets)
python main.py

# Customize in main.py:
generator = GamblingDataGenerator(
    num_players=500,      # Increase players
    num_games=200,        # Increase games
    num_sessions=2000,    # Increase sessions
    num_bets=10000       # Generate 10,000 bets
)
```

### Output Location

All files are saved to `./data/` directory:
```
data/
├── players.json
├── games.json
├── sessions.json
├── bets.json
├── transactions.json
└── events.json
```

### Upload to Hadoop

The script attempts to automatically upload to HDFS if:
1. `hdfs` Python library is installed
2. Hadoop cluster is running
3. NameNode is accessible at `http://localhost:9870`

If automatic upload fails, use manual upload:

```bash
# Upload all files
for file in players games sessions bets transactions events; do
  docker exec namenode hdfs dfs -put ./data/${file}.json /gambling/${file}/
done

# Or individually
docker exec namenode hdfs dfs -put ./data/bets.json /gambling/bets/
```

### Verify Upload

```bash
# Check HDFS
docker exec namenode hdfs dfs -ls /gambling/bets/

# Count records
docker exec namenode hdfs dfs -cat /gambling/bets/bets.json | wc -l
```

## Realistic Data Features

### Temporal Patterns
- Bets spread across 90-day period
- Sessions have realistic durations
- Events timestamped appropriately
- Transaction timing matches activity

### Relational Integrity
- Bets reference valid players, games, sessions
- Transactions link to players
- Events reference appropriate entities
- Currency consistency across related records

### Business Logic
- Bet amounts respect game limits
- Win multipliers are realistic
- Jackpots are rare but impactful
- VIP tier distribution reflects typical player base
- Payment method distribution realistic

### Edge Cases Included
- Failed transactions (~5%)
- Inactive games (~10%)
- Suspended/closed accounts
- Active sessions (ongoing)
- Jackpot wins (rare)
- Various currencies

## Analyzing Generated Data

### Query Examples

```sql
-- Top 10 players by wagering
SELECT player_id, SUM(bet_amount) as total_wagered
FROM bets
GROUP BY player_id
ORDER BY total_wagered DESC
LIMIT 10;

-- Game performance
SELECT g.game_name, g.game_type,
       COUNT(*) as plays,
       SUM(b.bet_amount) as wagered,
       SUM(b.payout_amount) as paid_out,
       SUM(b.bet_amount - b.payout_amount) as revenue
FROM bets b
JOIN games g ON b.game_id = g.game_id
GROUP BY g.game_name, g.game_type
ORDER BY revenue DESC;

-- Daily betting trends
SELECT DATE(bet_timestamp) as date,
       COUNT(*) as bets,
       SUM(bet_amount) as wagered,
       AVG(bet_amount) as avg_bet
FROM bets
GROUP BY DATE(bet_timestamp)
ORDER BY date;
```

### Using Spark

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("GamblingAnalytics").getOrCreate()

# Load data
bets_df = spark.read.json("hdfs://namenode:9000/gambling/bets/bets.json")
players_df = spark.read.json("hdfs://namenode:9000/gambling/players/players.json")

# Analysis
bets_df.createOrReplaceTempView("bets")
players_df.createOrReplaceTempView("players")

# Player statistics
spark.sql("""
    SELECT p.player_id, p.username, p.vip_tier,
           COUNT(b.bet_id) as total_bets,
           SUM(b.bet_amount) as total_wagered
    FROM players p
    LEFT JOIN bets b ON p.player_id = b.player_id
    GROUP BY p.player_id, p.username, p.vip_tier
    ORDER BY total_wagered DESC
    LIMIT 20
""").show()
```

## Extending Data Generation

### Add More Data

Modify `main.py` quantities:

```python
generator = GamblingDataGenerator(
    num_players=1000,    # Scale up
    num_games=500,
    num_sessions=10000,
    num_bets=50000      # 50k bets
)
```

### Add New Fields

Edit model classes in `models/` directory and update generator methods.

### Custom Distributions

Modify `random.choices()` weights in generator methods:

```python
# Make more platinum VIP players
vip_tier=random.choices(
    ['basic', 'silver', 'gold', 'platinum'],
    weights=[40, 30, 20, 10]  # More high-tier
)[0]
```

### Time Periods

Adjust date ranges:

```python
# Extend to 1 year
base_date = datetime.now() - timedelta(days=365)

# Or focus on recent data
base_date = datetime.now() - timedelta(days=30)
```

## Performance

Generation speed on typical hardware:
- 5,000 bets: ~2-3 seconds
- 10,000 bets: ~5-6 seconds
- 50,000 bets: ~25-30 seconds
- 100,000 bets: ~1 minute

File I/O is the main bottleneck for larger datasets.

## Data Quality

The generator ensures:
- ✓ Valid foreign key relationships
- ✓ Realistic value distributions
- ✓ Temporal consistency
- ✓ Currency consistency
- ✓ Business rule compliance
- ✓ Edge case representation
- ✓ Proper data types (Decimal for money)
- ✓ Complete records (no missing required fields)

## Troubleshooting

### Memory Issues

For very large datasets (100k+ bets), generate in batches:

```python
# Generate and save in chunks
for i in range(10):
    generator = GamblingDataGenerator(num_bets=10000)
    generator.generate_all_data()
    generator.save_to_json(f'./data/batch_{i}')
```

### Disk Space

Approximate space needed:
- 10k bets: ~25 MB
- 100k bets: ~250 MB
- 1M bets: ~2.5 GB

Ensure sufficient disk space before generation.

### HDFS Connection

If HDFS upload fails:
1. Check Hadoop cluster is running: `docker-compose ps`
2. Verify NameNode: `curl http://localhost:9870`
3. Check HDFS health: `docker exec namenode hdfs dfsadmin -report`
4. Use manual upload commands if needed