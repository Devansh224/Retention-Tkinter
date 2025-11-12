# chapters.py
from db_connection import create_connection

def add_chapter(user_id: int, subject_id: int, name: str):
    conn = create_connection(); cur = conn.cursor()
    cur.execute("""
        INSERT INTO chapters (user_id, subject_id, name)
        VALUES (%s, %s, %s)
    """, (user_id, subject_id, name))
    conn.commit(); cur.close(); conn.close(); return True

def get_chapters(user_id: int, subject_id: int):
    conn = create_connection(); cur = conn.cursor()
    cur.execute("SELECT id, name FROM chapters WHERE user_id=%s AND subject_id=%s ORDER BY created_at",
                (user_id, subject_id))
    rows = cur.fetchall(); cur.close(); conn.close(); return rows

def delete_chapter(user_id: int, subject_id: int, chapter_id: int):
    conn = create_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM chapters WHERE user_id=%s AND subject_id=%s AND id=%s",
                (user_id, subject_id, chapter_id))
    conn.commit(); cur.close(); conn.close(); return True
