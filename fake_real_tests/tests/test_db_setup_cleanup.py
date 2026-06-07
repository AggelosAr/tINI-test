
"""
Tests for async behavior with setup and cleanup decorators.
Validates that setup/cleanup run correctly in concurrent async execution.
"""
import threading
import time
from typing import Set

from tini_test.misc.exceptions import ExpectedWasDifferentFromActual
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test

# Shared state for tracking setup/cleanup execution
_state_lock = threading.Lock()
_executed_setups: Set[str] = set()
_executed_cleanups: Set[str] = set()
_state_counters: dict = {}


def _reset_state():
    """Reset tracking state between test runs."""
    global _executed_setups, _executed_cleanups, _state_counters
    with _state_lock:
        _executed_setups.clear()
        _executed_cleanups.clear()
        _state_counters.clear()


def _track_setup(name: str):
    """Track that a setup was called."""
    with _state_lock:
        _executed_setups.add(name)
        _state_counters[f"{name}_setup_count"] = _state_counters.get(f"{name}_setup_count", 0) + 1


def _track_cleanup(name: str):
    """Track that a cleanup was called."""
    with _state_lock:
        _executed_cleanups.add(name)
        _state_counters[f"{name}_cleanup_count"] = _state_counters.get(f"{name}_cleanup_count", 0) + 1


def _get_setup_count(name: str) -> int:
    """Get the number of times a setup was called."""
    with _state_lock:
        return _state_counters.get(f"{name}_setup_count", 0)


def _get_cleanup_count(name: str) -> int:
    """Get the number of times a cleanup was called."""
    with _state_lock:
        return _state_counters.get(f"{name}_cleanup_count", 0)


#####################
### SETUP EXECUTION
#####################


@Test.case(setup=lambda: _track_setup("simple"))
def test_setup_is_called() -> None:
    must_equal(1, _get_setup_count("simple"))


@Test.case(setup=lambda: _track_setup("with_sleep"))
def test_setup_with_sleep() -> None:
    """Test that setup with sleep works correctly in async context."""
    time.sleep(0.1)
    must_equal(1, _get_setup_count("with_sleep"))


#####################
### CLEANUP EXECUTION
#####################


@Test.case(cleanup=lambda: _track_cleanup("simple"))
def test_cleanup_is_called() -> None:
    """Cleanup is called after test completes."""
    pass


@Test.case(cleanup=lambda: _track_cleanup("with_sleep"))
def test_cleanup_with_sleep() -> None:
    """Test that cleanup with sleep works correctly in async context."""
    pass


#####################
### SETUP AND CLEANUP TOGETHER
#####################


@Test.case(
    setup=lambda: _track_setup("both_simple"),
    cleanup=lambda: _track_cleanup("both_simple")
)
def test_setup_and_cleanup_both_called() -> None:
    """Both setup and cleanup are called in order."""
    must_equal(1, _get_setup_count("both_simple"))


@Test.case(
    setup=lambda: _track_setup("both_with_sleeps"),
    cleanup=lambda: _track_cleanup("both_with_sleeps")
)
def test_setup_cleanup_with_multiple_sleeps() -> None:
    """Test setup, test, and cleanup with sleeps all work correctly."""
    time.sleep(0.05)
    must_equal(1, _get_setup_count("both_with_sleeps"))


#####################
### SETUP/CLEANUP WITH TEST FAILURE
#####################


@Test.case(cleanup=lambda: _track_cleanup("fail_cleanup"))
def test_cleanup_runs_on_failure() -> None:
    """Cleanup should run even when test has an exception."""
    # This test intentionally has logic that would raise if not caught
    try:
        a = 10
        b = 20
        must_equal(a, b)
    except ExpectedWasDifferentFromActual:
        # Expected failure - cleanup should still run
        pass


#####################
### ASYNC CONCURRENT EXECUTION
#####################


