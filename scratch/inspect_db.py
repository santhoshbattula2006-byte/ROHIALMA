import sqlite3

conn = sqlite3.connect('backend/test_agrimitra.db')
cursor = conn.cursor()

tables = [row[0] for row in cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
print("=== DATABASE TABLES CREATED BY ALEMBIC MIGRATION ===")
for t in sorted(tables):
    print(f" - {t}")

print("\n=== SAMPLE CONSTRAINTS & INDEXES ===")
for t in ["locations", "soil_profiles", "soil_default_dataset_records", "farmer_profiles"]:
    indexes = cursor.execute(f"PRAGMA index_list({t});").fetchall()
    print(f"\nTable '{t}' Indexes & Unique Constraints:")
    for idx in indexes:
        print(f"   * Index: {idx[1]} | Unique: {bool(idx[2])}")
