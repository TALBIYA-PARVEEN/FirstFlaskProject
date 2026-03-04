import sqlite3

conn = sqlite3.connect("instance/careernest.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO users (email,password_hash,role,is_active,is_approved,is_blacklisted)
VALUES (?,?,?,?,?,?)
""", (
    'admin@gmail.com',
    '$2b$12$WJyuVah6a7mPJZ6CBSNr.e9w6rvKV1dqcsmc9T8sKyN1XuoX9.h16',
    'admin',
    1,
    1,
    0
))

conn.commit()
conn.close()

print("Admin inserted successfully!")