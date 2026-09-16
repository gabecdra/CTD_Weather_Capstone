import sqlite3
import os
import pandas as pd

print("=" * 60)
print("🔍 DATABASE DIAGNOSTIC")
print("=" * 60)

# 1. Where are we?
print(f"\n1. Current directory: {os.getcwd()}")

# 2. What files exist?
print(f"\n2. Files in directory:")
for f in os.listdir('.'):
    if not f.startswith('.'):
        print(f"   - {f}")

# 3. Find all .db files
print(f"\n3. Database files found:")
db_files = [f for f in os.listdir('.') if f.endswith('.db')]
if db_files:
    for db in db_files:
        size = os.path.getsize(db)
        print(f"   - {db} ({size} bytes)")
else:
    print("   ❌ No .db files found in current directory!")

# 4. Try to open each database
for db_file in db_files:
    print(f"\n4. Checking database: {db_file}")
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"   Tables: {[t[0] for t in tables]}")
        
        # Check each table
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   - {table_name}: {count} rows")
            
            # Get columns
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"     Columns: {[c[1] for c in columns]}")
        
        conn.close()
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