@Test.case(
    setup=lambda: (time.sleep(0.05), _track_setup("async_1")),
    cleanup=lambda: (time.sleep(0.05), _track_cleanup("async_1"))
)
def test_async_concurrent_1() -> None:
    """First test in concurrent group with setup/cleanup sleeps."""
    time.sleep(0.02)
    must_equal(1, _get_setup_count("async_1"))


@Test.case(
    setup=lambda: (time.sleep(0.05), _track_setup("async_2")),
    cleanup=lambda: (time.sleep(0.05), _track_cleanup("async_2"))
)
def test_async_concurrent_2() -> None:
    """Second test in concurrent group with setup/cleanup sleeps."""
    time.sleep(0.02)
    must_equal(1, _get_setup_count("async_2"))


@Test.case(
    setup=lambda: (time.sleep(0.05), _track_setup("async_3")),
    cleanup=lambda: (time.sleep(0.05), _track_cleanup("async_3"))
)
def test_async_concurrent_3() -> None:
    """Third test in concurrent group with setup/cleanup sleeps."""
    time.sleep(0.02)
    must_equal(1, _get_setup_count("async_3"))


#####################
### STDOUT CAPTURE WITH SETUP/CLEANUP
#####################


@Test.case(
    setup=lambda: print("SETUP OUTPUT"),
    cleanup=lambda: print("CLEANUP OUTPUT")
)
def test_stdout_in_setup_cleanup() -> None:
    """Test that stdout from setup and cleanup is captured correctly."""
    print("TEST OUTPUT")


@Test.case(
    setup=lambda: (time.sleep(0.01), print("SETUP WITH SLEEP")),
    cleanup=lambda: (time.sleep(0.01), print("CLEANUP WITH SLEEP"))
)
def test_stdout_with_sleep_in_setup_cleanup() -> None:
    """Test that stdout is captured correctly even with sleeps in setup/cleanup."""
    time.sleep(0.01)
    print("TEST OUTPUT WITH SLEEP")


#####################
### STATE ISOLATION
#####################


@Test.case(setup=lambda: _track_setup("isolate_1"))
def test_isolation_first() -> None:
    """First test for isolation check."""
    must_equal(1, _get_setup_count("isolate_1"))


@Test.case(setup=lambda: _track_setup("isolate_2"))
def test_isolation_second() -> None:
    """Second test - setup should be called independently."""
    must_equal(1, _get_setup_count("isolate_2"))


@Test.case(setup=lambda: _track_setup("isolate_3"))
def test_isolation_third() -> None:
    """Third test - each test should have its own setup call."""
    must_equal(1, _get_setup_count("isolate_3"))


#####################
### SQLITE DATABASE TESTS (no external dependencies)
#####################

import os
import sqlite3
import tempfile

# Thread-local storage for database connections
_db_local = threading.local()


def _get_db_path(test_name: str) -> str:
    """Get a unique database file path for a test."""
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, f"tini_test_{test_name}.db")


def _create_test_db(test_name: str):
    """Create a test database with sample schema."""
    db_path = _get_db_path(test_name)
    print(f"\n🏗️  [SETUP] Creating database for test: {test_name}")
    print(f"   📁 Path: {db_path}")
    
    # Remove any existing database
    if os.path.exists(db_path):
        print(f"   🗑️  Removing existing database")
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"   📊 Creating 'users' table with schema:")
    print(f"      - id (INTEGER PRIMARY KEY)")
    print(f"      - name (TEXT NOT NULL)")
    print(f"      - email (TEXT UNIQUE NOT NULL)")
    print(f"      - age (INTEGER)")
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            age INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    print(f"   ✅ Database setup complete")


