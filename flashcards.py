from datetime import datetime, timedelta
from db_connection import create_connection

# 1) Add a new flashcard: due immediately (NOW)
def add_flashcard(user_id: int, subject_id: int, chapter_id: int, front: str, back: str, tags: str = None):
    conn = create_connection(); cur = conn.cursor()
    cur.execute("""
        INSERT INTO flashcards (user_id, subject_id, chapter_id, front, back, tags, next_review_date, review_interval)
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), 0)
    """, (user_id, subject_id, chapter_id, front, back, tags))
    conn.commit(); cur.close(); conn.close(); return True

# 2) Get flashcards for subject/chapter
def get_flashcards(user_id: int, subject_id: int, chapter_id: int = None):
    conn = create_connection(); cur = conn.cursor()
    if chapter_id:
        cur.execute("""
            SELECT id, front, back, next_review_date
            FROM flashcards
            WHERE user_id=%s AND subject_id=%s AND chapter_id=%s
        """, (user_id, subject_id, chapter_id))
    else:
        cur.execute("""
            SELECT id, front, back, next_review_date
            FROM flashcards
            WHERE user_id=%s AND subject_id=%s
        """, (user_id, subject_id))
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows

# 3) Get flashcards due now (timestamp-aware)
def get_due_flashcards(user_id, subject_id=None, chapter_id=None):
    conn = create_connection(); cur = conn.cursor()
    if subject_id and chapter_id:
        cur.execute("""
            SELECT id, front, back, next_review_date
            FROM flashcards
            WHERE user_id=%s AND subject_id=%s AND chapter_id=%s
              AND next_review_date <= NOW()
            ORDER BY next_review_date
        """, (user_id, subject_id, chapter_id))
    elif subject_id:
        cur.execute("""
            SELECT id, front, back, next_review_date
            FROM flashcards
            WHERE user_id=%s AND subject_id=%s
              AND next_review_date <= NOW()
            ORDER BY next_review_date
        """, (user_id, subject_id))
    else:
        cur.execute("""
            SELECT id, front, back, next_review_date
            FROM flashcards
            WHERE user_id=%s AND next_review_date <= NOW()
            ORDER BY next_review_date
        """, (user_id,))
    rows = cur.fetchall(); cur.close(); conn.close()
    return rows


# 4) Update review outcome (skip -> +1 hour, others -> days)
def update_flashcard_review(card_id: int, outcome: str):
    intervals = {
        "forgot": timedelta(days=1),
        "partial": timedelta(days=2),
        "effort": timedelta(days=3),
        "easy": timedelta(days=5),
        "skip": timedelta(hours=1)
    }
    interval = intervals.get(outcome)
    if interval is None:
        return

    next_dt = datetime.now() + interval
    interval_days = interval.days

    conn = create_connection(); cur = conn.cursor()
    cur.execute("""
        UPDATE flashcards
        SET review_interval=%s, next_review_date=%s, updated_at=NOW()
        WHERE id=%s
    """, (interval_days, next_dt, card_id))
    conn.commit(); cur.close(); conn.close()

# 5) Delete flashcard
def delete_flashcard(card_id):
    conn = create_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM flashcards WHERE id=%s", (card_id,))
    conn.commit()
    cur.close(); conn.close()
