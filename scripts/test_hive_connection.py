#!/usr/bin/env python
"""
Test Hive connection and troubleshoot connection issues
"""
import sys
import time
import socket


def test_port_connection(host='127.0.0.1', port=10000, timeout=5):
    """Test if port is accessible"""
    print(f"Testing connection to {host}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            print(f"✓ Port {port} is open and accessible")
            return True
        else:
            print(f"✗ Port {port} is not accessible (error code: {result})")
            return False
    except socket.error as e:
        print(f"✗ Socket error: {e}")
        return False


def test_hive_with_pyhive():
    """Test Hive connection using PyHive"""
    print("\nTesting Hive connection with PyHive...")
    try:
        from pyhive import hive

        print("  Connecting to Hive server...")
        conn = hive.Connection(
            host='localhost',
            port=10000,
            username='hive',
            database='default',
            auth='NONE'
        )

        cursor = conn.cursor()
        cursor.execute('SHOW DATABASES')
        databases = cursor.fetchall()

        print(f"✓ Connected successfully!")
        print(f"  Databases: {[db[0] for db in databases]}")

        cursor.close()
        conn.close()
        return True

    except ImportError:
        print("✗ PyHive not installed")
        print("  Install with: pip install pyhive thrift sasl thrift_sasl")
        return False
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Wait 2-3 minutes after starting Hadoop cluster")
        print("  2. Check Hive server logs: docker logs hive-server --tail 50")
        print("  3. Restart Hive: docker-compose restart hive-server hive-metastore")
        return False


def test_hive_with_beeline():
    """Test Hive using beeline CLI"""
    print("\nTesting Hive using beeline (inside container)...")
    import subprocess

    try:
        result = subprocess.run(
            ['docker', 'exec', 'hive-server', 'beeline', '-u',
             'jdbc:hive2://localhost:10000', '-e', 'SHOW DATABASES;'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            print("✓ Beeline connection successful!")
            print(f"  Output: {result.stdout[:200]}")
            return True
        else:
            print(f"✗ Beeline failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("✗ Beeline command timed out")
        return False
    except Exception as e:
        print(f"✗ Error running beeline: {e}")
        return False


def check_hive_metastore():
    """Check if Hive metastore is accessible"""
    print("\nChecking Hive Metastore (port 9083)...")
    return test_port_connection(host='127.0.0.1', port=9083)


def main():
    """Run all connection tests"""
    print("=" * 60)
    print("  Hive Connection Troubleshooting")
    print("=" * 60)

    results = {}

    # Test 1: Port accessibility
    results['port_10000'] = test_port_connection('127.0.0.1', 10000)

    # Test 2: Metastore
    results['metastore'] = check_hive_metastore()

    # Test 3: Beeline
    results['beeline'] = test_hive_with_beeline()

    # Test 4: PyHive
    results['pyhive'] = test_hive_with_pyhive()

    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)

    for test, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test}")

    print("\n" + "=" * 60)

    if all(results.values()):
        print("All tests passed! Hive is ready to use.")
        return 0
    else:
        print("\nSome tests failed. Recommendations:")

        if not results['port_10000']:
            print("\n1. Port 10000 not accessible:")
            print("   - Check if Hadoop cluster is running: docker-compose ps")
            print("   - Check firewall settings")
            print("   - Try: docker-compose restart hive-server")

        if not results['metastore']:
            print("\n2. Metastore not accessible:")
            print("   - Check: docker logs hive-metastore")
            print("   - Try: docker-compose restart hive-metastore hive-metastore-postgresql")

        if not results['beeline']:
            print("\n3. Beeline connection failed:")
            print("   - Wait 2-3 minutes after starting cluster")
            print("   - Check: docker logs hive-server")

        if not results['pyhive']:
            print("\n4. PyHive connection failed:")
            print("   - Install PyHive: pip install pyhive thrift sasl thrift_sasl")
            print("   - Alternative: Use Hue web interface at http://localhost:8888")

        return 1


if __name__ == '__main__':
    sys.exit(main())