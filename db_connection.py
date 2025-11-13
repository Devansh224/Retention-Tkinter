import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",        
    "password": "", 
    "database": "retention"
}


def create_database_if_not_exists():
    """Create the database if it doesn't exist"""
    try:
        # Connect without specifying database
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"Database '{DB_CONFIG['database']}' is ready.")
        
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error creating database: {e}")
        return False


def create_connection():
    try:
        # why "**" - unpacks the dictionary into keyword arguments
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error:
        return None

conn = None
cursor = None

def initialise_db():
    global conn, cursor
    
    # First, ensure the database exists
    if not create_database_if_not_exists():
        print("Failed to create/access database.")
        return
    
    # Now connect to the database
    conn = create_connection()
    if conn is None:
        print(f"Could not connect to '{DB_CONFIG['database']}' database.")
        return

    cursor = conn.cursor()
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        email VARCHAR(100),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Subjects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        name VARCHAR(50) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)
    # Chapters table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chapters (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        subject_id INT NOT NULL,
        name VARCHAR(100) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    )
    """)

    # Flashcards table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flashcards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subject_id INT NOT NULL,
    chapter_id INT,
    front TEXT NOT NULL,
    back TEXT NOT NULL,
    tags VARCHAR(100),
    next_review_date DATETIME NOT NULL,            
    review_interval INT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE
);

    """)

    # Tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        subject_id INT,
        chapter_id INT,
        linked_flashcards TEXT,
        due_date DATETIME,
        completed BOOLEAN DEFAULT FALSE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
        FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE               
    )
    """)

    # Exams table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exams (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        subject_id INT NOT NULL,
        exam_date DATE NOT NULL,
        description VARCHAR(255),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
    )
    """)

    # Scheduler table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scheduler (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        flashcard_id INT NOT NULL,
        next_revision DATETIME NOT NULL,
        revision_count INT DEFAULT 0,
        done BOOLEAN DEFAULT FALSE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("All tables initialised successfully!")

def close_connection(con, cur):
    if cur:
        cur.close()
    if con:
        con.close()

if __name__ == "__main__":
    initialise_db()