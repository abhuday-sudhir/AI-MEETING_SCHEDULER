import sqlite3

DB_PATH = "database/users.db"

def get_chat_by_user_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sender, message FROM chats WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"sender": sender, "message": message} for sender, message in rows]

def resolve_emails(names):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    emails = {}
    for name in names:
        cursor.execute("SELECT email FROM users WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            emails[name] = result[0]
    conn.close()
    return emails
