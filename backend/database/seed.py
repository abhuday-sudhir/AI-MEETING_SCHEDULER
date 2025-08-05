import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    sender TEXT,
    message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

# Seed users
users = [
    ("Raj", "raj@example.com"),
    ("Aditi", "aditi@example.com"),
    ("John", "john@example.com"),
    ("Sarah", "sarah@example.com"),
    ("Mike", "mike@example.com"),
    ("Lisa", "lisa@example.com"),
    ("David", "david@example.com"),
    ("Emma", "emma@example.com")
]
for name, email in users:
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    except:
        continue

# Seed chats for Raj (user_id = 1)
chats_raj = [
    (1, "Raj", "Hey team 👋"),
    (1, "Aditi", "Hi Raj!"),
    (1, "Raj", "Let's meet tomorrow at 3 PM"),
    (1, "John", "Sounds good"),
    (1, "Raj", "Aditi and John, please join")
]

# Seed chats for Sarah (user_id = 2)
chats_sarah = [
    (2, "Sarah", "Good morning everyone! 🌅"),
    (2, "Mike", "Morning Sarah!"),
    (2, "Lisa", "Hi there!"),
    (2, "Sarah", "I've scheduled our weekly meeting for Friday at 10 AM"),
    (2, "Mike", "Perfect, I'll be there"),
    (2, "Lisa", "Count me in too"),
    (2, "Sarah", "Great! We'll discuss the Q4 strategy")
]

# Seed chats for Marketing Team (user_id = 3)
chats_marketing = [
    (3, "David", "Marketing team standup in 5 minutes"),
    (3, "Emma", "I'll join from the conference room"),
    (3, "David", "We need to discuss the new campaign launch"),
    (3, "Emma", "I have the presentation ready"),
    (3, "David", "Perfect! Let's meet in the main conference room"),
    (3, "Emma", "I'll bring the latest analytics data"),
    (3, "David", "Great! This will be our weekly standup discussion")
]

# Insert all chats
all_chats = chats_raj + chats_sarah + chats_marketing
for user_id, sender, message in all_chats:
    cursor.execute("INSERT INTO chats (user_id, sender, message) VALUES (?, ?, ?)", (user_id, sender, message))

conn.commit()
conn.close()