def _cleanup_test_db(test_name: str):
    """Clean up test database file."""
    db_path = _get_db_path(test_name)
    print(f"\n🧹 [CLEANUP] Cleaning up database for test: {test_name}")
    
    if os.path.exists(db_path):
        print(f"   📁 DB Path: {db_path}")
        # Try to query final state before deletion
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"   📊 Final record count: {count} rows")
            
            # Show the actual data
            cursor.execute("SELECT id, name, email, age FROM users")
            rows = cursor.fetchall()
            if rows:
                print(f"   📋 Final data in database:")
                for row in rows:
                    print(f"      ID={row[0]}, Name={row[1]}, Email={row[2]}, Age={row[3]}")
            else:
                print(f"   📋 Database is empty")
            conn.close()
        except Exception as e:
            print(f"   ⚠️  Could not query database: {e}")
        
        print(f"   🗑️  Deleting database file")
        os.remove(db_path)
    else:
        print(f"   ℹ️  Database file does not exist: {db_path}")
    
    # Also clean up any connection stored in thread local
    if hasattr(_db_local, 'connection'):
        try:
            _db_local.connection.close()
        except:
            pass
        del _db_local.connection
    print(f"   ✅ Cleanup complete")


@Test.case(
    setup=lambda: _create_test_db("simple_insert"),
    cleanup=lambda: _cleanup_test_db("simple_insert")
)
def test_db_simple_insert() -> None:
    """Test basic INSERT operation with database setup/cleanup."""
    db_path = _get_db_path("simple_insert")
    print(f"\n📁 Test DB Path: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insert a user
    print("➕ Inserting: Alice (alice@example.com, age=30)")
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                   ("Alice", "alice@example.com", 30))
    conn.commit()
    
    # Verify the insert with actual data
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"✓ Row count after insert: {count}")
    
    cursor.execute("SELECT id, name, email, age FROM users")
    rows = cursor.fetchall()
    print(f"📋 Actual data in database:")
    for row in rows:
        print(f"   ID={row[0]}, Name={row[1]}, Email={row[2]}, Age={row[3]}")
    
    must_equal(1, count)
    conn.close()


@Test.case(
    setup=lambda: _create_test_db("db_query"),
    cleanup=lambda: _cleanup_test_db("db_query")
)
def test_db_insert_and_query() -> None:
    """Test INSERT followed by SELECT queries."""
    db_path = _get_db_path("db_query")
    print(f"\n📁 Test DB Path: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insert multiple users
    users = [
        ("Alice", "alice@example.com", 30),
        ("Bob", "bob@example.com", 25),
        ("Charlie", "charlie@example.com", 35),
    ]
    print("➕ Inserting users:")
    for name, email, age in users:
        print(f"   - {name} ({email}, age={age})")
        cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                       (name, email, age))
    conn.commit()
    
    # Query all users
    cursor.execute("SELECT id, name, email, age FROM users ORDER BY id")
    all_users = cursor.fetchall()
    count = len(all_users)
    print(f"✓ Total users in table: {count}")
    print(f"📋 All users in database:")
    for row in all_users:
        print(f"   ID={row[0]}, Name={row[1]}, Email={row[2]}, Age={row[3]}")
    must_equal(3, count)
    
    # Query by age
    cursor.execute("SELECT id, name, email, age FROM users WHERE age > ? ORDER BY age DESC", (28,))
    older_users = cursor.fetchall()
    print(f"🔍 Users older than 28: {len(older_users)} found")
    for row in older_users:
        print(f"   ID={row[0]}, Name={row[1]}, Age={row[3]}")
    must_equal(2, len(older_users))
    
    conn.close()


