#!/usr/bin/env python
"""
Kafka Producer for Gambling Platform Real-Time Events
Streams bets, transactions, and player events to Kafka topics
"""
import json
import time
import random
from datetime import datetime
from decimal import Decimal
from confluent_kafka import Producer
from confluent_kafka import KafkaException

# Import our data models
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models import Bet, Transaction, Event


# Simplified random ID generators
_bet_counter = 0
_transaction_counter = 0
_event_counter = 0


def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def create_producer(bootstrap_servers='localhost:9093'):
    """Create and return a Kafka producer"""
    try:
        conf = {
            'bootstrap.servers': bootstrap_servers,
            'client.id': 'gambling-producer',
            'acks': 'all',
            'retries': 3,
            'max.in.flight.requests.per.connection': 1
        }
        producer = Producer(conf)
        return producer
    except KafkaException as e:
        print("Error: Cannot connect to Kafka broker")
        print(f"Make sure Kafka is running at {bootstrap_servers}")
        print(f"Error: {e}")
        return None


def generate_bet_event():
    """Generate a random bet event"""
    global _bet_counter
    _bet_counter += 1

    bet_amount = Decimal(str(round(random.uniform(1.0, 100.0), 2)))
    is_won = random.random() < 0.45

    if is_won:
        multiplier = Decimal(str(round(random.uniform(1.2, 10.0), 2)))
        payout = bet_amount * multiplier
        is_jackpot = random.random() < 0.001
        if is_jackpot:
            payout = Decimal(str(round(random.uniform(10000, 100000), 2)))
    else:
        payout = Decimal('0.00')
        multiplier = None
        is_jackpot = False

    bet = Bet(
        bet_id=f"BK{_bet_counter:08d}",
        player_id=f"P{random.randint(1, 200):06d}",
        game_id=f"G{random.randint(1, 100):06d}",
        session_id=f"S{random.randint(1, 1000):06d}",
        bet_amount=bet_amount,
        bet_status='won' if is_won else 'lost',
        payout_amount=payout,
        win_multiplier=multiplier,
        is_jackpot=is_jackpot
    )

    return {
        'event_type': 'bet',
        'timestamp': datetime.utcnow(),
        'data': bet.to_dict()
    }


def generate_transaction_event():
    """Generate a random transaction event"""
    global _transaction_counter
    _transaction_counter += 1

    transaction_type = random.choice(['deposit', 'withdrawal', 'bonus', 'refund'])
    amount = Decimal(str(round(random.uniform(10.0, 1000.0), 2)))

    transaction = Transaction(
        transaction_id=f"TK{_transaction_counter:08d}",
        player_id=f"P{random.randint(1, 200):06d}",
        transaction_type=transaction_type,
        amount=amount,
        currency='USD',
        status=random.choice(['completed', 'pending', 'failed']),
        payment_method=random.choice(['credit_card', 'bank_transfer', 'ewallet', 'crypto'])
    )

    return {
        'event_type': 'transaction',
        'timestamp': datetime.utcnow(),
        'data': transaction.to_dict()
    }


def generate_player_event():
    """Generate a random player activity event"""
    global _event_counter
    _event_counter += 1

    event_types = ['login', 'logout', 'game_start', 'game_end', 'bonus_claimed', 'level_up']
    categories = ['authentication', 'gameplay', 'promotion', 'progression']

    event = Event(
        event_id=f"EK{_event_counter:08d}",
        player_id=f"P{random.randint(1, 200):06d}",
        event_type=random.choice(event_types),
        event_category=random.choice(categories),
        event_timestamp=datetime.utcnow()
    )

    return {
        'event_type': 'player_activity',
        'timestamp': datetime.utcnow(),
        'data': event.to_dict()
    }


def stream_events(producer, duration_seconds=60, events_per_second=10):
    """
    Stream events to Kafka topics

    Args:
        producer: KafkaProducer instance
        duration_seconds: How long to stream (default 60 seconds)
        events_per_second: Rate of event generation (default 10/sec)
    """
    print(f"=== Streaming events to Kafka ===")
    print(f"Duration: {duration_seconds} seconds")
    print(f"Rate: {events_per_second} events/second")
    print(f"Total events: {duration_seconds * events_per_second}")
    print()

    start_time = time.time()
    event_count = {'bets': 0, 'transactions': 0, 'player_activity': 0}

    try:
        while time.time() - start_time < duration_seconds:
            # Generate random event type with weighted probability
            event_type = random.choices(
                ['bet', 'transaction', 'player_activity'],
                weights=[0.6, 0.2, 0.2],  # 60% bets, 20% transactions, 20% player activity
                k=1
            )[0]

            # Generate and send event
            if event_type == 'bet':
                event = generate_bet_event()
                topic = 'gambling-bets'
                key = event['data']['bet_id']
                event_count['bets'] += 1
            elif event_type == 'transaction':
                event = generate_transaction_event()
                topic = 'gambling-transactions'
                key = event['data']['transaction_id']
                event_count['transactions'] += 1
            else:
                event = generate_player_event()
                topic = 'gambling-player-activity'
                key = event['data']['event_id']
                event_count['player_activity'] += 1

            # Send to Kafka
            producer.produce(
                topic,
                key=key.encode('utf-8'),
                value=json.dumps(event, default=json_serializer).encode('utf-8')
            )
            producer.poll(0)  # Trigger delivery callbacks

            # Print progress every 100 events
            total_events = sum(event_count.values())
            if total_events % 100 == 0:
                elapsed = time.time() - start_time
                rate = total_events / elapsed if elapsed > 0 else 0
                print(f"Sent {total_events} events ({rate:.1f}/sec) - "
                      f"Bets: {event_count['bets']}, "
                      f"Transactions: {event_count['transactions']}, "
                      f"Player Activity: {event_count['player_activity']}")

            # Sleep to maintain rate
            time.sleep(1.0 / events_per_second)

    except KeyboardInterrupt:
        print("\nStopped by user")

    # Flush and close
    producer.flush()

    print()
    print("=== Streaming Complete ===")
    print(f"Total events sent: {sum(event_count.values())}")
    print(f"  Bets: {event_count['bets']}")
    print(f"  Transactions: {event_count['transactions']}")
    print(f"  Player Activity: {event_count['player_activity']}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Stream gambling events to Kafka')
    parser.add_argument('--broker', default='localhost:9093',
                        help='Kafka broker address (default: localhost:9093)')
    parser.add_argument('--duration', type=int, default=60,
                        help='Duration in seconds (default: 60)')
    parser.add_argument('--rate', type=int, default=10,
                        help='Events per second (default: 10)')

    args = parser.parse_args()

    # Create producer
    print(f"Connecting to Kafka at {args.broker}...")
    producer = create_producer(args.broker)

    if not producer:
        print("Failed to create Kafka producer. Exiting.")
        return 1

    print("Connected successfully!")
    print()

    # Stream events
    stream_events(producer, args.duration, args.rate)

    # Producer is already flushed in stream_events
    return 0


if __name__ == '__main__':
    sys.exit(main())
