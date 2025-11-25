#!/usr/bin/env python
"""
Kafka Consumer for Gambling Platform Real-Time Events
Consumes and processes events from Kafka topics
"""
import json
import signal
import sys
from collections import defaultdict
from datetime import datetime
from confluent_kafka import Consumer, KafkaException
from confluent_kafka import KafkaError


class GracefulKiller:
    """Handle graceful shutdown"""
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args):
        self.kill_now = True


def create_consumer(topics, bootstrap_servers='localhost:9093', group_id='gambling-consumer'):
    """Create and return a Kafka consumer"""
    try:
        conf = {
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True,
            'client.id': 'gambling-consumer'
        }
        consumer = Consumer(conf)
        consumer.subscribe(topics)
        return consumer
    except KafkaException as e:
        print("Error: Cannot connect to Kafka broker")
        print(f"Make sure Kafka is running at {bootstrap_servers}")
        print(f"Error: {e}")
        return None


def process_bet_event(event):
    """Process a bet event"""
    data = event['data']
    return {
        'type': 'BET',
        'id': data['bet_id'],
        'player': data['player_id'],
        'amount': data['bet_amount'],
        'status': data['bet_status'],
        'game': data['game_id']
    }


def process_transaction_event(event):
    """Process a transaction event"""
    data = event['data']
    return {
        'type': 'TRANSACTION',
        'id': data['transaction_id'],
        'player': data['player_id'],
        'type_detail': data['transaction_type'],
        'amount': data['amount'],
        'status': data['status']
    }


def process_player_activity_event(event):
    """Process a player activity event"""
    data = event['data']
    return {
        'type': 'ACTIVITY',
        'id': data['event_id'],
        'player': data['player_id'],
        'action': data['event_type'],
        'category': data['event_category']
    }


def consume_events(consumer, max_messages=None):
    """
    Consume events from Kafka topics

    Args:
        consumer: KafkaConsumer instance
        max_messages: Maximum number of messages to consume (None for unlimited)
    """
    print("=== Kafka Consumer Started ===")
    print("Waiting for messages... (Ctrl+C to stop)")
    print()

    killer = GracefulKiller()
    stats = defaultdict(int)
    message_count = 0

    try:
        while not killer.kill_now:
            if max_messages and message_count >= max_messages:
                break

            # Poll for messages (1 second timeout)
            message = consumer.poll(1.0)

            if message is None:
                continue

            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer error: {message.error()}")
                    continue

            message_count += 1
            stats[message.topic()] += 1

            # Parse event
            event = json.loads(message.value().decode('utf-8'))

            # Process based on event type
            topic = message.topic()
            if 'bet' in topic:
                processed = process_bet_event(event)
            elif 'transaction' in topic:
                processed = process_transaction_event(event)
            elif 'activity' in topic:
                processed = process_player_activity_event(event)
            else:
                processed = {'type': 'UNKNOWN', 'data': event}

            # Print event (every 10th message to reduce output)
            if message_count % 10 == 0:
                key = message.key().decode('utf-8') if message.key() else 'None'
                print(f"[{message_count}] Topic: {topic:30s} | "
                      f"Key: {key:20s} | "
                      f"Type: {processed['type']:12s} | "
                      f"ID: {processed.get('id', 'N/A')}")

            # Print stats every 100 messages
            if message_count % 100 == 0:
                print()
                print(f"--- Stats (Total: {message_count}) ---")
                for topic, count in stats.items():
                    print(f"  {topic}: {count}")
                print()

    except KeyboardInterrupt:
        print("\nStopped by user")

    print()
    print("=== Consumer Stopped ===")
    print(f"Total messages consumed: {message_count}")
    print("\nMessages by topic:")
    for topic, count in stats.items():
        print(f"  {topic}: {count}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Consume gambling events from Kafka')
    parser.add_argument('--broker', default='localhost:9093',
                        help='Kafka broker address (default: localhost:9093)')
    parser.add_argument('--topics', nargs='+',
                        default=['gambling-bets', 'gambling-transactions', 'gambling-player-activity'],
                        help='Kafka topics to consume from')
    parser.add_argument('--group', default='gambling-consumer',
                        help='Consumer group ID (default: gambling-consumer)')
    parser.add_argument('--max-messages', type=int, default=None,
                        help='Maximum messages to consume (default: unlimited)')

    args = parser.parse_args()

    # Create consumer
    print(f"Connecting to Kafka at {args.broker}...")
    consumer = create_consumer(args.topics, args.broker, args.group)

    if not consumer:
        print("Failed to create Kafka consumer. Exiting.")
        return 1

    print("Connected successfully!")
    print()

    # Consume events
    consume_events(consumer, args.max_messages)

    # Close consumer
    consumer.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())
