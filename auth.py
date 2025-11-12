import bcrypt
from db_connection import create_connection

def register_user(username: str, password: str, email: str | None = None):
    conn = create_connection()
    if conn is None:
        return False, "Database connection failed"

    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cur.fetchone():
            return False, "Username already exists"

        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cur.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
            (username, pw_hash, email)
        )
        conn.commit()
        return True, "Account created successfully"
    finally:
        cur.close()
        conn.close()


def authenticate_user(username: str, password: str):
    conn = create_connection()
    if conn is None:
        return False, "Database connection failed"

    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        if not user:
            return False, "User not found"

        stored_hash = user["password_hash"].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return True, user
        else:
            return False, "Invalid password"
    finally:
        cur.close()
        conn.close()
