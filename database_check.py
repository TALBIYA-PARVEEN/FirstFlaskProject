import sqlite3

conn = sqlite3.connect('instance/careernest.db')
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

# Show structure of a table
cursor.execute("PRAGMA table_info(users);")
print(cursor.fetchall())