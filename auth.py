import bcrypt
from db_connection import create_connection

# CRUD Features for User Authentication

# 1- User Registration

'''
- attribute: DATATYPE - tells the compiler that the content must be of this type
- As we are keeping email optional, we use str | None which means it can be string or None
'''
def register_user(username: str, password: str, email: str | None = None):
    conn = create_connection()
    if conn is None:
        return False, "Database connection failed"

    # normally when fetching we will get a tuple, but dictionary=True gives us a dict
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cur.fetchone():
            return False, "Username already exists"

        '''
        - password.encode("utf-8") → converts string to bytes (bcrypt works on bytes).
        - bcrypt.gensalt() → generates a random salt (random piece of data).
        - bcrypt.hashpw() → hashes the password with that salt.
        - .decode("utf-8") → converts the hash back to a string so it can be stored in the DB.
        '''

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


def authenticate_user(identifier: str, password: str):
    """
    Authenticate a user by either username or email.
    identifier: can be username OR email
    password: plain text password entered by user
    """
    conn = create_connection()
    if conn is None:
        return False, "Database connection failed"

    cur = conn.cursor(dictionary=True)
    try:
        # Match either username or email
        # we use %s as a placeholder
        cur.execute("SELECT * FROM users WHERE username=%s OR email=%s", (identifier, identifier))
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