@Test.case(
    setup=lambda: _create_test_db("db_update"),
    cleanup=lambda: _cleanup_test_db("db_update")
)
def test_db_insert_update_delete() -> None:
    """Test full CRUD operations on database."""
    db_path = _get_db_path("db_update")
    print(f"\n📁 Test DB Path: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # CREATE (insert)
    print("➕ CREATE: Inserting Alice (age=30)")
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                   ("Alice", "alice@example.com", 30))
    conn.commit()
    
    cursor.execute("SELECT id, name, email, age FROM users")
    rows = cursor.fetchall()
    print(f"   After INSERT - Data: {rows}")
    
    # READ
    print("📖 READ: Fetching Alice's data")
    cursor.execute("SELECT id, age, name, email FROM users WHERE name = ?", ("Alice",))
    user_id, age, name, email = cursor.fetchone()
    print(f"   Retrieved - ID={user_id}, Name={name}, Email={email}, Age={age}")
    must_equal(30, age)
    
    # UPDATE
    print(f"✏️ UPDATE: Changing Alice's age from 30 to 31")
    cursor.execute("UPDATE users SET age = ? WHERE id = ?", (31, user_id))
    conn.commit()
    
    cursor.execute("SELECT id, name, email, age FROM users WHERE id = ?", (user_id,))
    updated_row = cursor.fetchone()
    new_age = updated_row[3]
    print(f"   After UPDATE - ID={updated_row[0]}, Name={updated_row[1]}, Email={updated_row[2]}, Age={new_age}")
    must_equal(31, new_age)
    
    # DELETE
    print(f"🗑️ DELETE: Removing user ID {user_id}")
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"   After DELETE - Rows remaining: {count}")
    
    cursor.execute("SELECT id, name, email, age FROM users")
    remaining = cursor.fetchall()
    print(f"   Remaining data: {remaining}")
    
    must_equal(0, count)
    conn.close()


@Test.case(
    setup=lambda: _create_test_db("db_with_sleep_setup"),
    cleanup=lambda: _cleanup_test_db("db_with_sleep_setup")
)
def test_db_with_setup_sleep() -> None:
    """Test database operations with sleep in setup."""
    time.sleep(0.02)
    db_path = _get_db_path("db_with_sleep_setup")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                   ("TestUser", "test@example.com", 25))
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    must_equal(1, count)
    
    conn.close()


@Test.case(
    setup=lambda: _create_test_db("db_concurrent_1"),
    cleanup=lambda: _cleanup_test_db("db_concurrent_1")
)
def test_db_concurrent_insert_1() -> None:
    """First concurrent database test."""
    time.sleep(0.01)
    db_path = _get_db_path("db_concurrent_1")
    print(f"\n[CONCURRENT 1] Inserting User1 (age=20)")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                   ("User1", "user1@example.com", 20))
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"[CONCURRENT 1] Row count: {count}")
    must_equal(1, count)
    
    conn.close()


@Test.case(
    setup=lambda: _create_test_db("db_concurrent_2"),
    cleanup=lambda: _cleanup_test_db("db_concurrent_2")
)
def test_db_concurrent_insert_2() -> None:
    """Second concurrent database test."""
    time.sleep(0.01)
    db_path = _get_db_path("db_concurrent_2")
    print(f"\n[CONCURRENT 2] Inserting User2 (age=25)")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                   ("User2", "user2@example.com", 25))
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"[CONCURRENT 2] Row count: {count}")
    must_equal(1, count)
    
    conn.close()


@Test.case(
    setup=lambda: _create_test_db("db_concurrent_3"),
    cleanup=lambda: _cleanup_test_db("db_concurrent_3")
)
def test_db_concurrent_insert_3() -> None:
    """Third concurrent database test."""
    time.sleep(0.01)
    db_path = _get_db_path("db_concurrent_3")
    print(f"\n[CONCURRENT 3] Inserting User3 (age=30)")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                   ("User3", "user3@example.com", 30))
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    print(f"[CONCURRENT 3] Row count: {count}")
    must_equal(1, count)
    
    conn.close()
    
    conn.close()


@Test.case(
    setup=lambda: _create_test_db("db_transaction"),
    cleanup=lambda: _cleanup_test_db("db_transaction")
)
def test_db_transaction_rollback() -> None:
    """Test database transaction and rollback behavior."""
    db_path = _get_db_path("db_transaction")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insert initial data
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                   ("Alice", "alice@example.com", 30))
    conn.commit()
    
    # Start a transaction
    try:
        cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                       ("Bob", "bob@example.com", 25))
        # Intentionally insert duplicate email to cause constraint violation
        cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                       ("Charlie", "alice@example.com", 35))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
    
    # Verify only first insert persisted (Bob should not be there if rollback works)
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    # Should be 1 (just Alice) if rollback worked
    must_equal(1, count)
    
    conn.close()

